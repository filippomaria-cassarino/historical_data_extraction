# Decision log

## 2026-10-08 — Initial scope
- Begin with targeted quantitative fisheries variables, not comprehensive historical narrative extraction.
- Use observation-level JSON with controlled vocabularies for classification fields and free text for source-reported values.
- Preserve historical units and temporal/spatial expressions; avoid unsupported normalization.
- Test small PDF chunks and persist each output rather than relying on Playground browser state.
- Store original PDFs, raw JSON, validated examples, and extraction rules separately.

## Open questions
- Define a stable observation identifier and deduplication method.
- Evaluate treatment of multi-location and discontinuous-time observations.
- Specify how to represent age/size distributions and sample sizes.
- Validate recall and field accuracy on manually curated pages across reports.
- Choose exact API model/version, retry policy, and PostgreSQL mapping.
