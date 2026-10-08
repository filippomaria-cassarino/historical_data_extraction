# Project context

Goal: extract reproducible, auditable quantitative fisheries observations from historical Irish sea and inland fisheries reports and scientific investigations, for future stock and fisheries modelling.

Initial scope: species/taxon, catch, landings, abundance, size, age, maturity, fishing effort, location, time, original units, and source provenance.

Sample reports supplied during development: 1890, 1909, 1914, 1944. These are test excerpts, not a representative evaluation corpus.

Planned workflow: PDF pages -> model extraction with a versioned prompt and strict JSON schema -> raw JSON saved immediately -> validation -> curated data -> PostgreSQL -> R/Python analysis.

Process small page chunks (initially 1–2 pages); do not request an entire report as one large response. Preserve original source PDFs and raw model responses.

This folder is the authoritative record of protocol decisions when provided to the assistant. The assistant cannot automatically access local Windows files from a normal chat; share updated project files or use an enabled local-file workflow.
