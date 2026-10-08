# Historical fisheries extraction

Reproducible development of a quantitative extraction pipeline for historical Irish fisheries PDF reports.

## Getting started
1. Read `PROJECT_CONTEXT.md`, `EXTRACTION_RULES.md`, and `DECISION_LOG.md` before modifying prompts or extraction outputs.
2. Store source PDFs in `data/original_pdfs/` (not tracked by Git by default).
3. Test small page chunks and save raw responses before review.
4. Add manually checked examples to `examples/validated/` and record changes in `DECISION_LOG.md`.
5. Pin the prompt version, schema version, model ID, source PDF checksum, and page range for each API run.

The project currently contains a protocol and schema, not an implemented extraction script. Do not treat outputs as validated until reviewed.
