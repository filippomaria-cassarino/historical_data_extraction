import re
import csv
from pathlib import Path
import pymupdf

KEYWORDS = {
    "Herring": ["herring", "herrings", "clupea harengus"]
}

# Paths
pdf_path = Path("data/original_pdfs/Report of the Sea and Inland Fisheries, 1890.pdf")
output_dir = Path("data/information_location")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "herring_1890.csv"


def classify_page(text):
    text = re.sub(r"\s+", " ", text.lower())

    matches = []

    for category, words in KEYWORDS.items():
        if any(
            re.search(rf"\b{re.escape(word)}\b", text)
            for word in words
        ):
            matches.append(category)

    return matches


# Search PDF
results = []

with pymupdf.open(pdf_path) as doc:
    for page_index, page in enumerate(doc):
        categories = classify_page(page.get_text())

        for category in categories:
            results.append({
                "pdf_name": pdf_path.name,
                "pdf_page": page_index + 1,
                "category": category
            })

# Save CSV
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["pdf_name", "pdf_page", "category"]
    )
    writer.writeheader()
    writer.writerows(results)

print(f"Found {len(results)} matching pages.")
print(f"Saved to: {output_path}")