# Extraction rules v0.3 — project reference (not sent to API)

The runtime instructions are entirely contained in `prompts/extraction_v0.3.md`. Do **not** append this file to the API request; doing so duplicates tokens and risks conflicting instructions.

## Scientific scope
- Include quantitative catch, landings, abundance, size, age, maturity and fishing effort (including vessels, fishers, trips and survey effort).
- Exclude monetary values, qualitative claims lacking quantities, unrelated morphology, and administrative material.
- Preserve historical terms, species/group names, units, temporal and spatial descriptions. Do not silently standardize, convert or infer.
- Distinguish commercial landings, survey catches, experimental fishing; landing place versus catch area; publication date versus observation date.
- Preserve source page/table and enough evidence to audit each value. Flag illegibility; never fabricate values or treat blanks as zero.

## Exhaustiveness and quality
- Examine every page, table, continuation and quantitative paragraph.
- For every table, identify relevant columns, enumerate every row, and output one observation per relevant nonblank cell.
- Internally audit table-cell coverage before returning output; never select representative rows.
- Avoid duplicate measurements repeated in prose and tables, while preserving distinct measures.
- Manually validate completeness and transcription accuracy against page images; JSON Schema validates shape, not correctness.
- Save model version, generation settings, exact runtime prompt, schema, source-page range, hashes, outputs and review results for reproducibility.