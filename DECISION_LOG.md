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

## 14 Oct 2026 - First update
- table extraction retains most values, but it needs to become more flexible to allow for catch at age/size; maybe edit schema?
- Tocken consumption is high: reduce data, schema and prompt to a minimum.
- Entire pdfs cannot be sent. We could break down the text into tematic chunks in txt for the AI and loop the extraction around these. Answer: break into chunks, but keep pdf
- Appendixes may contain the same information, but more structured
- Reports contain data from  ultiple years. A year search might avoid useless duplications
- Some reports have tables shared between pages

