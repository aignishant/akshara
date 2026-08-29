# ADR-0007 — The plan's tables are projected; the plan's judgement is read in full

- **Date:** 2026-08-29
- **Day:** — (repo tooling, between Day 15 and Day 16)
- **Phase:** 2
- **Status:** accepted
- **Amends:** `CLAUDE.md`'s mandatory read order. **No section of the master plan changes; it
  stays v1.3.0.**
- **Related:** ADR-0002 (the depth contract) · ADR-0003 (three-digit days and folder slugs)

## Context

`CLAUDE.md` ordered four documents read before anything else. Measured on 2026-08-29, at Day 15
written:

| File | Bytes | ~tokens |
| --- | ---: | ---: |
| `docs/00_MASTER_PLAN.md` | 113,283 | 28,320 |
| `CLAUDE.md` | 22,222 | 5,555 |
| the last day's `LESSON.md` | 14,744 | 3,686 |
| the last day's `CHECKLIST.md` | 9,231 | 2,307 |
| `docs/TRACEABILITY.md` | 2,588 | 647 |
| `docs/PROGRESS.md` | 557 | 139 |
| **Total, every session** | **162,625** | **≈ 40,656** |

The plan is 70% of that. Inside the plan, **54% is table data**: §7–§23, the curriculum ID tables,
at 31,958 bytes, and §24, the day map, at 26,554. To write Day 16 a session needs *three rows* of
those 58,512 bytes — its own §24.2 row and the two §7–§23 rows defining `TOK-16` and `TOK-17`.

The obvious alternative — shortening the plan — was tested and rejected. Measuring 8-gram overlap
between the three documents that state the contract found **4.0%** (§25 against `CLAUDE.md`),
**6.0%** (§25 against the day-generating skill) and **3.9%** (`CLAUDE.md` against the skill). There
is no duplication to remove. What is large is large because it is saying something.

## Decision

**Facts are projected mechanically. Judgement is read in full or not at all.**

1. **`scripts/brief.py`, run as `./m brief N`**, prints day N's §24.2 row, the §7–§23 definition of
   every ID that day must close, its §24.1 phase and gate, the rows for the days either side, and
   the last row of `docs/PROGRESS.md` — **every line copied verbatim**. It generates a header, a
   table of `sed` commands, and one loud row for the case where the plan names an ID no curriculum
   table defines. `tests/test_brief.py` asserts that invariant across every shape of day the plan
   contains, including the days that close no IDs.

2. **`CLAUDE.md`'s read order starts with the brief**, and names §2, §6, §25 and §28 as sections
   read *in full* when the task calls for them. The brief itself prints the command that fetches
   each one. Nothing is summarised: a compressed depth contract is a compressed day.

3. **`scripts/depth_check.py` gains two rules** — every relative link to a curriculum document must
   resolve, and §11's ledger row must carry `docs/PROGRESS.md`'s seven columns with the day it
   belongs to. Both were invariants the project stated about itself and nothing enforced.

## Consequences

Measured, same day, same files:

| Session | Before | After | Saved |
| --- | ---: | ---: | ---: |
| Any session's floor | 40,656 tok | 12,814 tok | 68% |
| Writing a day (adds the day skill, §2, §6, §25, §28 in full) | 45,361 tok | 25,684 tok | 43% |
| Answering a question about the plan | 33,876 tok | 6,034 tok | 82% |

- The brief is **not citable**. It says so in its own header: cite the plan, never the projection.
- If the plan's table shapes change, the brief goes wrong *loudly* — `tests/test_brief.py` fails,
  because a projected row would no longer match a source line.
- Enforcing link resolution turned up **11 broken cross-day links and one dead `prerequisites`
  path**, all from Day 10's folder and section slugs being renamed. They are fixed in this change.
  This is the cost of ADR-0003's "the number is the identity, the slug is a label on it": slugs
  move, and until now nothing noticed.
- **Rejected, deliberately:** compressing `CLAUDE.md`, §2, §6, §25 or §28; deduplicating the three
  rule documents (measured above); and generating any summary of a day's parts. The parts are the
  product, and an LLM-written précis of them is Principle 8's failure mode with a helpful face.
- **Deferred:** projecting the previous day's hub and checklist (23,975 bytes). Continuity is
  judgement, and the saving is not worth guessing at it.
