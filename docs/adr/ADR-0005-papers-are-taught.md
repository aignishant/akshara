# ADR-0005 — A paper the field rests on gets its own part

- **Date:** 2026-08-25
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Amends:** master plan v1.0.0 → **v1.1.0**
- **Establishes:** Principle 21 · §24.3 (the paper roster) · §25.10 (the paper-part contract)
- **Related:** ADR-0002 (the depth contract)

## Context

v1.0.0 already required every empirical claim to be *cited* (Principle 8): an arXiv id and a
section, never a number from memory. That is necessary and it is not sufficient.

A citation says the idea has a source. It teaches nothing about the source. And the obvious
remedy — "read the paper" — is advice almost nobody acts on, because a reader facing a nine-page
PDF does not know which parts matter, what the notation means, or which of the paper's claims the
field later abandoned. The result is the failure mode this whole field runs on: **half-remembered
claims detached from their conditions.** "Temperature 0.7 is best." "Twenty tokens per parameter."
"LoRA rank 16 is standard." Every one is a real result, from a real paper, measured under conditions
nobody restates.

There is also a plain gap in coverage. 88 of the 162 days rest on a specific published result. Under
v1.0.0 those days would teach the mechanism and reduce its origin to a parenthesis — which is
exactly the "summary in place of explanation" failure §25.8 already forbids for code.

## Decision

**A paper gets a part**, under the same contract as every other part, plus two sections of its own.

1. **Principle 21** — a paper the field rests on is taught, not cited.
2. **§24.3, the paper roster** — 130 papers mapped to 88 days, **listed by title and year only**.
   Principle 8 forbids writing a number from memory and an arXiv id is a number, so identifiers are
   resolved live at generation time and recorded in `docs/PAPERS.md` before the part is written. A
   plan shipping 130 remembered identifiers would be teaching the opposite of what §25.10 exists to
   teach.
3. **§25.10, the paper-part contract** — one part per paper, in a dedicated section **last in the
   day**, carrying the nine unconditional sections plus three:
   - **`The paper in one small project`** — the smallest end-to-end runnable project that implements
     the paper's contribution *and nothing else*, at T0, with an **A/B** that switches the idea off.
     Reading a paper produces recognition; re-implementing its contribution in fifty lines and
     watching the effect appear and disappear produces understanding. **The isolation is the
     pedagogy**: being able to strip an idea to the smallest thing that still demonstrates it is the
     proof you understood what the paper added. This is Principle 3 applied to the literature.
   - **`What the paper showed`** — the evidence, cited to its table, and what it does *not* support;
     also where the demo's number and the paper's number get compared out loud.
   - **`What came after`** — corrections, supersessions, failed reproductions.
4. **`papers:` becomes a required hub key**, with `papers: []` as the answer when a day rests on
   none — the same "an empty answer is still an answer" rule the compute budget already uses.
5. **`docs/PAPERS.md`**, which distinguishes `taught` from `cited`, making "we mentioned it" and
   "we explained it" different and checkable states.

`scripts/depth_check.py` enforces the mechanical half: the frontmatter keys, the two extra sections
and their order, the missing `papers:` key, and a hub whose declared paper count disagrees with the
`kind: paper` parts on disk.

## Consequences

**Good.**

- The reader learns *why* attention scales by √d_k, not just that it does — which is what lets them
  reason about the next architecture instead of memorising this one.
- After ~130 paper parts, reading an unfamiliar paper — find the contribution, find the evidence,
  find what the evidence does not support — is a transferable skill that outlives every specific
  result in the plan.
- `What came after` means no reader ends up defending a 2017 default in 2027.
- The distinction between `[reported: Table 3]` and `[measured here: seed 1337]` becomes a habit
  rather than a rule, which is the only way Principle 8 survives 162 days. The small project is what
  forces it: the learner ends up holding both numbers at once.
- The small projects accumulate into something unplanned but valuable — a `papers/` tree of
  ~130 minimal, runnable, individually ablatable implementations of the field's core results.

**Costly, accepted.**

- This is the single largest addition to the plan's length. It is also the one most worth paying
  for; §25.10.4 states the argument.
- Writing a paper part requires actually reading the paper. That is a real cost per day and it is
  non-negotiable — §25.10.3 rule 4 exists because a paper part written from an abstract is *worse*
  than none, since it launders unreliability through the appearance of rigour.

**Rejected alternatives.**

| Alternative | Why not |
| --- | --- |
| Keep citations, add a "further reading" list per day | This is what v1.0.0 effectively had. Nobody reads a link list, and it makes no claim checkable. |
| A separate `papers/` tree outside `days/` | Decouples the paper from the day whose code it explains, and the coupling is the pedagogy: *"`apply_rope()` is §3.4.2 of this paper"*. |
| Put the paper part first in the day | A reader sent to a paper before they understand the mechanism learns to be intimidated by papers. Teach the idea, then read the argument. |
| Ship arXiv ids in the plan | Would put 130 remembered numbers into the document that forbids remembered numbers. |
| A paper part with no runnable demo | Produces recognition, not understanding. The reader can quote the paper and cannot argue about it. |
| Demonstrate the paper inside the full Akshara model | The effect disappears among fifty other moving parts. Isolation is the whole point. |
| Skip the A/B to save length | A demo that only shows the code runs demonstrates nothing. The ablation is the only part that proves the claim. |
