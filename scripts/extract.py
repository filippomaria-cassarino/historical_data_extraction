
## Extract structured fisheries observations from a PDF using the OpenAI Responses API.
import argparse # allows arguments such as --pdf, --pages, --model
import base64   # converts PDF bytes into a representation suitable for the API request
from datetime import datetime, timezone # timestamps for output files and metadata
import hashlib # computes SHA256 hashes for provenance
import io # used to create a file-like object for the PDF bytes
import json # used to read/write JSON files
from pathlib import Path # used to resolve paths relative to the project root
import re # checks the format of page ranges

from dotenv import load_dotenv # Loads your API key from .env
from openai import OpenAI # OpenAI client for the Responses API
from pypdf import PdfReader, PdfWriter # used to read the input PDF and create a new PDF containing only the selected pages

ROOT = Path(__file__).resolve().parents[1] # project root directory (historical_fisheries_extraction folder)

# Reproducibility function
def sha256(data: bytes) -> str: #  hashes show whether two extraction runs used identical input files
    return hashlib.sha256(data).hexdigest() 

# Extraction function
def main(): 
    # define arguments to specify in the terminal (pdf, pages, model)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to input PDF, relative to project root or absolute"
    )
    parser.add_argument(
        "--pages",
        default=None,
        help="Optional 1-based page range, e.g. 1-2 or 3. Default: all pages"
    )
    parser.add_argument(
        "--model",
        default="gpt-4.1",
        help="PDF-capable OpenAI model"
    )
    args = parser.parse_args()

    # resolve and validate PDF path
    pdf_path = Path(args.pdf)
    if not pdf_path.is_absolute():
        pdf_path = ROOT / pdf_path

    if not pdf_path.is_file():
        parser.error(f"PDF not found: {pdf_path}")

    # read PDF and determine page count
    original_pdf = pdf_path.read_bytes()
    reader = PdfReader(io.BytesIO(original_pdf))
    total_pages = len(reader.pages)

    if total_pages == 0:
        parser.error("PDF contains no pages")

    # select pages: all by default, or specified range
    if args.pages is None:
        start = 1
        end = total_pages
    else:
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", args.pages)

        if not match:
            parser.error("--pages must be like 1, 1-2 or 3-4")

        start = int(match.group(1))
        end = int(match.group(2) or start)

        if start < 1 or end < start or end > total_pages:
            parser.error(
                f"Invalid page range. PDF contains {total_pages} pages."
            )

    pages_label = f"{start}-{end}"

    # load prompt, rules and JSON schema at the latest version
    prompt_path = ROOT / "prompts" / "extraction_v0.3.md"
    rules_path = ROOT / "EXTRACTION_RULES_v0.3.md"
    schema_path = ROOT / "schemas" / "fisheries_v0.2.json"

    prompt_bytes = prompt_path.read_bytes()
    rules_bytes = rules_path.read_bytes()
    schema_bytes = schema_path.read_bytes()

    # v0.3 prompt contains rules, but we don't send them to the API. We keep them in the metadata for provenance.
    instructions = prompt_bytes.decode("utf-8")
    schema_config = json.loads(schema_bytes)

    # create PDF containing selected pages
    writer = PdfWriter()

    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])

    buffer = io.BytesIO()
    writer.write(buffer)
    subset_pdf = buffer.getvalue()

    encoded = base64.b64encode(subset_pdf).decode("ascii")

    # initialize OpenAI client
    load_dotenv(ROOT / ".env")
    client = OpenAI()

    print(
        f"Extracting pages {pages_label} of "
        f"{pdf_path.name} with {args.model}..."
    )

    # submit PDF for structured extraction
    response = client.responses.create(
        model=args.model,               # change model?
        instructions=(
            instructions
            + f"\n\nThe submitted PDF contains original PDF pages "
              f"{start} through {end}. "
              f"Submitted page 1 corresponds to original PDF page {start}. "
              "Use original PDF page indices (1-based) in source_page, "
              "not page indices within the submitted excerpt."
        ),
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Extract all in-scope quantitative fisheries "
                            "observations from this PDF excerpt. "
                            "Return structured JSON."
                        ),
                    },
                    {
                        "type": "input_file",
                        "filename": (
                            f"{pdf_path.stem}_pages_{pages_label}.pdf"
                        ),
                        "file_data": (
                            f"data:application/pdf;base64,{encoded}"
                        ),
                    },
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": schema_config["name"],
                "strict": True,
                "schema": schema_config["schema"],
            }
        },
    )

    if not response.output_text:
        raise RuntimeError(
            f"No JSON output returned (response status: {response.status})."
        )

    extracted = json.loads(response.output_text)

    # save extracted observations
    outdir = ROOT / "outputs" / "raw"
    outdir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )

    basename = f"{pdf_path.stem}_p{pages_label}_{timestamp}"

    output_path = outdir / f"{basename}.json"
    metadata_path = outdir / f"{basename}.metadata.json"

    output_path.write_text(
        json.dumps(extracted, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # save provenance and API usage
    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pdf_path": str(pdf_path),
        "pages": pages_label,
        "page_start": start,
        "page_end": end,
        "total_pdf_pages": total_pages,
        "pdf_sha256": sha256(original_pdf),
        "submitted_pages_sha256": sha256(subset_pdf),
        "prompt_sha256": sha256(prompt_bytes),
        "rules_sha256": sha256(rules_bytes),
        "rules_sent_to_api": False,
        "schema_sha256": sha256(schema_bytes),
        "model_requested": args.model,
        "model_returned": response.model,
        "response_id": response.id,
        "usage": (
            response.usage.model_dump()
            if response.usage else None
        ),
        "observation_count": len(
            extracted.get("observations", [])
        ),
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(
        f"Saved {metadata['observation_count']} observations: "
        f"{output_path}"
    )
    print(f"Saved provenance metadata: {metadata_path}")


if __name__ == "__main__":
    main()

