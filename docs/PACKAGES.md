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
| `git` | 2.54.0.windows.1 | 2026-08-27 | 0 | Version control, and Git Bash — the shell every day document is written for. Observed with `git --version`. |
| `uv` | 0.12.3 | 2026-08-27 | 0 | One binary owns the interpreter, the packages, the lock and the run. Observed with `uv --version`. |
| `python` | 3.12.12 | 2026-08-27 | 0 | Runtime, per plan §5. Observed with `sys.version` under `uv run` — **not** the top of `uv python list`, which offers 3.12.13 as a download it has not installed. |
| `ruff` | 0.16.4 | 2026-08-27 | 0 | Lint and format, one tool. Resolved live with `uv pip compile` against PyPI. Dev dependency. |
| `pytest` | 9.1.1 | 2026-08-27 | 0 | Test runner behind `./m check`. Resolved live with `uv pip compile` against PyPI. Dev dependency. |
| `nbstripout` | 0.9.1 | 2026-08-27 | 1 | Strips notebook outputs on the way into the index (OPS-02, part 2.3). A credential or a data sample reaches a committed file through a cell's `outputs` array without appearing in any cell's source. Version read live from `https://pypi.org/pypi/nbstripout/json`. Dev dependency. |
| `tiktoken` | 0.14.0 | 2026-08-27 | 14 | 🔍 compare against the hand-rolled byte-level BPE (TOK-12). Chosen because it ships the published GPT split patterns and BPE ranks. Version read live from PyPI on 2026-08-27. |
| `tokenizers` | 0.23.1 | 2026-08-27 | 14 | 🔍 compare the four-stage pipeline — normalizer, pre-tokenizer, model, post-processor, decoder (TOK-13). Trains locally; no download. Version read live from PyPI on 2026-08-27. |
| `regex` | 2026.7.19 | 2026-08-27 | 14 | Transitive dependency of `tiktoken`. Also the module that supports `\p{L}` and possessive quantifiers, which Day 13 part 2.2 had to approximate with stdlib `re`. Not pinned directly; resolved by `uv`. |
| `sentencepiece` | 0.2.2 | 2026-08-27 | 15 | 🔍 compare the canonical Unigram/SentencePiece implementation against the hand-rolled Viterbi and against `tokenizers` (TOK-15). Version read live from PyPI on 2026-08-27; licence Apache-2.0 read from the installed distribution METADATA. |
