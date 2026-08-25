# ADR-0002 — A day is a hub plus one document per subtopic, and every tensor gets a shape table

- **Date:** 2026-08-25
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Establishes:** master plan §25 (the depth contract)
- **Related:** ADR-0001

## Context

The default format for a technical curriculum is one long document per topic. It looks thorough, and
it fails in three specific ways:

1. **A subject cannot be revisited alone.** A reader who wants to re-read only "what is a KV cache"
   re-reads prefill, TTFT and eviction to get there.
2. **A thin subtopic is invisible.** With one file per day there is no artifact that distinguishes
   "this day covered six subtopics and one of them got two paragraphs" from "this day covered five".
   Nothing in the repo can tell the difference, so nothing catches it.
3. **A time estimate at the top authorises the worst edit in technical writing** — cutting the
   explanation because the document is getting long.

A fourth failure is specific to this subject. Transformer code is tensor code, and **more bugs in it
are shape bugs than are algorithm bugs.** A document that writes `x = x.view(B, T, self.n_head, hs).transpose(1, 2)`
and moves on has handed the reader a line they can copy and cannot debug.

## Decision

A day is **one hub (`LESSON.md`) plus one document per subtopic** under `parts/`, with:

- **eleven required part sections in order**, nine unconditional and two conditional (§25.4);
- **`## Shapes` mandatory whenever a part introduces or transforms a tensor** — one row per tensor:
  symbolic shape, the concrete numbers used in this part, and **what each axis means**. Symbols
  (`B`, `T`, `C`, `H`, `hs`, `V`) are fixed curriculum-wide (Principle 20);
- **`**Line by line:**` mandatory after every non-exempt code block** (§28.3);
- **`In production` mandatory in every part** — the section that makes a document professional
  rather than introductory;
- **no time estimate anywhere**, with a carve-out for *measured* durations, which are data
  (Principle 8) rather than a clock;
- **at least one deliberate-failure part per day**;
- a `level` ladder (`foundation` → `working` → `production`) that a day climbs.

`scripts/depth_check.py` (`./m depth [N]`) enforces the mechanical half.

## Consequences

**Good.**

- A subtopic can be re-read, linked to, and reviewed on its own.
- Thinness is visible from `docs/TRACKER.md` without opening a day.
- The `Shapes` requirement makes the single most common failure mode in this subject
  un-skippable — and it is machine-checkable, because a code block that calls `.view`, `.transpose`
  or `einsum` and sits in a part with no `## Shapes` heading is a detectable state.

**Costly, accepted.**

- Days are folders, not files. Navigation depends on the hub's §2 map, which is therefore mandatory
  and is checked for linking every part on disk.
- The checker cannot judge whether an explanation is *good*. §25.8 lists the failure modes for
  review-by-reading; the script only catches structure.

**Rejected alternatives.**

| Alternative | Why not |
| --- | --- |
| One file per day | The three failures above. This is the format being replaced. |
| Shapes as a convention, not a checked rule | Conventions in teaching material decay silently, and this is the one whose decay costs the reader the most. |
| Ban every mention of a duration | Would ban `p95 latency`, `GPU-minutes`, and `the run took 43 min on a T4` — which are measurements, and Principle 8 wants more of them, not fewer. |
