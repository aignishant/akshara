# Plan Changelog — Project Akshara

Append-only. Principle 14: **if reality changes, the plan is amended first.** A breaking library
release, a dataset losing its licence, a free tier closing, a paper being superseded → an entry
here (and an ADR if the change is structural) → *then* code. Days are never silently patched.

Principle 19 lives here too: when a day turns out to hold two ideas and is split, the day count
changes, and the change is recorded here rather than argued about later.

| Date | Plan version | Change | Why | ADR |
| ---- | ------------ | ------ | --- | --- |
| 2026-08-25 | v1.0.0 | Initial plan: 17 curricula, 309 IDs, 162 days, 22 phases. | — | ADR-0001 |
| 2026-08-25 | v1.1.0 | Papers become teaching, not citations: Principle 21, the §24.3 roster (130 papers across 88 days), the §25.10 paper-part contract, the `papers:` hub key, and `docs/PAPERS.md`. | A citation says an idea has a source and teaches nothing about it. Naming a paper and moving on is the citation equivalent of an unexplained line of code. | ADR-0005 |
| 2026-08-25 | v1.1.0 | Day 1's title in §24.2 reworded, and the Day 0 / Day 1 boundary stated explicitly under §24.2's Phase 0 table. | Writing Day 0 surfaced two defects in the row: it claimed `uv + Python 3.12` and `.gitignore`, which Day 0 already builds, and it said **five** ledgers when v1.1.0 made it seven. No ID moved; OPS-01..04 still close on Day 1. | — |
