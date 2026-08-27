---
day: 14
phase: 2
phase_name: "Tokenization"
title: "Now compare — tiktoken, the tokenizers pipeline, and what production does that yours does not"
ids: ["TOK-12", "TOK-13"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18]
kind: tokenizer
plan_version: "v1.3.0"
parts: 14
compute_tier: T0
generated: "2026-08-27"
status: written
lab_scaffolded: false
commit: ""
---

# Day 14 — 🔍 Now compare

> You have built a tokenizer four times. Today you open the library, and the honest result is not the one
> you expect: your implementation is right, the library is faster, and the thing neither of you fixes is
> the one that matters most.

---

## §1 Where we are

Four days of building. Day 11 gave you character and word tokenizers and showed both are unusable — one
too long, one lossy. Day 12 built BPE's merge loop. Day 13 made it byte-level, gave it a real
pre-tokenizer, and proved zero out-of-vocabulary by construction.

Today is the first 🔍 **compare** day of the curriculum. Principle 3 says *build first, compare after*, and
the reason is now available to be tested rather than asserted: you can only tell what a library is doing
if you have done it yourself.

The result is worth stating before you start, because it is not the expected one.

**Your code is correct.** At an equal vocabulary size, a production Rust implementation lands within
**0.043%** of your token count on the same corpus — 46,291 against your 46,311. The four-day gap between
your tokenizer and `gpt2` is not code quality. It is 50× the vocabulary trained on thousands of times the
text.

**The library is faster, by about 10×** — and part of that is a bigger vocabulary rather than a faster
language, and 2.57× of it comes back the moment you call `encode_batch` instead of looping.

**The library gives you one real capability you do not have:** offsets. Every token knows the character
range it came from. That is what extractive tasks, highlighting and citation are built on, and your
tokenizer throws the information away at its first line.

**And the thing neither of you fixes** is that a vocabulary trained on English charges Hindi **6.88×** more
per character. Installing a library does not reduce that by one token.

Along the way today pays a debt: Day 13 could not run the published split pattern because the standard
library has no `\p{L}`, and left a `TODO` saying Day 14 would install `regex` and check. Part 1.2 checks.
The approximation was wrong in exactly two places out of 28,889.

**Today is also the first day this curriculum installs anything.** Two pinned packages, three downloaded
vocabulary files, and every one of them recorded in a ledger row *before* it was loaded. That ritual is
Principle 13, and it starts now.

---

## §2 The map

Fourteen parts across four sections. Section 1 is `tiktoken` and closes `TOK-12`; section 2 is the
`tokenizers` pipeline and closes `TOK-13`; section 3 is what remains after both; section 4 is the ledger.

### 01 — `tiktoken` (`TOK-12`)

| Part | Title | Level |
| --- | --- | --- |
| 1.1 | [The same corpus through both](parts/01-tiktoken/1.1-the-same-corpus-through-both.md) | working |
| 1.2 | [The published pattern, verbatim](parts/01-tiktoken/1.2-the-published-pattern-verbatim.md) | working |
| 1.3 | [What a vocabulary file looks like](parts/01-tiktoken/1.3-what-a-vocabulary-file-looks-like.md) | working |
| 1.4 | [Your merges against theirs](parts/01-tiktoken/1.4-your-merges-against-theirs.md) | working |
| 1.5 | 💥 [The special token that was just text](parts/01-tiktoken/1.5-the-special-token-that-was-just-text.md) | production |

### 02 — The `tokenizers` pipeline (`TOK-13`)

| Part | Title | Level |
| --- | --- | --- |
| 2.1 | [Five stages, not one](parts/02-the-tokenizers-pipeline/2.1-five-stages-not-one.md) | working |
| 2.2 | [The same vocabulary, trained twice](parts/02-the-tokenizers-pipeline/2.2-the-same-vocabulary-trained-twice.md) | working |
| 2.3 | [Offsets are the product](parts/02-the-tokenizers-pipeline/2.3-offsets-are-the-product.md) | production |
| 2.4 | [Padding, truncation and the mask](parts/02-the-tokenizers-pipeline/2.4-padding-truncation-and-the-mask.md) | production |
| 2.5 | 💥 [The normalizer that broke the round trip](parts/02-the-tokenizers-pipeline/2.5-the-normalizer-that-broke-the-round-trip.md) | production |

### 03 — The remaining gap

| Part | Title | Level |
| --- | --- | --- |
| 3.1 | [The file is the contract](parts/03-the-remaining-gap/3.1-the-file-is-the-contract.md) | production |
| 3.2 | [The tax a vocabulary charges a language](parts/03-the-remaining-gap/3.2-the-tax-a-vocabulary-charges-a-language.md) | production |
| 3.3 | 💥 [The mismatch the library will not catch](parts/03-the-remaining-gap/3.3-the-mismatch-the-library-will-not-catch.md) | production |

### 04 — Together

| Part | Title | Level |
| --- | --- | --- |
| 4.1 | [Six tokenizers, one table](parts/04-together/4.1-six-tokenizers-one-table.md) | production |

---

## §3 Setup — run this

Two packages, exact pins, both looked up live on PyPI on 2026-08-27 (Principle 6 — never invent a version).

```bash
uv add "tiktoken==0.14.0" "tokenizers==0.23.1"
uv run python -c "import tiktoken, tokenizers, regex; print(tiktoken.__version__, tokenizers.__version__, regex.__version__)"
```

Expected: `0.14.0 0.23.1 2026.7.19`. `regex` arrives as a transitive dependency of `tiktoken` and is the
module that finally makes part 1.2 possible.

**Before you run `tiktoken.get_encoding`, write the ledger rows.** The first call downloads vocabulary
files over the network. Principle 13 says the row goes in *before* the load, not after — §11 has all four
rows verbatim, with the SHA-256 hashes `tiktoken` itself verifies. Four rows, because this day loads three
encodings and `gpt2` alone needs two files.

These are text files — base64, JSON, space-separated pairs. Nothing in them executes, which is why
Principle 13 permits them where it forbids a pickle outright.

**If you have no network**, sections 2 and 3 still run in full: `tokenizers` trains locally and downloads
nothing. Only section 1 needs the fetch.

The corpus is `docs/00_MASTER_PLAN.md`, sha256 `9760f2b6d4340b97`, 113,283 bytes, 110,837 code points.
Every script prints the hash first. If yours differs, every number in this day is mine and not yours —
record your own and say so.

---

## §4 Build brief

You are not building a tokenizer today. You are building the **checks** that tell you when two tokenizers
disagree, and reading three real file formats closely enough to write your own on Day 16.

Work through the parts in order. In `lab/`, produce:

1. **The comparison script.** One `text` variable, six tokenizers, one table — part 4.1's table, with your
   numbers and your corpus hash.
2. **`assert_same_tokenizer(a, b, probes)`** from part 3.3. Ids against ids, never strings against strings.
   This function goes into `tests/` and stays there for the rest of the curriculum.
3. **A probe set** that is sensitive: a bare word, a leading space, a multi-byte character, a number, a run
   of whitespace, a special-token literal, and one non-English sentence.
4. **The multilingual rate table** from part 3.2, as four lines you can paste into any future tokenizer
   review.

Do **not** write anything into `akshara/` today. Day 16 is where the tokenizer becomes a committed module,
and it should be written knowing what these three file formats got right and wrong.

---

## §5 The eval that must be able to fail

`tests/test_tokenizer_compare.py`, CPU-only, deterministic, offline for everything except the section-1
fetch (mark those `@pytest.mark.gpu`-style skipped if you want a fully offline gate).

The tests that must go **red before green**:

| Change | Test that must fail |
| --- | --- |
| Rebuild the pre-tokenizer after loading the file (part 3.3) | `assert_same_tokenizer` — 4/4 probes |
| Compare with strings instead of ids | **nothing fails** — that is the finding, assert it |
| `pad_id=0` on a byte-level vocabulary (part 2.4) | `pad_id >= 256` |
| Drop the attention mask | mask must recover the original lengths exactly |
| Add an `NFKC` normalizer (part 2.5) | the round trip must go False |
| Run the tiling assertion on `café` (part 2.3) | must fail — and pass on ASCII |

Three of those assert that something **fails**. That is deliberate: each one pins the boundary of a
property rather than the property, and each one is the antidote to Silent Failure #5.

---

## §6 Compute budget

**Tier: T0 — laptop CPU. GPU-minutes: 0.**

| Step | Cost on this machine |
| --- | --- |
| `uv add` both packages | one-off, network |
| Download four vocabulary files (three encodings) | 6.8 MB total, one-off, cached |
| `tokenizers` train at `V = 1000` | **0.34 s** |
| Your Day 13 tokenizer, encode the corpus | 0.246 s (best of 5) |
| `tiktoken gpt2`, encode the corpus | 0.025 s (best of 5) |
| Day 12 char-level BPE train at `V = 1000` | 39.0 s — the longest step |
| First `get_encoding` call | 4.6–8.9 s, network-bound |

Nothing here needs a GPU and nothing here is close to a budget. The longest step is Day 12's Python
trainer, and part 4.1 needs it only once.

**The question this day cannot answer:** whether a vocabulary that compresses better produces a *better
model*. Every column in part 4.1's table is a proxy. Answering it properly costs a training run at each
vocabulary size, which is Day 17 (`TOK-20`) as far as arithmetic takes it, and beyond $0 to settle.

---

## §7 Traps

| # | Trap | Where |
| --- | --- | --- |
| 1 | Reading a three-variable comparison as one number — "libraries compress 39% better" | 1.1 |
| 2 | `[^\W\d_]` is *not* "a letter": `²` is category `No` and slips through | 1.2 |
| 3 | Shipping `encoder.json` without `vocab.bpe` — loads fine, tokenizes 4× longer | 1.3 |
| 4 | `#version: 0.2` counted as a merge — shifts every rank, rank 0 is the most powerful slot | 1.3, 1.4 |
| 5 | `encode` vs `encode_ordinary` — 9 ids or 4, one containing end-of-document | 1.5 |
| 6 | Assigning a pre-tokenizer and forgetting the decoder — `Ġ` leaks into user output | 2.1 |
| 7 | Comparing merge lists position-by-position after a tie — 651 false disagreements | 2.2 |
| 8 | Offsets are **character** offsets; and two tokens can share one span | 2.3 |
| 9 | `pad_id=0` on a byte-level vocabulary — id 0 is `!`, so `Hi` decodes as `Hi!` | 2.4 |
| 10 | Truncation leaves **no trace** in the attention mask | 2.4 |
| 11 | NFKC breaks `decode(encode(s)) == s` and nothing warns | 2.5 |
| 12 | Reconstructing any stage in code instead of loading it from the file | 3.1, 3.3 |
| 13 | "Zero out-of-vocabulary" read as "affordable in every language" | 3.2 |
| 14 | Relaxing a test (`.lstrip`) to make it pass — the relaxation *is* the bug report | 3.3 |

**The unifying trap, found five separate times today:** `decode(encode(s)) == s` passes on every one of
these bugs. It tests that *one* tokenizer is self-consistent. It cannot test that *two* agree.

---

## §8 Verify before you code

Principle 7 — never invent an API. Everything below was checked against the installed package on
2026-08-27, at the version pinned, and the day names what was checked.

| Symbol | How it was verified |
| --- | --- |
| `tiktoken.__version__`, `tokenizers.__version__`, `regex.__version__` | imported and printed: `0.14.0`, `0.23.1`, `2026.7.19` |
| `r50k_pat_str` | read from `tiktoken_ext/openai_public.py` via `inspect.getsource`, and cross-checked against the loaded encoder's `_pat_str` |
| download URLs and SHA-256 hashes | read from the same source file, **before** any load; recorded in `docs/MODELS.md` |
| `tiktoken.load.read_file_cached`, `check_hash` | source read; confirmed a bad *cache* re-fetches and a bad *download* raises |
| `encode` / `encode_ordinary` / `allowed_special` | the `ValueError` triggered deliberately and its text quoted verbatim |
| `BpeTrainer(vocab_size, initial_alphabet, show_progress)` | docstring read from the installed `tokenizers` |
| `pre_tokenizers.ByteLevel(add_prefix_space, use_regex, trim_offsets)` | printed from a live object |
| `Encoding.offsets`, `.word_ids`, `.attention_mask`, `.special_tokens_mask`, `.overflowing` | enumerated with `dir()` and each one exercised |
| `processors.TemplateProcessing(single, special_tokens)` | built and its output checked against `special_tokens_mask` |

Two honesty notes. `enc._pat_str` is a **private** attribute — used in part 1.2 because it is what the
loaded object actually uses, cited alongside the public source, and it does not belong in `akshara/`. And
possessive quantifiers `++` **do** work in the standard library on Python 3.12; the only thing that blocked
Day 13 was `\p{L}`. I expected otherwise and measured.

---

## §9 Say it in an interview

**"Why not just use `tiktoken`?"** You should. The point of building it four times is that you can now say
what it does: a rank-based encoder over a byte-level vocabulary with a published regex pre-tokenizer, no
merge list stored, specials declared in code. At an equal vocabulary size a hand-rolled Python version
lands within 0.043% on token count and about 10× behind on speed.

**"What is the difference between `tiktoken` and `tokenizers`?"** `tiktoken` is an inference-only encoder:
fast, no training, no offsets, ranks only. `tokenizers` is a five-stage configurable pipeline —
normalizer, pre-tokenizer, model, post-processor, decoder — that trains, carries offsets and serializes
every stage into one file. Choose the first to encode with a published vocabulary, the second to build one.

**"How do you know two tokenizers are the same?"** Compare **ids**, not strings, on probes chosen to be
sensitive — and better, compare the serialized configs. A round-trip test passes on every mismatch I know
of, because each tokenizer round-trips through its own configuration.

**"What is `add_prefix_space` and why does it matter?"** It prepends a space before splitting so a
string-initial word tokenizes like a mid-sentence one. It matters because it must match between training
and serving: flip it at serving time and 4 out of 4 probes produce different ids, with green round trips
and no error.

**"What does a tokenizer cost a non-English speaker?"** Measured: Hindi costs `gpt2` 6.88× more tokens per
character than English, `cl100k_base` 4.50×, `o200k_base` 1.25×. That is context window, compute — attention
is `O(T²)`, so 6.88× the tokens is roughly 47× the attention work — and money. It is decided by the
tokenizer's training corpus and cannot be changed without retraining the model.

**"What is Silent Failure #2?"** Tokenizer/template mismatch: training and inference use different text
pipelines. It is the default outcome, not a mistake, unless something structural prevents it — load every
stage from one file, hash that file, log the hash at both ends, and keep golden `(string, ids)` pairs in
CI.

---

## §10 Done when

- `CHECKLIST.md` is fully ticked.
- `./m depth 14` is green.
- Your own version of part 4.1's six-row table exists in `lab/`, with **your** corpus hash.
- `assert_same_tokenizer` exists, and you have watched it go red on the part 3.3 configuration.
- `docs/PACKAGES.md` has two rows; `docs/MODELS.md` has three; both were written **before** the load.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append verbatim, with your real commit sha:

```text
| 14 | 2026-08-27 | TOK-12, TOK-13 | 14 | T0 | <sha> | yes |
```

**`docs/PACKAGES.md`** — three rows, versions looked up live on PyPI on 2026-08-27:

```text
| `tiktoken` | 0.14.0 | 2026-08-27 | 14 | 🔍 compare against the hand-rolled byte-level BPE (TOK-12). Chosen because it ships the published GPT split patterns and BPE ranks. Version read live from PyPI on 2026-08-27. |
| `tokenizers` | 0.23.1 | 2026-08-27 | 14 | 🔍 compare the four-stage pipeline — normalizer, pre-tokenizer, model, post-processor, decoder (TOK-13). Trains locally; no download. Version read live from PyPI on 2026-08-27. |
| `regex` | 2026.7.19 | 2026-08-27 | 14 | Transitive dependency of `tiktoken`. Also the module that supports `\p{L}` and possessive quantifiers, which Day 13 part 2.2 had to approximate with stdlib `re`. Not pinned directly; resolved by `uv`. |
```

**`docs/MODELS.md`** — four rows, written **before** the first `get_encoding` call (Principle 13). Three
encodings, four files, because `gpt2` splits its merge list and its token→id map across two:

```text
| `gpt2` BPE ranks | `openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe` | sha256 `1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5` | MIT (via `tiktoken`) | text (`vocab.bpe`) | n/a — vocabulary only | 2026-08-27 | 14 | The published GPT-2 merge list, to compare against the one trained on Day 12. **Not a pickle** (P13); `tiktoken` verifies this hash on download. |
| `gpt2` encoder | `openaipublic.blob.core.windows.net/gpt-2/encodings/main/encoder.json` | sha256 `196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783` | MIT (via `tiktoken`) | JSON | n/a — vocabulary only | 2026-08-27 | 14 | The token→id table paired with the merge list above. |
| `cl100k_base` ranks | `openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken` | sha256 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` | MIT (via `tiktoken`) | text (`.tiktoken`) | n/a — vocabulary only | 2026-08-27 | 14 | A later, larger vocabulary with the three-digit number cap Day 13 part 2.4 quoted. |
| `o200k_base` ranks | `openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken` | sha256 `446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d` | MIT (via `tiktoken`) | text (`.tiktoken`) | n/a — vocabulary only | 2026-08-27 | 14 | The multilingual vocabulary part 3.2 measures the Hindi tax against. |
```

**`docs/DATASETS.md`** — no rows. The corpus is this repo's own plan.

**`docs/RUNS.md`** — no rows. Nothing was trained that produces weights.

**Commit:**

```text
day 014: 🔍 compare — tiktoken, the tokenizers pipeline, and the gap neither closes — closes TOK-12, TOK-13
```
