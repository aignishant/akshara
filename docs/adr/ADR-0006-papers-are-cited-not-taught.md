# ADR-0006 — Paper parts are removed; papers return to being cited

- **Date:** 2026-08-26
- **Day:** 1 (pre-curriculum tooling)
- **Phase:** 0
- **Status:** accepted
- **Amends:** master plan v1.1.0 → **v1.2.0**
- **Supersedes:** ADR-0005 (papers are taught)
- **Removes:** Principle 21 · §24.3 (the paper roster) · §25.10 (the paper-part contract) ·
  the `papers:` hub frontmatter key · `docs/PAPERS.md`
- **Related:** ADR-0002 (the depth contract)

## Context

ADR-0005 made every paper the curriculum rests on into a full teaching document: its own part, in a
dedicated section last in the day, carrying three sections beyond the standard nine — including
**`The paper in one small project`**, the smallest end-to-end runnable implementation of the
paper's contribution, with a mandatory A/B ablation, living in the day's own `papers/` directory.

The roster in §24.3 committed the curriculum to **130 papers across 88 of the 162 days**.

ADR-0005 called that cost out and accepted it: *"This is the single largest addition to the plan's
length. It is also the one most worth paying for."* That judgement was made before any paper part
had been written, on Day 0, when the cost was an estimate rather than an observation.

The cost is now the binding constraint. Each paper part is a full part under the §25.4 contract
**plus** a read of the actual paper, **plus** an isolated runnable demo with an ablation, **plus** a
`docs/PAPERS.md` row with a live-resolved identifier — multiplied by 130. That is a second
curriculum running alongside the first, and it consumes the budget that the mechanism teaching,
the lab code and the training runs need. The plan's own §25.7 test applies to the plan itself: when
a unit needs "and also" to introduce its second half, it is two units. Akshara is a *build* course;
the literature course ADR-0005 bolted onto it is a different project.

## Decision

**Paper parts are removed. Papers return to being cited, under Principle 8 — which is where
v1.0.0 had them.**

Concretely, deleted from the plan:

1. **Principle 21** — "a paper the field rests on is taught, not cited".
2. **§24.3, the paper roster** — the 130-paper / 88-day mapping and its `24.3.1` commentary.
3. **§25.10, the paper-part contract** — all four subsections: where paper parts live, what one
   must contain, the rules around them, and the argument for their length.
4. **The `papers:` hub frontmatter key**, and the enforcement of it in `scripts/depth_check.py`.
5. **`docs/PAPERS.md`**, the paper ledger. It held no rows: no paper part was ever written, so
   nothing is lost and no append-only history is rewritten.

**What is deliberately kept.**

- **Principle 8 is untouched and remains the rule that matters here.** Every empirical claim is
  still *"measured here, on `<hardware>`, seed `<n>`, `<date>`"* or *"reported in
  arXiv:XXXX.XXXXX §N"*. A benchmark number recalled from memory is still a rumour. Identifiers are
  still resolved live, never written from memory, or left as a `TODO` carrying the exact lookup
  command.
- **§28's citation rule** — cite by arXiv id and section, *"the √d_k scaling argument
  (arXiv:1706.03762 §3.2.1)"*. "The literature shows" is still not a citation.
- **The §26 freshness check** still asks, per phase, whether a paper the phase cites has been
  corrected, retracted or superseded.
- **`ARCH-25` and Day 40** — *"the original paper vs what people actually build now, a diff, item by
  item"* — are **unchanged**. That is a 🔍 compare day about an architecture, not a paper part, and
  removing it would move the day count (Principle 19). No curriculum ID, day boundary, phase, gate
  or compute policy changes under this ADR.

## Consequences

**Good.**

- The plan is ~31,000 characters shorter, and a day's writing budget goes to the mechanism, the
  lab and the failure part rather than to a parallel literature track.
- `depth_check.py` loses five rules, three helpers and a counter; the contract it enforces is again
  the one contract in §25.4.
- Days no longer carry a mandatory trailing section that is the same shape on 88 of them.

**Costly, accepted.**

- **The reader is not walked through the arguments behind the defaults they inherit.** ADR-0005's
  central claim was real: *"temperature 0.7 is best", "twenty tokens per parameter", "LoRA rank 16
  is standard"* are real results from real papers under conditions nobody restates. Principle 8
  keeps the curriculum from *repeating* those numbers unsourced; it does not teach the reader to
  interrogate them. That gap is now open and is accepted deliberately, not overlooked.
- **`What came after` is lost as a required section.** No structural place now says which defaults
  the field quietly abandoned. Where that matters for a specific day, it belongs in that part's
  `In production` section.
- Re-adding paper coverage later is another amendment. That is the intended friction.

**Rejected alternatives.**

| Alternative | Why not |
| --- | --- |
| Keep paper parts, drop only the runnable small project | Removes the most expensive half but leaves 130 mandatory documents and the roster, the ledger and the frontmatter key. The cost driver is the per-day obligation, not only the demo. |
| Make paper parts optional — keep §25.10 as "may" | Leaves an unenforced contract in a plan whose whole premise is that contracts are checked mechanically. An unenforced rule rots, and `./m depth` could no longer speak to it. |
| Keep the §24.3 roster as suggested reading | A list of 130 titles nobody is required to act on is the "further reading" list ADR-0005 correctly rejected as useless. |
| Delete `ARCH-25` / Day 40 along with the paper machinery | Day 40 is an architecture diff, not a paper part. Removing it would move the day count and needs its own argument (Principle 19). |
| Leave `docs/PAPERS.md` in place, unused | A ledger nobody writes to is a claim the curriculum tracks something it does not. It has zero rows; deleting it is honest. |
