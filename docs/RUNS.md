# Run Ledger — Project Akshara

Append-only. **This is the ledger an ordinary project does not have, and the one that will save
you.** Six weeks after a training run, the only difference between a result and an anecdote is a
row containing a seed, a config hash and a hardware line (Principle 9).

Every training run gets a row. **Including the ones that failed** — Principle 10: a run that
diverged is reported as diverged. A ledger with no failures in it is a ledger someone has been
editing.

Rules:

- `Config` points at a file in `configs/`, which **is** committed. The weights are not.
- `Hash` is of the config file, so "same config" is checkable rather than remembered.
- `Hardware` is the actual device string, not the plan: `T4 16GB (Colab)`, `CPU i7-1165G7`.
- `Outcome` is one of `ok` · `diverged` · `oom` · `preempted` · `abandoned`, plus one clause of
  what you learned. "preempted at step 4100, resumed as run 012" is a useful row.
- Before writing `ok`, state in the `Silent failure ruled out` column which of the five (plan §6)
  this run could have hit and how you checked. `overfit-1-batch passed` is the minimum for any run
  (Principle 12).

| Run | Day | Config | Hash | Seed | Hardware | Steps | Tokens | Train loss | Val loss | Wall | Checkpoint | Outcome | Silent failure ruled out |
| --- | --- | ------ | ---- | ---- | -------- | ----- | ------ | ---------- | -------- | ---- | ---------- | ------- | ------------------------ |
