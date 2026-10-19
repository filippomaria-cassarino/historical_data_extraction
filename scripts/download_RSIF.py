## This script downloads all PDF files from the Marine Institute's DSpace repository and saves them to a local directory. 
##It also creates a CSV manifest of the downloaded files.

import csv
import re
import time
from pathlib import Path

import requests

BASE = "https://oar.marine.ie/server"
COLLECTION = "2f5c23ac-46aa-41f4-b8ac-1f0ef10105ca"

OUTPUT = Path("data/original_pdfs")
OUTPUT.mkdir(parents=True, exist_ok=True)

session = requests.Session()


def get_json(url, params=None):
    response = session.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def get_all(url, params=None, nested_key=None):
    """Retrieve all records from a paginated DSpace endpoint."""
    results = []
    params = dict(params or {})
    params["size"] = 100

    page = 0

    while True:
        params["page"] = page
        data = get_json(url, params)

        if nested_key:
            data = data["_embedded"][nested_key]

        embedded = data.get("_embedded", {})

        records = next(
            (v for v in embedded.values() if isinstance(v, list)),
            []
        )

        results.extend(records)

        pagination = data.get("page", {})
        total_pages = pagination.get("totalPages", 1)

        print(f"Retrieved page {page + 1}/{total_pages}")

        page += 1

        if page >= total_pages:
            break

    return results


def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]', "_", name)


# Retrieve collection items
items = get_all(
    f"{BASE}/api/discover/search/objects",
    {
        "scope": COLLECTION,
        "dsoType": "item"
    },
    nested_key="searchResult"
)

print(f"Found {len(items)} collection records.")

import pymupdf

manifest = []

for result in items:

    item = result.get("_embedded", {}).get("indexableObject", {})
    item_id = item.get("uuid")

    if not item_id:
        continue

    title = item.get("name", item_id)

    year_match = re.search(r"\b(?:18|19)\d{2}\b", title)

    if not year_match:
        print(f"Skipping: {title}")
        continue

    year = year_match.group()
    print(f"Processing: {title}")

    bundles = get_all(
        f"{BASE}/api/core/items/{item_id}/bundles"
    )

    pdf_files = []

    for bundle in bundles:
        if bundle.get("name") != "ORIGINAL":
            continue

        files = get_all(
            f"{BASE}/api/core/bundles/{bundle['uuid']}/bitstreams"
        )

        pdf_files.extend([
            f for f in files
            if f.get("name", "").lower().endswith(".pdf")
        ])

    if not pdf_files:
        continue

    candidates = []

    for file in pdf_files:

        url = (
            f"{BASE}/api/core/bitstreams/"
            f"{file['uuid']}/content"
        )

        try:
            response = session.get(url, timeout=180)
            response.raise_for_status()

            pdf_bytes = response.content

            # Measure extractable text
            with pymupdf.open(
                stream=pdf_bytes,
                filetype="pdf"
            ) as doc:

                text_length = sum(
                    len(page.get_text().strip())
                    for page in doc
                )

            candidates.append({
                "uuid": file["uuid"],
                "url": url,
                "bytes": pdf_bytes,
                "text_length": text_length
            })

            print(f"  Candidate: {text_length} text characters")

        except (requests.RequestException, Exception) as e:
            print(f"  Failed: {e}")

        time.sleep(1)

    if not candidates:
        continue

    # Select PDF with most extractable text
    best = max(candidates, key=lambda x: x["text_length"])

    if best["text_length"] == 0:
        print(f"  No searchable PDF found: {title}")
        continue

    filename = f"RSIF_{year}.pdf"
    path = OUTPUT / filename

    # Avoid silently overwriting a different report
    if path.exists():
        print(f"  File already exists: {filename}")
        continue

    path.write_bytes(best["bytes"])

    manifest.append({
        "title": title,
        "year": year,
        "pdf_name": filename,
        "bitstream_id": best["uuid"],
        "download_url": best["url"],
        "text_characters": best["text_length"]
    })

    print(f"  Saved: {filename}")


# Save manifest
manifest_path = OUTPUT / "download_manifest.csv"

with open(manifest_path, "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "title",
            "year",
            "pdf_name",
            "bitstream_id",
            "download_url",
            "text_characters"
        ]
    )

    writer.writeheader()
    writer.writerows(manifest)

print(f"\nFinished. Saved {len(manifest)} reports.")