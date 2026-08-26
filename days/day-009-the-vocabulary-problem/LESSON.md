---
day: 9
phase: 2
phase_name: "Tokenization"
title: "The vocabulary problem — and what a tokenizer is for"
ids: ["TOK-01", "TOK-02"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 20]
kind: tokenizer
plan_version: "v1.3.0"
parts: 11
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 9 — The vocabulary problem, and what a tokenizer is for

> **Yesterday (Day 8):** gradient descent, the `2/L` boundary, momentum, Adam and AdamW — and the
> overfit-one-batch test that refuses to let a broken model be mistaken for a badly-tuned one.
> **Today:** the first day of the tokenizer phase. What the model's output list actually is, why the
> two obvious ways to fill it are both wrong, what a tokenizer is as an object, and the two failures
> that follow from getting either answer wrong.
> **Tomorrow (Day 10):** Unicode code points, normalization, and UTF-8 — the layer underneath every
> vocabulary in this phase (TOK-03, TOK-04).

---

## §1 Where we are

Eight days of mathematics have produced a model that consumes numbers and emits numbers. Today the
question is which numbers, and it turns out to be a design decision with a permanent, unrecoverable
consequence.

A language model's last layer produces one score per entry of a fixed list. Sampling picks one index
from that list. **That index is the output** — there is no mechanism by which a model can emit
anything else, in the same way there is no mechanism by which a die can roll a seven. So the list is
not a preprocessing detail on the way to the interesting part. It is the exact set of things the model
is capable of saying, chosen before training and unchangeable afterwards without surgery.

The two obvious ways to fill that list are both wrong, in opposite directions, and both wrongnesses
are measurable on a corpus already in this repository. Fill it with **words** and it never stops
growing: measured today, a single 109 KB document is still producing 395 unseen word types in its last
fifth, 35.7% of its types occur exactly once, and everything you cut becomes a token meaning "I cannot
represent this". Fill it with **characters** and nothing is ever unrepresentable — and the same text
becomes 5.60× longer, which is 31× the attention work and a context window that holds 183 words instead
of 1,024.

The answer the field arrived at is in between, and today builds a deliberately crude version of it
before Day 12 builds the real one. Then the day turns to the tokenizer as an *object*: two functions
and a table, sitting at both ends of the stack and nowhere in the middle, shipped as a separate
artefact from the weights, sized by an arithmetic that has three terms with three different scalings.

Two of the eleven parts are failures reproduced on purpose, and neither of them raises. In one, a
smaller vocabulary makes the reported loss **fall** by 18% while destroying 18% of the held-out text.
In the other, two tokenizers that pass every size check, every range check and every shape check in the
stack turn `'the quick brown fox'` into `'lbitparqwt sjyxtcjd'` — fluent, plausible, and about nothing.

Everything runs on the laptop, with no packages installed, against a corpus committed to this
repository. Every number below reproduces exactly for any reader.

---

## §2 The map

Eleven parts, three sections. Section 1 is TOK-01 — what goes in the list. Section 2 is TOK-02 — what a
tokenizer is and where it sits. Section 3 puts the day in one table. The day climbs
`foundation → working → production`, and each of the first two sections ends with something breaking.

### Section 1 — `01-the-vocabulary-problem`: TOK-01, what goes in the list

The vocabulary is a hard limit, not a convenience. This section rules out the two obvious answers with
measurements, builds the compromise, and then shows what the ruled-out answer costs when it is shipped
anyway.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A model can only emit what is in its vocabulary](parts/01-the-vocabulary-problem/1.1-a-model-can-only-emit-its-vocabulary.md) | Why is the vocabulary a permanent limit rather than a preprocessing choice? | `foundation` |
| 1.2 | [Why not words](parts/01-the-vocabulary-problem/1.2-why-not-words.md) | What stops a word vocabulary from ever being finished? | `working` |
| 1.3 | [Why not characters](parts/01-the-vocabulary-problem/1.3-why-not-characters.md) | If characters solve coverage completely, what do they cost? | `working` |
| 1.4 | [The subword compromise](parts/01-the-vocabulary-problem/1.4-the-subword-compromise.md) | What does the middle of the dial actually buy, slot by slot? | `working` |
| 1.5 | [💥 The vocabulary that could not spell](parts/01-the-vocabulary-problem/1.5-the-vocabulary-that-could-not-spell.md) | Why does destroying text make the reported loss go **down**? | `production` |

### Section 2 — `02-what-a-tokenizer-is`: TOK-02, the object and its place

A tokenizer is smaller than people expect and more load-bearing than people expect. Four parts on what
it is, where it lives, how it is versioned and how it is sized — then the mismatch that no check inside
the model can see.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [A function and its inverse](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md) | What is the one property that makes two functions a tokenizer? | `foundation` |
| 2.2 | [Where the tokenizer sits](parts/02-what-a-tokenizer-is/2.2-where-the-tokenizer-sits.md) | At which steps does a character exist, and at which does it not? | `working` |
| 2.3 | [The tokenizer is not part of the model](parts/02-what-a-tokenizer-is/2.3-the-tokenizer-is-not-part-of-the-model.md) | If neither artefact can validate the other, what binds them? | `production` |
| 2.4 | [Vocabulary size is a budget](parts/02-what-a-tokenizer-is/2.4-vocabulary-size-is-a-budget.md) | What exactly does one more vocabulary slot cost, and buy? | `production` |
| 2.5 | [💥 The tokenizer that did not match](parts/02-what-a-tokenizer-is/2.5-the-tokenizer-that-did-not-match.md) | Why do five reasonable checks all pass on a completely wrong output? | `production` |

### Section 3 — `03-together`: the day in one table

Three schemes, one paragraph, six columns — and the observation that five of those columns are trades
and one of them is a gate.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Three tokenizers, one table](parts/03-together/3.1-three-tokenizers-one-table.md) | Why does the scheme that wins no single column win the argument? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything in this day is the Python standard library — `collections`,
`pathlib`, `re`, `math`, `json`, `hashlib`, `random`. That is not an accident: a tokenizer is a
dictionary and two comprehensions, and installing something to do it would hide exactly the thing
today is about (Principle 3).

```bash
uv run python -c "import sys, collections, hashlib; print('python', sys.version.split()[0])"
./m scaffold 9
```

The corpus for every measurement today is `docs/00_MASTER_PLAN.md`, at the revision in this repository.
It is used because it is committed, so **every figure in this day reproduces exactly** rather than
approximately — and because it is genuinely mixed content: English prose, code fences, tables, box
drawing, Devanagari and emoji, which is what makes the coverage failures visible at all.

Two conventions are in play and the parts say which they use, because mixing them silently is how
tokenizer comparisons go wrong:

- **Whitespace tokens** — `text.split()` — used by parts 1.3, 1.4, 2.4 and 3.1. Gives 19,475 tokens and
  109,060 characters.
- **Lowercased alphabetic runs** — `re.findall(r"[A-Za-z']+", text)` lowercased — used by parts 1.2 and
  1.5. Gives 14,798 tokens and 2,376 types.

Nothing from Days 2–8 is required to run today's code. Day 5's distribution-over-a-vocabulary and Day
6's `ln(V)` loss floor are *referenced* constantly, and rereading Day 5 part 1.1 before starting is
worth the two minutes.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-009-the-vocabulary-problem/lab/vocab.py` | [1.2](parts/01-the-vocabulary-problem/1.2-why-not-words.md), [1.3](parts/01-the-vocabulary-problem/1.3-why-not-characters.md), [1.4](parts/01-the-vocabulary-problem/1.4-the-subword-compromise.md) | `word_types`, `char_types`, `keep_top_n` returning `(V, T)` — **`sorted` everywhere a set becomes an order** |
| `days/day-009-the-vocabulary-problem/lab/tokenizer.py` | [2.1](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md) | `CharTokenizer` with `from_text`, `encode`, `decode`, `save`, `load` — and a `sha256` property |
| `days/day-009-the-vocabulary-problem/lab/budget.py` | [2.4](parts/02-what-a-tokenizer-is/2.4-vocabulary-size-is-a-budget.md) | `vocab_budget(V, C, tied)` → params, MiB, `ln(V)`; `loss_in_context` |
| `days/day-009-the-vocabulary-problem/lab/compare.py` | [3.1](parts/03-together/3.1-three-tokenizers-one-table.md) | `compare(text, schemes)` — every row measured on **one** text by construction |
| `tests/test_tokenizer.py` | [2.1](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md), [2.5](parts/02-what-a-tokenizer-is/2.5-the-tokenizer-that-did-not-match.md), [3.1](parts/03-together/3.1-three-tokenizers-one-table.md) | the round-trip test, the mismatch test, the four invariants |

Nothing under `akshara/` today. Day 11 is where the tokenizer becomes a package module; today it lives
in `lab/`, because the version written here is a stand-in that Day 12 replaces.

**`TODO(me)`:** part [1.4](parts/01-the-vocabulary-problem/1.4-the-subword-compromise.md) ranks
candidate pieces by raw word frequency, which never discovers a suffix like `ing`. Write down, in one
paragraph, what you would rank by instead — before reading Day 12.

---

## §5 The eval that must be able to fail

Three checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_tokenizer.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| add `.lower()` to `encode` | output still readable, `decode(encode(s)) != s` | the round-trip test |
| build the vocabulary with `list(set(text))` instead of `sorted(...)` | same `V`, same characters, different ids, fluent wrong text | the mismatch test |
| add `+1` for the space **and** count spaces as characters | `T` exceeds the character count | the invariant test |

The second row is the day's centrepiece, and it is worth breaking by hand rather than reading about.
Encoding `'the quick brown fox'` with one table and decoding with the other gives
`'lbitparqwt sjyxtcjd'` — the right length, lower-case Latin, containing a space. **Five separate
checks pass on that output**: same `V`, same character set, ids in range, same output length, every
character printable.

The first row is the one that will actually happen to you. `.lower()` in an `encode` is added for a
good reason roughly once per project, and it silently removes capital letters from the model's universe
with no error and perfectly readable output.

---

## §6 Compute budget

**Tier: T0.** Python's standard library on a laptop CPU, over a 109 KB file committed to this
repository.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed, nothing downloaded |
| Disk | negligible; the largest artefact written is a 1,540-byte vocabulary file |

What T0 proves: **every claim in this day.** The vocabulary growth curve, the 35.7% hapax rate, the
5.60× length ratio, the 31.4× attention multiplier, the keep-top-N curve, the round-trip result, the
`2VC` parameter arithmetic and the mismatch output are all exact counts or exact multiplications over a
committed file. There is no seed, no hardware dependence and no benchmark anywhere in this day — run it
on any conforming machine and the numbers are identical.

What T0 **cannot** show is the one thing that matters most and is not measurable by counting: whether a
subword vocabulary produces a *better model* at fixed compute. That needs training runs, it is Day 17,
and no amount of counting substitutes for it. What today settles is which schemes are worth spending a
run on — and that word-level is not, for a reason that is a correctness property rather than a
performance one.

One number in part [1.5](parts/01-the-vocabulary-problem/1.5-the-vocabulary-that-could-not-spell.md)
deserves its label read carefully. The `5.6437` nats figure is the loss of an **explicitly described,
deliberately stupid model** — one that predicts `<unk>` perfectly and everything else at chance —
computed as arithmetic. It is not the result of a training run and the part says so. It establishes the
*direction* of the bias, which is the claim being made.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| A vocabulary built from `set()` without `sorted` | two runs, same characters, different ids, no error anywhere | [2.1](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md), [2.5](parts/02-what-a-tokenizer-is/2.5-the-tokenizer-that-did-not-match.md) |
| `.lower()` or `.strip()` inside `encode` | perfectly readable output that is not the input | [2.1](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md) |
| An `encode` that skips characters it does not know | a shorter list, no exception, information gone | [2.1](parts/02-what-a-tokenizer-is/2.1-a-function-and-its-inverse.md) |
| Shrinking `V` and reading the loss as an improvement | loss falls 18%, held-out text 18% destroyed | [1.5](parts/01-the-vocabulary-problem/1.5-the-vocabulary-that-could-not-spell.md) |
| Comparing losses across two tokenizations | two floors, `5.011` and `8.613`, and the wrong ordering | [2.4](parts/02-what-a-tokenizer-is/2.4-vocabulary-size-is-a-budget.md) |
| Quoting a compression ratio measured on your training text | `4.67` chars/token on familiar English, `0.89` on Devanagari | [1.4](parts/01-the-vocabulary-problem/1.4-the-subword-compromise.md) |
| Shipping weights without the tokenizer | loads cleanly, runs forever, output is subtly wrong | [2.3](parts/02-what-a-tokenizer-is/2.3-the-tokenizer-is-not-part-of-the-model.md) |
| Round-tripping through one tokenizer object | a test that cannot fail | [2.5](parts/02-what-a-tokenizer-is/2.5-the-tokenizer-that-did-not-match.md) |

Two of the plan's five silent failures are live today. **#2, tokenizer/template mismatch**, is part
2.5's entire subject, and the check the plan prescribes — round-trip the exact training string through
the inference path and `assert` equality — is written there as a function. **#4, noise mistaken for
improvement**, is part 1.5 in a different costume: a metric that moves in the right direction for a
reason that is not learning.

---

## §8 Verify before you code

Every library symbol used today is standard library, and the ones worth checking against the
documentation for **Python 3.12.12**, the version actually running here, are these:

| Symbol | What was checked | Why it matters today |
| --- | --- | --- |
| `set` iteration order | the language reference does not define it | the reason `sorted` is not optional — part 2.5 |
| `collections.Counter.most_common(n)` | returns the `n` most common, ties broken by insertion order | ties are why two "identical" vocabularies can differ |
| `json.dumps(..., sort_keys=True)` | sorts by key, producing stable bytes | the reason a vocabulary hash is reproducible — part 2.3 |
| `hashlib.sha256` | hashes bytes, not `str` | the hash must be over the file's bytes, not the object |
| `str.split()` with no argument | splits on runs of whitespace and discards empty strings | why 19,475 differs from a naive `split(" ")` |

Read the `set` line again before writing any vocabulary code. Iteration order not being part of the
contract is the whole of part 2.5, and it is the kind of fact that is obvious once stated and invisible
until it costs a week.

---

## §9 Say it in an interview

*"Why not just tokenize on words?"* — "Because the vocabulary never converges. On a single 109 KB
document I measured 395 new word types appearing in the last fifth, 35.7% of types occurring exactly
once, and 8.89% of held-out tokens outside an *uncapped* vocabulary built from the other 80% of the
same file. And whatever you cut becomes `<unk>`, which is not a degraded word — it is the absence of a
word, and a word-level model cannot spell its way out because there is no smaller unit to fall back to."

*"So why not characters?"* — "Coverage is perfect and the sequence is 5.60× longer on English, which is
31× the attention work, and a 1,024-token context holds 183 words instead of 1,024. That last one is a
capability question, not a speed question."

*"You shrank the vocabulary and validation loss improved. Ship it?"* — "Not until I see the fallback
rate on the eval set in both runs. `<unk>` is a frequent, easy token, so pushing text into it lowers
the average surprise while making the model strictly worse. Measured on a real corpus, an 18% `<unk>`
rate buys an 18% reduction in the uniform baseline on its own. And the two runs have different `ln(V)`
floors, so their losses are not comparable anyway — per character or per byte is the comparable
quantity."

*"A deployed model starts producing fluent text unrelated to the prompt. Where do you look?"* — "The
tokenizer, not the model. A broken model produces broken text; a mismatched tokenizer produces good
text about the wrong input. Nothing inside the model can catch it, because every id is in range and
every shape matches — I have the measured example where five separate checks pass on
`'lbitparqwt sjyxtcjd'`. The two fixes are a tokenizer hash checked at load, and a real training string
round-tripped through the serving path — and the root cause is usually a vocabulary built without
`sorted`."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 9` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 9 | 2026-08-26 | TOK-01, TOK-02 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; everything used is the standard library.

`docs/DATASETS.md` — **no rows today**, and it is worth being precise about why. Every measurement in
this day is over `docs/00_MASTER_PLAN.md`, which is a file in this repository under this repository's
own licence. It is not a dataset, it was not downloaded, and giving it a `DATASETS.md` row would make
the ledger less useful rather than more. **The first `DATASETS.md` row is Day 14's**, when a real
corpus is fetched and its licence and revision SHA go in the ledger *before* the download.

`docs/MODELS.md` — **no rows today.** Nothing was downloaded and nothing was loaded.

`docs/RUNS.md` — **no rows today.** Nothing today trains, and the `5.6437` figure in part 1.5 is
labelled arithmetic rather than a run for exactly this reason.

Commit:

```text
day 009: The vocabulary problem and what a tokenizer is for — closes TOK-01, TOK-02
```
