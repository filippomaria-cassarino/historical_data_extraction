# Historical fisheries quantitative extraction v0.3

Extract **all** explicitly reported quantitative fisheries observations from the supplied PDF pages. Return only JSON conforming to the supplied schema.

**Scope:** catch, landings, abundance, size, age, maturity, and fishing_effort (including vessels, personnel, trips and sampling effort). Exclude monetary values/prices, qualitative claims without quantities, unrelated morphology and administration.

**Exhaustive table procedure (mandatory):**
1. Inspect every page, including page bottoms and continuation tables. Identify relevant measurement columns using headings, units, captions and footnotes.
2. Traverse **every row from first to last**, including older years. Emit **one observation per qualifying nonblank row × measurement-column cell**. For a 10-row table with one relevant column, return 10 observations; with two relevant columns, return 20. Never select representative rows or omit values to shorten the output.
3. Before finalizing, compare each relevant table cell against the emitted observations; correct omissions, duplicate cells and row/column misalignments. Ignore out-of-scope monetary columns, even when adjacent to catch quantities.
4. Then extract additional quantitative observations from prose, without duplicating measurements already extracted from tables. Distinct quantities in the same sentence require distinct observations.

**Fidelity:** Preserve source-reported species/group, value expression, unit, time, location and measurement definition. Use numeric values/bounds only when unambiguous; do not convert units, infer modern taxa, locations or dates, or mistake publication year for observation year. Never interpret blanks as zero. For partly legible cells, retain readable text and note uncertainty; do not invent digits. Distinguish catch from landings, commercial from survey/experimental data, and landing port from capture location.

**Provenance:** Give the source page. If no qualifying observations exist, return an empty `observations` array.
