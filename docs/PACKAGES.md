# Package Ledger — Project Akshara

Append-only. Principle 6: **never invent a version number.** Every install gets a row here with the
version actually observed, the date it was observed, the day that added it, and why. If a version
could not be looked up, the row says `TODO(<the exact lookup command>)` — never a guess.

Packages arrive **on the day they are first used**, and — where the package does something the
curriculum teaches — only **after** the hand-rolled version exists (Principle 3). `tokenizers`
cannot arrive before Day 14, because Days 12–13 are where you write BPE yourself.

Plan §5.1: pins are stricter here than in ordinary projects because a loose ML dependency fails
*silently* — a changed optimizer default or normalization step still trains, just not the same
model.

| Package | Version | Date | Day | Why |
| ------- | ------- | ---- | --- | --- |
