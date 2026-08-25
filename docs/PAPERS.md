# Paper Ledger — Project Akshara

Append-only. **Principle 21: a paper the field rests on is taught, not cited.** Every paper in the
roster (plan §24.3) gets its own part, under the contract in §25.10 — and a row here **before that
part is written**.

**Why this ledger exists.** Principle 8 forbids writing a number from memory, and an arXiv id is a
number. The plan's §24.3 therefore lists papers by *title and year only*. This table is where the
identifier becomes real: resolved live, from a URL you actually fetched, on a date you record.

Rules:

- `Identifier` is the arXiv id where one exists, otherwise the venue and year (`ACL 2002`,
  `NeurIPS 2017`, `OSDI 2022`). Never both invented.
- `URL fetched` is the page you actually opened — the abstract page or the PDF — and `Fetched`
  is the date you opened it. A row with no fetch date is a row somebody guessed.
- `Part` is the paper part that teaches it: `days/day-043-.../parts/03-the-papers/3.1-....md`.
- A paper cited *in passing* by a part but not taught still gets a row, marked `cited` in `Taught?`.
  A paper that gets a part is marked `taught`. That distinction is the whole point of the ledger:
  it makes "we mentioned it" and "we explained it" different, checkable states.
- `Demo` is the path to the paper's small project — `papers/<slug>/` — the smallest runnable
  thing that implements that paper's contribution and nothing else (§25.10.2 section 9). Every
  `taught` row has one, including parked 🅿️ papers. A `taught` row with an empty `Demo` cell is a
  part that described a paper instead of demonstrating it.

| Paper | Year | Identifier | Day | Part | Demo | Taught? | URL fetched | Fetched |
| ----- | ---- | ---------- | --- | ---- | ---- | ------- | ----------- | ------- |
