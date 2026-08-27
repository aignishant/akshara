---
day: 12
phase: 2
phase_name: "Tokenization"
title: "BPE from scratch I — the merge loop, by hand and then trained"
ids: ["TOK-07", "TOK-08"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18]
kind: tokenizer
plan_version: "v1.3.0"
parts: 11
compute_tier: T0
generated: "2026-08-27"
status: written
lab_scaffolded: false
commit: ""
---

# Day 12 — BPE from scratch I

> **Yesterday (Day 11):** both obvious tokenizers, built and broken. The character one is lossless and
> 5.56× too long; the word one is compact and cannot represent 10.41% of held-out text with nothing
> underneath to fall back on.
> **Today:** the algorithm that sits between them. One rule — merge the commonest adjacent pair — run by
> hand on twelve words, then trained on the whole corpus, then read.
> **Tomorrow (Day 13):** BPE II — encode and decode properly, the regex pre-tokenizer, and the byte
> alphabet that closes the last gate (TOK-09, TOK-10, TOK-11).

---

## §1 Where we are

Day 11 ended with a scoreboard: three trades, two gates, and the observation that one of the two gates
had a handle on it. Today closes every trade and one of the gates, with an algorithm you can run on paper.

The rule is four lines long. Count every adjacent pair of symbols in the corpus, take the commonest, glue
it into one new symbol, repeat. Nothing in it knows about language. Run it six times on twelve words and
**merge 4 produces `est`** — a real English suffix, discovered by counting. Run it 349 times on the corpus
and merge 18 is `ing`, merge 23 is `ion`, merge 12 is ` the`. Day 11 part 2.4 asked what you would have to
count to find `ing` without a suffix list; the answer is pairs, not words.

The trades go first. At `V = 1000` — the same vocabulary size as Day 11's word tokenizer — BPE encodes the
corpus in 42,130 tokens against the character tokenizer's 110,837: **2.63 characters per token against
1.00**, which is 62% of the sequence-length problem gone for the same number of slots.

Then the gate. Day 11's word tokenizer emitted `the tokenizer <unk> its vocabulary and cannot <unk>
anything <unk>` and **no id sequence in it could ever produce the word `spell`**. BPE at a *smaller*
vocabulary encodes the same sentence exactly, spelling `memorises` as `mem` + `or` + `is` + `es`, because
when no learned piece fits the alphabet is underneath. Thirteen extra tokens buys three words and the
ability to say them.

And then the honest half. **BPE does nothing for coverage.** The trained tokenizer is still missing 6 of
6 Cyrillic characters, because merges combine symbols and never add one. The alphabet came from the
corpus on Day 11 and it still does. That is tomorrow's one-line change.

Two of the eleven parts are failures reproduced on purpose. In one, removing the pre-tokenizer makes **16
of the first 60 merges** glue a word's ending to the gap after it — tokens like `'e '` and `', '` — and
the tokenizer that results compresses *slightly better* while making a word's tokenization depend on what
follows it. In the other, training on the same words in a different order produces merge lists that
**diverge at merge 24**, because a tie was broken by whichever pair a `Counter` happened to see first.

Everything runs on the laptop. The longest single step is 50.8 seconds. Every script prints the corpus
sha256 first, so a reader whose numbers differ knows immediately why.

---

## §2 The map

Eleven parts, three sections. Section 1 is TOK-07 — the merge rule itself, by hand and then in a loop.
Section 2 is TOK-08 — training as something that produces an artifact you can read, hash and mis-handle.
Section 3 puts three tokenizers in one table. The day climbs `foundation → working → production` and each
of the first two sections ends with something breaking.

### Section 1 — `01-the-merge-loop`: TOK-07, one rule

The algorithm, small enough to check by hand, then wrapped in a loop with the boundary it must not cross.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [Merge the commonest pair](parts/01-the-merge-loop/1.1-merge-the-commonest-pair.md) | What is the rule, and why does an unseen word stop being a problem? | `foundation` |
| 1.2 | [Six merges, by hand](parts/01-the-merge-loop/1.2-six-merges-by-hand.md) | How does an algorithm that only merges pairs produce long tokens? | `working` |
| 1.3 | [The loop, and where it stops](parts/01-the-merge-loop/1.3-the-loop-and-where-it-stops.md) | What does BPE become if you never stop it? | `working` |
| 1.4 | [The pre-tokenizer](parts/01-the-merge-loop/1.4-the-pre-tokenizer.md) | Where are merges not allowed to reach, and why is the tokenizer lossless again? | `working` |
| 1.5 | [💥 The merge that ate the space](parts/01-the-merge-loop/1.5-the-merge-that-ate-the-space.md) | Why does the worse tokenizer compress better? | `production` |

### Section 2 — `02-training-a-vocabulary`: TOK-08, the learned artifact

The merge list as a file with a hash, the target size as the only knob, the list as a document you read,
what it costs, and the way two identical runs stop being identical.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [The merge table is the artifact](parts/02-training-a-vocabulary/2.1-the-merge-table-is-the-artifact.md) | Why can you not store the merges in a set? | `foundation` |
| 2.2 | [Training to a target size](parts/02-training-a-vocabulary/2.2-training-to-a-target-size.md) | What does each doubling of `V` actually buy? | `working` |
| 2.3 | [Reading the table](parts/02-training-a-vocabulary/2.3-reading-the-table.md) | What can you learn about a corpus from its merge list alone? | `working` |
| 2.4 | [What training costs](parts/02-training-a-vocabulary/2.4-what-training-costs.md) | Why is a library thousands of times faster without being cleverer? | `production` |
| 2.5 | [💥 The vocabulary that depended on the order of the corpus](parts/02-training-a-vocabulary/2.5-the-vocabulary-that-depended-on-the-order-of-the-corpus.md) | Where is the nondeterminism in an algorithm with no random numbers? | `production` |

### Section 3 — `03-together`: the scoreboard

Day 11's five findings, checked off — four closed and one still open.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Three tokenizers, one table](parts/03-together/3.1-three-tokenizers-one-table.md) | What did BPE actually fix, and what did it leave exactly as it was? | `production` |

---

## §3 Setup — run this

**No new packages today.** `re`, `collections`, `json`, `hashlib`, `time`, `random`, `pathlib`. Principle
3 is the point of the whole day: the hand-rolled BPE exists before any library is opened, and Day 14 is
where the library arrives.

```bash
uv run python -c "import sys; print('python', sys.version.split()[0])"
uv run python -c "import hashlib, pathlib; print('corpus sha256[:16]', hashlib.sha256(pathlib.Path('docs/00_MASTER_PLAN.md').read_bytes()).hexdigest()[:16])"
./m scaffold 12
```

**Compare that hash against `9760f2b6d4340b97`.** Every measurement in this day is over
`docs/00_MASTER_PLAN.md` at one revision. A different hash means your corpus is a different corpus and
your numbers are the correct ones for it — the merge list especially, which is the output that changes
most visibly when the corpus does.

One thing to know before you start, because it affects how you work: **training is slow.** The trainer in
this day recounts every pair after every merge, so `V = 2000` takes 50.8 seconds on the hardware this was
written on. That is deliberate — part 2.4 is about why and what a real implementation does instead — but
it means you should train once and reuse the result rather than retraining inside a loop.

Two conventions carried forward from Day 11 and Day 10:

- **Every token is printed with `ascii()`.** A merge list is full of tokens made of spaces and newlines,
  and ` the` against `the` is the distinction the list is most useful for. Part 1.5's failure is invisible
  without it.
- **Every regular expression is a raw string.** `r"\s*\S+|\s+"`, never `"\s*\S+|\s+"`.

Day 11 parts 2.4 and 2.5 and Day 9 part 2.5 are referenced throughout. Rereading Day 11 part 2.5 — the
sentence the word tokenizer could not say — before starting is worth it, because part 3.1 encodes the same
sentence and the comparison is the day's payoff.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `akshara/tokenizer/bpe.py` | [1.1](parts/01-the-merge-loop/1.1-merge-the-commonest-pair.md), [1.3](parts/01-the-merge-loop/1.3-the-loop-and-where-it-stops.md), [1.4](parts/01-the-merge-loop/1.4-the-pre-tokenizer.md) | `PATTERN`, `pretokenize`, `word_counts`, `pair_counts`, `merge_word`, `train` — with the `(count, pair)` tie-break |
| `akshara/tokenizer/bpe.py` | [2.1](parts/02-training-a-vocabulary/2.1-the-merge-table-is-the-artifact.md) | `save`, `load`, `sha256` over `{pattern, alphabet, merges}` — merges as a JSON **array** |
| `days/day-012-bpe-the-merge-loop/lab/trace.py` | [1.2](parts/01-the-merge-loop/1.2-six-merges-by-hand.md) | the six-merge toy trace, printing the top four candidates at every step |
| `days/day-012-bpe-the-merge-loop/lab/audit.py` | [1.5](parts/01-the-merge-loop/1.5-the-merge-that-ate-the-space.md), [2.3](parts/02-training-a-vocabulary/2.3-reading-the-table.md) | `describe_merges`, `boundary_tokens`, `whitespace_tokens` — **runs on the merge list alone** |
| `days/day-012-bpe-the-merge-loop/lab/compare.py` | [3.1](parts/03-together/3.1-three-tokenizers-one-table.md) | the three-row table, every row from **one** text variable |
| `tests/test_bpe.py` | [1.1](parts/01-the-merge-loop/1.1-merge-the-commonest-pair.md), [1.4](parts/01-the-merge-loop/1.4-the-pre-tokenizer.md), [2.1](parts/02-training-a-vocabulary/2.1-the-merge-table-is-the-artifact.md), [2.5](parts/02-training-a-vocabulary/2.5-the-vocabulary-that-depended-on-the-order-of-the-corpus.md) | the toy-trace fixture, the pre-tokenizer tiling assertion, the artifact round trip, the order-independence test |

`akshara/tokenizer/bpe.py` sits beside Day 11's `char.py` and `word.py`. Day 13 extends the same module
rather than replacing it.

**`TODO(me)`:** part [2.4](parts/02-training-a-vocabulary/2.4-what-training-costs.md) projects 5.5 hours
for a 10 MB corpus at 8,000 merges, from a cost model that assumes the work is proportional to
`merges × characters`. Write down, in one paragraph and before reading Day 14, what data structure would
let a merge update only the affected words — and what you would have to store to know which words those
are.

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_bpe.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| change the tie-break to `max(pairs, key=pairs.get)` | passes on the toy fixture, fails on shuffled input | the order-independence test |
| drop the `i < len(symbols) - 1` guard in `merge_word` | `IndexError` on some words and not others | the toy-trace fixture |
| change `PATTERN` to `r"\S+"` | chunks look fine, `"".join(chunks) != text` | the pre-tokenizer tiling assertion |
| store the merges as a JSON object instead of an array | reloads cleanly, tokenizes the probe into more tokens | the artifact round trip |

The first row is the one worth doing carefully, because it is the day's subtlest failure: measured in part
2.5, the merge lists agree for **twenty-three merges** and diverge at the twenty-fourth. A test that
compares the first ten passes.

The fourth row is the one that looks harmless. `sort_keys=True` — the flag that makes the hash stable —
reorders a JSON object's keys, so a merge can end up running before the merge that creates its input.
Nothing raises; the probe just tokenizes into 21 tokens instead of 15.

---

## §6 Compute budget

**Tier: T0.** Python's standard library on a laptop CPU, over a 113,283-byte file in this repository.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — nothing installed, nothing downloaded |
| Disk | negligible; the largest artifact written is a 5,863-byte tokenizer file |
| Longest single step | **50.8 s** — training to `V = 2000`, measured on the hardware below |

What T0 proves: **every claim in this day.** The toy trace, the merge lists, the compression curve, the
boundary-token counts, the order-dependence divergence and the three-row table are all exact counts and
arithmetic over one file.

Three labels to read carefully, all stated in the parts as well:

- **The four training durations are wall-clock on Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB
  RAM, Windows 11, CPython 3.12.12** and are the only hardware-dependent numbers in the day. Every count,
  ratio and merge list is not.
- **Part 2.4's two extrapolated rows are arithmetic under a stated assumption**, not measurements. They
  assume cost is proportional to `merges × characters`, which the loop's structure implies and four data
  points do not prove.
- **Part 2.5's shuffle is seeded** with a stated seed, so the divergence at merge 24 reproduces exactly.

What T0 **cannot** show is whether a BPE vocabulary trains a better model than the alternatives at fixed
compute. That needs runs, it is Day 17, and today decides what it can on correctness grounds — losslessness
and coverage are properties of a table and need no GPU.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| `pairs[(a, b)] += 1` instead of `+= n` | trains on the vocabulary rather than the corpus; worse merges, no error | [1.1](parts/01-the-merge-loop/1.1-merge-the-commonest-pair.md) |
| No lookahead guard in `merge_word` | `IndexError` on some words, not others | [1.1](parts/01-the-merge-loop/1.1-merge-the-commonest-pair.md), [1.2](parts/01-the-merge-loop/1.2-six-merges-by-hand.md) |
| A trace that prints only the winner | ties invisible; part 2.5's bug survives review | [1.2](parts/01-the-merge-loop/1.2-six-merges-by-hand.md) |
| Letting the loop run to exhaustion | a word tokenizer, arrived at from the other direction | [1.3](parts/01-the-merge-loop/1.3-the-loop-and-where-it-stops.md) |
| A target below the alphabet size | `V` is the alphabet size, no merges, no error | [1.3](parts/01-the-merge-loop/1.3-the-loop-and-where-it-stops.md) |
| Sizing an embedding from `config.vocab_size` | rows that never receive a gradient when the trainer stops early | [1.3](parts/01-the-merge-loop/1.3-the-loop-and-where-it-stops.md) |
| A pre-tokenizer that does not tile the text | chunks look reasonable, the tokenizer cannot reproduce its input | [1.4](parts/01-the-merge-loop/1.4-the-pre-tokenizer.md) |
| A regex with a capturing group in `findall` | tuples instead of strings; `TypeError` on join | [1.4](parts/01-the-merge-loop/1.4-the-pre-tokenizer.md) |
| Dropping the pre-tokenizer because compression improved | 16 of 60 merges glue words to the next space | [1.5](parts/01-the-merge-loop/1.5-the-merge-that-ate-the-space.md) |
| Storing merges in a set, sorted, or as a JSON object | still lossless, 40% more tokens | [2.1](parts/02-training-a-vocabulary/2.1-the-merge-table-is-the-artifact.md) |
| Comparing compression across corpora | a confident conclusion about the wrong variable | [2.2](parts/02-training-a-vocabulary/2.2-training-to-a-target-size.md) |
| Never reading the merge list | a vocabulary trained on Markdown syntax, and no metric moves | [2.3](parts/02-training-a-vocabulary/2.3-reading-the-table.md) |
| Extrapolating training time by scaling one factor | 390× the cost, not 90× | [2.4](parts/02-training-a-vocabulary/2.4-what-training-costs.md) |
| `max(pairs, key=pairs.get)` | two runs, same data, different tokenizer | [2.5](parts/02-training-a-vocabulary/2.5-the-vocabulary-that-depended-on-the-order-of-the-corpus.md) |
| Ranking tokenizers by compression alone | the lossy one wins | [3.1](parts/03-together/3.1-three-tokenizers-one-table.md) |

Two of the plan's five silent failures are live today. **#2, tokenizer/template mismatch**, is part 2.5's
whole subject arriving through the trainer rather than through the id table: two artifacts, same size,
both lossless, different contents, and only the hash from part 2.1 can tell them apart. **#4, noise
mistaken for improvement**, is part 1.5: removing the pre-tokenizer *improves* compression on the training
text while making the tokenizer structurally worse, so the metric moves in the direction that means
success.

---

## §8 Verify before you code

Everything used today is the standard library. The symbols worth checking against the documentation for
**Python 3.12.12** were checked on **2026-08-26**:

| Symbol | What was checked | Why it matters today |
| --- | --- | --- |
| `max(iterable, key=...)` | returns the **first** maximal element | the entire subject of part 2.5 |
| `collections.Counter` | preserves insertion order; equality compares keys and counts | why the tie-break leaks corpus order; why part 1.1's losslessness check works |
| `re.findall` with groups | returns tuples, not strings, when the pattern has groups | part 1.4's loud failure |
| `re` and `\s`, `\S` | whitespace and non-whitespace, Unicode-aware by default | the pre-tokenizer pattern |
| `json.dumps(..., sort_keys=True)` | sorts **object keys**; does not reorder arrays | why merges must be an array — part 2.1 |
| `json.dumps(..., ensure_ascii=True)` | escapes all non-ASCII in the output | a merge list contains newlines and spaces |
| `time.perf_counter` | monotonic, highest available resolution | the right clock for a duration — parts 2.2 and 2.4 |
| `random.Random(seed)` | a local generator; does not touch global state | parts 2.1 and 2.5 seed their own shuffles |

One external document was fetched rather than recalled, on **2026-08-26**:

| Cited | What was checked | URL |
| --- | --- | --- |
| **arXiv:1508.07909**, *Neural Machine Translation of Rare Words with Subword Units* | title, and that the abstract describes byte-pair encoding used as a subword segmentation | `https://arxiv.org/abs/1508.07909` |

That paper is the one that brought byte-pair encoding into use as a tokenizer; the pair-merging idea
itself comes from a 1990s data-compression algorithm, which this day does not cite because it did not
fetch it.

---

## §9 Say it in an interview

*"Explain BPE in one minute."* — "Count every adjacent pair of symbols across the corpus, glue the
commonest one into a new symbol, add it to the vocabulary, repeat until the vocabulary is the size you
wanted. Because a merge is only ever an option at encode time, an unseen word falls back to smaller pieces
instead of becoming `<unk>`. And the pieces it finds are the ones you would have picked by hand — on my
corpus merge 18 was `ing` and merge 23 was `ion`, with no grammar in the algorithm at all."

*"How do you choose the vocabulary size?"* — "It is a dial between two failures rather than a
hyperparameter with an optimum. Zero merges is a character tokenizer; running to exhaustion is a word
tokenizer — on a twelve-word toy corpus that took 12 merges and left every word as one token. In between,
compression rises concavely: my return fell from 0.174 to 0.067 characters per token per hundred merges
between `V = 500` and `V = 2000`, while the parameter cost rises linearly at `2VC`. So the decision is
where a falling benefit meets a constant marginal cost."

*"Why do BPE tokenizers use a pre-tokenizer? The algorithm does not need one."* — "Without it the
commonest pairs in English are word endings followed by a space, so the highest-value merges get spent on
tokens like `'e '` and `', '` — I measured 16 of the first 60. Once those exist, a word's tokenization
depends on the character after it. And it does not show up in the round trip or in the compression ratio,
which is actually slightly *better* without the pre-tokenizer, so the only way to see it is to read the
merge list."

*"BPE training has no randomness in it. Is it deterministic?"* — "Only if the tie-break is total. Ties are
constant, and `max` on counts alone returns whichever tied pair the counter yields first — which is
insertion order, which is corpus read order. I trained on the same words in two orders and the merge lists
diverged at merge 24, with both tokenizers passing every check I had: same size, both lossless, same
compression, ids in range. The only thing that differed was the artifact hash."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 12` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined by
understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 12 | 2026-08-27 | TOK-07, TOK-08 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; everything used is the standard library.

`docs/DATASETS.md` — **no rows today.** Every measurement is over `docs/00_MASTER_PLAN.md`, a file in this
repository under this repository's own licence. It was not downloaded and it is not a dataset. The first
`DATASETS.md` row is still Day 14's.

`docs/MODELS.md` — **no rows today.** Nothing was downloaded and nothing was loaded.

`docs/RUNS.md` — **no rows today.** Nothing today trains a model. The four training durations are
tokenizer training, not model training, and part 2.4's two projections are labelled as arithmetic in their
part and again in §6.

Commit:

```text
day 012: BPE from scratch I, the merge loop — closes TOK-07, TOK-08
```
