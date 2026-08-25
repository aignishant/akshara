# ADR-0004 — `RUNS.md` is a ledger, and no weight file ever enters git

- **Date:** 2026-08-25
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Establishes:** Principles 8, 9, 10 · master plan §27
- **Related:** ADR-0001

## Context

This repo differs from an ordinary software repo in two ways that both bite hard if they are not
decided up front.

**Results are not in the code.** A training run's meaning lives in a config, a seed, a piece of
hardware and an outcome. Six weeks later, the difference between a result and an anecdote is whether
those four things were written down at the time. They cannot be reconstructed afterwards, and
"I think I used a cosine schedule" is not a reproduction.

**Artifacts are enormous and permanent.** A 400MB checkpoint committed once is in git history
forever, cannot be removed without rewriting history, and makes the repo effectively unclonable. The
mistake is one `git add -A` away, on a day when the learner is tired and the run finally worked.

There is a third, subtler problem: a ledger that only records successes is a ledger someone has been
editing. Divergence, OOM and pre-emption are the normal texture of training, and hiding them teaches
the wrong lesson about what the work is like.

## Decision

**1. `docs/RUNS.md` is an append-only ledger with one row per training run**, carrying: run id, day,
config path, config hash, seed, hardware string, steps, tokens, train/val loss, wall time,
checkpoint location, outcome, and which of the five silent failures (§6) was ruled out and how.

**2. Failed runs get rows.** `Outcome` is one of `ok` · `diverged` · `oom` · `preempted` ·
`abandoned`, plus a clause of what was learned (Principle 10).

**3. Configs are committed; weights and data are not** (Principle 9). `configs/` is tracked.
`.gitignore` blocks `*.safetensors`, `*.gguf`, `*.bin`, `*.pt`, `*.pth`, `*.ckpt`, `*.npy`,
`data/`, `checkpoints/`, `runs/`.

**4. `./m done N` refuses to commit if any of those are staged**, and prints the offending paths.
A rule that depends on remembering it is not a rule.

**5. Downloaded artifacts are pinned by revision SHA before use** — `docs/MODELS.md` and
`docs/DATASETS.md` — with licence, and for models, **safetensors only**: `torch.load` on an
untrusted pickle executes arbitrary code at load time (Principle 13, SAFE-11).

## Consequences

**Good.**

- Any run in the project's history can be re-derived from git plus a documented download.
- The catastrophic-and-irreversible mistake is blocked mechanically rather than culturally.
- `DATASETS.md` carrying a `Decontaminated?` column makes Silent Failure #1 a visible, auditable
  state instead of an assumption. Day 147 (SAFE-14) audits the whole table.

**Costly, accepted.**

- More bookkeeping per training day. The day documents therefore print the exact row to paste, and
  the checklist has a box for it, so the cost is paid in seconds rather than in willpower.
- Checkpoints must live outside the tracked tree, so `AKSHARA_CHECKPOINT_DIR` is an environment
  variable rather than a hardcoded path.

**Rejected alternatives.**

| Alternative | Why not |
| --- | --- |
| Git LFS for checkpoints | Still couples repo size to artifact count, and free LFS quota is a budget — which §4 forbids depending on. |
| An experiment tracker (W&B) as the source of truth | A hosted account is not $0-guaranteed and not clonable. It is supported as an *optional* mirror; the ledger in git is the record. |
| Trust `.gitignore` alone | One `git add -f`, or a path the pattern misses, and it is permanent. The `./m done` check is the backstop. |
