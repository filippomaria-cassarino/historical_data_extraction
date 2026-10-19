# Extraction rules v0.2 

## Scope and fidelity

1. Extract only explicit quantitative observations in these categories: catch, landings, abundance, size, age, maturity, fishing_effort.
2. Keep source-reported species names, numerical expressions, units, locations, and times. Do not silently standardize or convert them.
3. Distinguish commercial landings from scientific survey catches and experimental fishing.
4. Extract one observation per distinct quantitative measurement, retaining row/column context and source provenance.
5. Historical time can be a month, year, interval, season, or disjoint periods. Preserve the original expression; only fill standardized start/end at supported precision.
6. Preserve original location wording and distinguish location type from role (catch area, landing place, vessel base, etc.).
7. Never assume publication year equals observation year.
8. Never treat missing or illegible values as zero. Flag uncertainty and OCR/table ambiguities.
9. Exclude prices, monetary values, purely qualitative statements, unrelated morphology, and administrative content.
10. Keep supporting source text short but sufficient to audit each observation; distinguish verbatim evidence from reconstructed row/column descriptions.
11. Avoid double-counting the same measurement repeated in narrative and table in the same excerpt.
12. Check page images when OCR or table layout is unreliable.

## Mandatory exhaustive table extraction

13. Inspect every page for all tables, tabulated lists, continuation tables, and relevant numeric prose, including material at page bottoms.
14. For each table, determine which columns contain qualifying fisheries measurements; exclude irrelevant columns without excluding the relevant columns of the same table.
15. Enumerate **every row**, including the oldest years and the final rows. Do not select representative or recent rows.
16. Create a separate observation for **each qualifying nonblank cell** at the intersection of a table row and relevant measurement column, preserving year, species, location, unit, and measurement definition. A 10-row table with one qualifying numeric column should yield 10 observations, unless specific cells are blank or out of scope.
17. If a qualifying cell is partly illegible, preserve what is readable and flag uncertainty; never guess digits. Do not create measurements from truly empty cells.
18. Before submitting JSON, audit each table row and relevant column against the observation list. Correct omissions and wrong row/column alignments. Check first, middle, and last rows explicitly.
19. Only after completing table extraction, extract additional measurements in narrative text and remove true duplicates.
20. Never shorten or summarize a table's extraction for brevity. If a table is too large for reliable extraction in one request, process it in smaller page/table chunks rather than deliberately dropping observations.

## Quality assurance

21. JSON schema validity is not evidence of complete extraction. Human review and, where possible, automated row/year coverage checks are required.
22. Record the exact prompt, schema, model, generation settings, source-page range, and file hashes for reproducibility.
