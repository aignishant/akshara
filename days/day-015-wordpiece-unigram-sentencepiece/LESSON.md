---
day: 15
phase: 2
phase_name: "Tokenization"
title: "The other families — WordPiece, Unigram and SentencePiece; a probabilistic vocabulary"
ids: ["TOK-14", "TOK-15"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18]
kind: tokenizer
plan_version: "v1.3.0"
parts: 13
compute_tier: T0
generated: "2026-08-27"
status: written
lab_scaffolded: false
commit: ""
---

# Day 15 — The other families

> BPE is one answer to one question. Today you meet the other two, and they disagree about almost
> everything: how to score a merge, how to encode a word, what to do with a character you have never seen,
> and whether a tokenizer is a function at all.

---

## §1 Where we are

Four days built BPE and one day compared it. Every tokenizer so far has shared a shape: an ordered merge
list, applied by rank, over a byte-level alphabet.

Today that shape stops being the only one. Two more families arrive, and each disagrees with BPE about
something fundamental.

**WordPiece** changes one line of Day 12's trainer — maximize `count(ab)/(count(a)×count(b))` instead of
`count(ab)` — and abandons the merge list at encode time entirely, walking the word greedily instead. The
measured consequence is severe: `café` becomes a single `[UNK]` that decodes to the **empty string**, and
the unknown rate on the training corpus is **0.000%**, which is why nobody notices.

**Unigram** runs the whole thing backwards. It starts with **56,957** candidate substrings and prunes 98.2%
of them, and every surviving token carries a **log probability**. That turns encoding into a search: 8
valid segmentations of `▁dollars`, and Viterbi returns the argmax, **201,000×** more likely than the worst.

**And because there are probabilities, they can be sampled.** Subword regularization deliberately makes the
tokenizer non-deterministic — at which point `assert_same_tokenizer(ug, ug)`, the check Day 14 built,
**fails against the tokenizer itself**.

Two hand-rolled implementations, twenty lines each, agree with the Rust library **7/7** and **6/6**.
Principle 3 pays out twice.

The day ends where the week has been heading: a nine-row table with **two** veto columns, in which exactly
three tokenizers are both lossless and complete, and all three represent text as bytes somewhere.

---

## §2 The map

Thirteen parts across four sections. Section 1 closes `TOK-14`; sections 2 and 3 close `TOK-15`; section 4
is the ledger.

### 01 — WordPiece (`TOK-14`)

| Part | Title | Level |
| --- | --- | --- |
| 1.1 | [Scoring a pair by likelihood](parts/01-wordpiece/1.1-scoring-a-pair-by-likelihood.md) | working |
| 1.2 | [The `##` convention](parts/01-wordpiece/1.2-the-hash-hash-convention.md) | working |
| 1.3 | [Greedy longest-match-first](parts/01-wordpiece/1.3-greedy-longest-match-first.md) | working |
| 1.4 | 💥 [The word that became one `[UNK]`](parts/01-wordpiece/1.4-the-word-that-became-one-unk.md) | production |

### 02 — Unigram (`TOK-15`)

| Part | Title | Level |
| --- | --- | --- |
| 2.1 | [Start big and prune](parts/02-unigram/2.1-start-big-and-prune.md) | working |
| 2.2 | [Every token carries a probability](parts/02-unigram/2.2-every-token-carries-a-probability.md) | working |
| 2.3 | [Viterbi picks the best segmentation](parts/02-unigram/2.3-viterbi-picks-the-best-segmentation.md) | working |
| 2.4 | [Subword regularization](parts/02-unigram/2.4-subword-regularization.md) | production |
| 2.5 | 💥 [The tokenizer that disagreed with itself](parts/02-unigram/2.5-the-tokenizer-that-disagreed-with-itself.md) | production |

### 03 — SentencePiece (`TOK-15`)

| Part | Title | Level |
| --- | --- | --- |
| 3.1 | [The metaspace trick](parts/03-sentencepiece/3.1-the-metaspace-trick.md) | working |
| 3.2 | [Byte fallback](parts/03-sentencepiece/3.2-byte-fallback.md) | production |
| 3.3 | 💥 [The normalizer that was already on](parts/03-sentencepiece/3.3-the-normalizer-that-was-already-on.md) | production |

### 04 — Together

| Part | Title | Level |
| --- | --- | --- |
| 4.1 | [Nine tokenizers, one table](parts/04-together/4.1-nine-tokenizers-one-table.md) | production |

---

## §3 Setup — run this

Sections 1 and 2 need only `tokenizers==0.23.1`, already pinned on Day 14. Section 3 adds one package,
version looked up live on PyPI on 2026-08-27 (Principle 6):

```bash
uv add "sentencepiece==0.2.2"
uv run python -c "import sentencepiece as spm, tokenizers; print(spm.__version__, tokenizers.__version__)"
```

Expected: `0.2.2 0.23.1`.

**Licence, read from the installed distribution rather than recalled:**

```bash
grep -i "^license" .venv/Lib/site-packages/sentencepiece-0.2.2.dist-info/METADATA
```

Expected: `License-Expression: Apache-2.0`. That is where §11's `docs/PACKAGES.md` row gets its licence
field — PyPI's JSON API returns `null` for it, so the distribution metadata is the source.

**Nothing is downloaded today.** No `docs/MODELS.md` rows: every vocabulary in this day is trained locally
from the repo's own plan. Day 14 downloaded four files; today downloads none, and the absence is worth
confirming rather than assuming.

The corpus is `docs/00_MASTER_PLAN.md`, sha256 `9760f2b6d4340b97`, 113,283 bytes, 110,837 code points.
Every script prints the hash first.

---

## §4 Build brief

Principle 3, twice. Both algorithms are hand-rolled in about twenty lines each **before** the library is
opened, and both are checked against it.

In `lab/`, produce:

1. **`wordpiece_encode(word, vocab, unk)`** — greedy longest-match-first, part 1.3. Must agree with
   `tokenizers` on your probe set. Mine agreed 7/7.
2. **`viterbi(word, logp)`** — the dynamic program, part 2.3. Must agree with the library **and** with a
   brute-force enumeration of every segmentation. Mine agreed 6/6.
3. **The OOV probe set** — words your corpus does not contain, in more than one script. This is the
   measurement Day 14's table lacked and part 4.1's second veto column needs.
4. **The nine-row table** from part 4.1, with your numbers and your corpus hash.

Do **not** write anything into `akshara/`. Day 16 is where the tokenizer becomes a committed module, and it
should be written knowing what all three families get right and wrong.

---

## §5 The eval that must be able to fail

`tests/test_tokenizer_families.py`, CPU-only, deterministic, offline.

| Change | Test that must fail |
| --- | --- |
| Drop `min_frequency` from the WordPiece score (part 1.1) | the chosen pair has count 1, not 1,233 |
| Shuffle a WordPiece vocabulary (part 1.3) | **nothing fails** — assert that, it is the finding |
| Shuffle a BPE merge list | ids change — the contrast that gives the above meaning |
| Multiply probabilities instead of adding logs (part 2.2) | 200 terms underflow to exactly `0.0` |
| Leave `<unk>` in the Viterbi table (part 2.3) | **nothing fails** — assert the non-effect and say why |
| Enable `alpha`/`nbest_size` (part 2.5) | `assert_same_tokenizer(t, t)` fails against itself |
| Encode `café` under WordPiece (part 1.4) | decodes to `''`, not to a placeholder |
| Run the whitespace probes under Metaspace (part 3.1) | a tab and a leading space are still lost |
| Train SentencePiece with defaults (part 3.3) | 1,646 newlines destroyed |

**Five of those assert that something does *not* happen.** By now that should feel like the normal shape of
a test rather than a curiosity: a property is only pinned when you have pinned its boundary too.

---

## §6 Compute budget

**Tier: T0 — laptop CPU. GPU-minutes: 0.**

| Step | Cost on this machine |
| --- | --- |
| `uv add sentencepiece` | one-off, 1.2 MiB download |
| WordPiece train, `V = 1000` | 0.2 s |
| Unigram train, `V = 1000` | 1.0 s |
| Unigram train, `V = 300` / `V = 3000` | 1.4 s / 0.7 s — **falling with `V`** |
| SentencePiece train, `V = 1000` | ~1.1 s |
| Day 12 char-level BPE train, for part 4.1's row 3 | **39.0 s** — the longest step |
| 400 sampled encodings (part 2.4) | under a second |

The longest step is Day 12's Python trainer, needed once for one row of the closing table. Everything new
today trains in about a second, because it is all Rust or C++.

**The question this day cannot answer:** whether subword regularization improves a *model*. arXiv:1804.10959
reports BLEU gains on translation; this day trains no model and measuring it here would cost a training run
per configuration. What is measured is the cost side: **42% more tokens** at `alpha = 0.1`.

---

## §7 Traps

| # | Trap | Where |
| --- | --- | --- |
| 1 | The likelihood score with no `min_frequency` picks a pair seen **once** | 1.1 |
| 2 | `##` collides with markdown — 158 `#` characters destroyed on this corpus | 1.2, 1.4 |
| 3 | `[UNK]` takes the **whole word**, and decodes to `''` | 1.4 |
| 4 | An unknown rate of 0.000% measured on the corpus that trained the vocabulary | 1.4 |
| 5 | `max_input_chars_per_word` turns a 101-character token into one `[UNK]`, silently | 1.3 |
| 6 | `.tokens` shows `'é'` while the id is `0` = `<unk>` — **the string lies** | 2.1 |
| 7 | `<unk>` scores `0.0`, the maximum — inert in Viterbi, wrong by 1.0 in a mass sum | 2.2, 2.3 |
| 8 | Multiplying probabilities underflows to `0.0`; every segmentation then ties | 2.2, 2.3 |
| 9 | Sampling left on at inference — it travels in the saved file | 2.4 |
| 10 | `Metaspace` loses a **tab** and one **leading space**, invisibly on this corpus | 3.1 |
| 11 | `DecodePieces` round-trips where `Decode(ids)` does not — the same lie as #6 | 3.2 |
| 12 | Byte fallback **costs** 11.2% compression; it is not a free improvement | 3.2 |
| 13 | SentencePiece normalizes **by default** — 1,646 newlines, `²`, `…` gone | 3.3 |
| 14 | `remove_extra_whitespace` is not a field; the plural is | 3.3 |

**The unifying trap, met three separate times today:** a token *string* misreports an unknown, and only the
**id** is truthful. Day 14 said "compare ids, not strings" about two tokenizers; today it turns out to
apply within one.

---

## §8 Verify before you code

Principle 7. Everything below checked against the installed package on 2026-08-27, at the version pinned.

| Symbol | How it was verified |
| --- | --- |
| `sentencepiece.__version__` | imported and printed: `0.2.2` |
| `sentencepiece` licence | `License-Expression: Apache-2.0` read from the installed `METADATA` — PyPI's JSON returns `null` |
| `models.WordPiece(unk_token=, max_input_chars_per_word=)` | docstring read from the installed `tokenizers` |
| `models.Unigram`, `.alpha`, `.nbest_size` | enumerated with `dir()`, then exercised |
| `trainers.UnigramTrainer(shrinking_factor=, n_sub_iterations=, max_piece_length=)` | docstring read |
| `pre_tokenizers.Metaspace(replacement=, prepend_scheme=, split=)` | printed from a live object |
| `SentencePieceTrainer.train(byte_fallback=, normalization_rule_name=, add_dummy_prefix=)` | each accepted by the trainer |
| `remove_extra_whitespaces` | **probed**: the singular raises `NOT_FOUND: unknown field name`, the plural is accepted |
| `SentencePieceProcessor.Decode` vs `.DecodePieces` | both run on the same input; they disagree, and the difference is part 3.2 |

Two honesty notes. **`remove_extra_whitespace` (singular) does not exist** — I wrote it first, the trainer
refused it by name, and the plural is correct. And the `sentencepiece` docstring for `train` is empty, so
its arguments were verified by calling them rather than by reading; a field that does not exist raises
immediately, which makes probing a legitimate verification method here.

---

## §9 Say it in an interview

**"What is the difference between BPE and WordPiece?"** One line in the trainer — BPE maximizes
`count(ab)`, WordPiece maximizes `count(ab)/(count(a)×count(b))` — and a completely different encoder. BPE
replays an ordered merge list; WordPiece walks the word greedily against an unordered vocabulary, so its
file can be edited and its merge order does not exist. The likelihood rule needs a `min_frequency` guard or
it picks pairs seen once.

**"What makes Unigram probabilistic?"** Every token carries a log probability, so a segmentation has a
score and encoding is an argmax found by Viterbi rather than a rule. Measured: `▁dollars` has 8
segmentations and the best is 201,000× more likely than the worst. It also means you can *sample*, which is
subword regularization.

**"What is SentencePiece?"** Packaging, not an algorithm — usually Unigram underneath. Its contributions
are the `▁` metaspace substitution, so whitespace is data rather than a delimiter, and byte fallback, so
any character is representable. Its default normalizer is `nmt_nfkc`, which destroys newlines.

**"How would you choose a tokenizer?"** Two vetoes before any other column. Is it lossless on my corpus?
Can it represent text it has never seen? Compression only breaks ties among the survivors. Measured on one
corpus, nine tokenizers: six lossless, four complete, three both — and all three of those represent text as
bytes somewhere.

**"What does `byte_fallback` cost?"** 256 vocabulary slots and, measured at `V = 1000`, 11.2% more tokens.
At `V = 32000` the slots are 0.8% of the budget and the cost largely disappears, which is why it is
standard in production and looks expensive at toy scale.

**"When is a tokenizer not a function?"** When subword regularization is on. Same object, same string, 50
calls, ~40 distinct id sequences — every one round-tripping. Determinism is a configuration, and any test
comparing ids must state that it assumes it.

---

## §10 Done when

- `CHECKLIST.md` is fully ticked.
- `./m depth 15` is green.
- Your `wordpiece_encode` and `viterbi` both agree with the library on your own probes.
- Your nine-row table exists in `lab/`, with **your** corpus hash.
- You have watched `assert_same_tokenizer(t, t)` fail, and can say why that is not a bug.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append verbatim, with your real commit sha:

```text
| 15 | 2026-08-27 | TOK-14, TOK-15 | 13 | T0 | <sha> | yes |
```

**`docs/PACKAGES.md`** — one row:

```text
| `sentencepiece` | 0.2.2 | 2026-08-27 | 15 | 🔍 compare the canonical Unigram/SentencePiece implementation against the hand-rolled Viterbi and against `tokenizers` (TOK-15). Version read live from PyPI on 2026-08-27; licence Apache-2.0 read from the installed distribution METADATA. |
```

**`docs/MODELS.md`** — **no rows.** Every vocabulary today is trained locally; nothing is downloaded.

**`docs/DATASETS.md`** — no rows. The corpus is this repo's own plan.

**`docs/RUNS.md`** — no rows. Nothing was trained that produces weights.

**Commit:**

```text
day 015: the other families — WordPiece, Unigram and SentencePiece — closes TOK-14, TOK-15
```
