# ADR-0003 — Day folders are `day-NNN-<slug>`; the number is the identity, the slug is a label

- **Date:** 2026-08-25
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Related:** ADR-0002 (the depth contract)

## Context

The plan runs to Day 161. Two naming decisions follow, and both are cheap now and expensive later.

**Zero-padding.** With two digits, `day-9` sorts after `day-100` in every file listing, every editor
tab bar, every `git log --stat` and every glob. That is a papercut paid 162 times.

**Slugs.** `days/day-043/` and `parts/02/` are addresses, not answers. A hundred and sixty-two of
them are indistinguishable in a file tree, and a `git log` of `day-043: complete` tells a reader
nothing about what changed.

But a slug used as a *key* is a liability: the moment a better title suggests itself, renaming the
folder breaks every tool that resolved a day by its full name.

## Decision

- Day folders are **`day-NNN-<slug>`** — three digits, zero-padded, then a kebab-case slug of 1–4
  words from the hub's `title` with articles dropped: `days/day-030-scaled-dot-product/`.
- Section folders are **`NN-<slug>`** — two digits, zero-padded, then 1–3 words from the section's
  heading in the hub's §2 map: `parts/03-causal-mask/`.
- Part files are **`<section>.<subtopic>-<slug>.md`**, and the folder number must agree with the
  number before the dot.
- **The number is the identity; the slug is a label on it.** `./m`, `depth_check.py`, `tracker.py`
  and `trace.py` all resolve a day by number and accept whatever slug follows. A folder can be
  renamed to a better slug at any time without breaking anything.

## Consequences

**Good.**

- The file tree says what the curriculum teaches without opening anything.
- Sorting is correct everywhere, for free.
- Slugs can be improved as understanding improves, which is the normal case when writing 162 days.

**Costly, accepted.**

- Every tool must glob (`days/day-NNN-*`) rather than construct a path. That is four lines in `./m`
  and one regex in each script, written once.
- `./m depth` rejects a bare `days/day-030/` and a two-digit `day-30-…`. That strictness is the
  point: the rule only holds if it is enforced on day one rather than retrofitted at day ninety.
