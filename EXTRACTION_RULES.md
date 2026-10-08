# Extraction rules v0.1

1. Only extract explicit quantitative observations in these categories: catch, landings, abundance, size, age, maturity, fishing_effort.
2. Keep source-reported species names, numerical expressions, units, locations and times. Do not silently standardize or convert them.
3. Distinguish commercial landings from scientific survey catches and experimental fishing.
4. Extract separate observations for each distinct quantitative measurement; preserve row/column headings and source provenance.
5. Historical time can be a month, year, interval, season or disjoint periods. Preserve the original expression; only fill standardized start/end at supported precision.
6. Location can be a port, bay, fishing ground, administrative area, coastal stretch, etc. Preserve original wording and distinguish location type from role (catch area vs landing place).
7. Never assume the publication year equals the observation year.
8. Never treat missing or illegible values as zero. Flag uncertainty and OCR/table ambiguities.
9. Exclude prices, purely qualitative statements, unrelated morphology and administrative content in v0.1.
10. Keep supporting source text short but sufficient to audit each observation.
11. Avoid double counting a number repeated in narrative and table in the same excerpt.
12. Check extracted observations against page images when OCR or layout is unreliable.
