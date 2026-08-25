# Dataset Ledger — Project Akshara

Append-only. Every dataset gets a row **before it is downloaded** — Principle 13: blast radius
before capability, and Principle 6: pin the revision, not just the name.

**Pin the revision SHA, not the repo name.** A dataset owner can force-push, and your
"reproduction" silently becomes a different experiment (plan §5.1).

**The `Decontaminated?` column is not optional.** Silent Failure #1 (plan §6) is a benchmark test
set sitting inside a pretraining corpus. A corpus row that says `no` is a corpus that must not be
used for a run whose results you intend to report (TRAIN-23).

**Licence is checked before download, not after.** SAFE-14 audits this whole table on Day 147; a
row you cannot defend then is a row you should not have added now.

| Dataset | Source URL | Revision SHA | Licence | Size | Date | Day | Decontaminated? | Why |
| ------- | ---------- | ------------ | ------- | ---- | ---- | --- | --------------- | --- |
