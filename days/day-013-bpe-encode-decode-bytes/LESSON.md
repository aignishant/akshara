---
day: 13
phase: 2
phase_name: "Tokenization"
title: "BPE from scratch II — encode, decode, the regex pre-tokenizer, and byte-level BPE"
ids: ["TOK-09", "TOK-10", "TOK-11"]
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

# Day 13 — BPE from scratch II

> **Yesterday (Day 12):** the merge rule, by hand on twelve words and then trained. It closed every trade
> Day 11 named and one of its two gates, and left the other exactly where it was.
> **Today:** the three things that turn a merge list into a tokenizer — an encoder that runs at scale, a
> pre-tokenizer worth the name, and the one-line change that closes the last gate.
> **Tomorrow (Day 14):** 🔍 open a production tokenizer and compare — `tiktoken` and the `tokenizers`
> pipeline (TOK-12, TOK-13).

---

## §1 Where we are

Day 12 ended with a scoreboard that had one line still open: **the alphabet came from the corpus**, so a
tokenizer trained on English raised on the first Cyrillic character it met, and no number of merges could
help because merges combine symbols and never add one.

Today closes it, and the change is `sorted(set(text))` → `range(256)`. Everything else about the
algorithm is untouched. What it buys is not a better coverage percentage but a different kind of claim:
**every input is a byte string, every byte is one of 256, and all 256 are the first entries of the
vocabulary, so `encode` cannot raise.** Measured here, five scripts, an emoji sequence, an empty string
and 64 random bytes all round-trip. The bill is 0.24 characters per token and 4.0% of the merges spent
reassembling multi-byte characters.

Before that, two things the merge list needed. **An encoder that inverts the loop**: instead of walking
744 merges asking which apply, walk the pairs in the word and take the lowest rank — identical output,
**93× faster**. And **a pre-tokenizer worth the name**: Day 12's `\s*\S+|\s+` keeps `don't`, `3.14`,
`GPT-2` and `snake_case` as single chunks, so merges glue letters to digits and words to apostrophes. The
GPT-style pattern separates them, at a cost of 5% compression — 2.51 characters per token down to 2.39 —
and it trains 1.9× faster because it produces 35% fewer distinct chunks.

Three of the thirteen parts are failures. A byte-level token can be **half a character**, so decoding a
prefix during generation prints a black diamond that a later token replaces. A number is **three tokens
in an arbitrary grouping** — `2024` is `2` + `02` + `4` — because the digit branch is unbounded. And the
merge list, which Day 12 taught you to read as a diagnostic, is now **partly illegible**: three of the
first twenty-two merges are the UTF-8 bytes of one em dash, two of which decode to nothing.

One of those failures caught a bug in this day's own material. Day 12's merge audit, carried forward
without thinking, reported 15 letter-and-digit merges that do not exist — because the byte-mapping
symbols are themselves letters. **A check written for one representation gives confident wrong answers on
another**, and part 2.3 shows the corrected version.

Everything runs on the laptop. Every script prints the corpus sha256 first.

---

## §2 The map

Thirteen parts, four sections. Section 1 is TOK-09 — turning a merge list into a working encoder and
decoder. Section 2 is TOK-10 — the pre-tokenizer, read symbol by symbol. Section 3 is TOK-11 — the byte
alphabet. Section 4 closes Day 11's scoreboard. Each of the first three sections ends with something
breaking.

### Section 1 — `01-encode-and-decode`: TOK-09, merge list to tokenizer

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [Encoding applies merges by rank](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md) | Why is inverting the loop 93× faster with identical output? | `foundation` |
| 1.2 | [Decode is a lookup, not a search](parts/01-encode-and-decode/1.2-decode-is-a-lookup-not-a-search.md) | Which direction of the round trip does *not* hold, and where does that bite? | `working` |
| 1.3 | [From tokens to ids](parts/01-encode-and-decode/1.3-from-tokens-to-ids.md) | Why is `V` knowable before the corpus is read? | `working` |
| 1.4 | [💥 The token that was half a character](parts/01-encode-and-decode/1.4-the-token-that-was-half-a-character.md) | Why does a streamed response flicker a black diamond? | `production` |

### Section 2 — `02-the-regex-pre-tokenizer`: TOK-10, where merges may not reach

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Why Day 12's pattern is not enough](parts/02-the-regex-pre-tokenizer/2.1-why-day-12s-pattern-is-not-enough.md) | What does a whitespace-only boundary fail to separate? | `foundation` |
| 2.2 | [The GPT pattern, symbol by symbol](parts/02-the-regex-pre-tokenizer/2.2-the-gpt-pattern-symbol-by-symbol.md) | What is each of the seven branches protecting? | `working` |
| 2.3 | [What the pattern costs and buys](parts/02-the-regex-pre-tokenizer/2.3-what-the-pattern-costs-and-buys.md) | Why does the better pre-tokenizer compress worse and train faster? | `working` |
| 2.4 | [💥 The number that was three tokens](parts/02-the-regex-pre-tokenizer/2.4-the-number-that-was-three-tokens.md) | Why does `2024` split as `2` + `02` + `4`? | `production` |

### Section 3 — `03-byte-level-bpe`: TOK-11, the last gate

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [The alphabet becomes 256](parts/03-byte-level-bpe/3.1-the-alphabet-becomes-256.md) | What does one line change, and what does it cost? | `foundation` |
| 3.2 | [The byte-to-unicode trick](parts/03-byte-level-bpe/3.2-the-byte-to-unicode-trick.md) | Why is a GPT vocabulary full of `Ġ`? | `working` |
| 3.3 | [Zero out-of-vocabulary, measured](parts/03-byte-level-bpe/3.3-zero-out-of-vocabulary.md) | What is the difference between a coverage percentage and a construction? | `working` |
| 3.4 | [💥 The vocabulary you cannot read](parts/03-byte-level-bpe/3.4-the-vocabulary-you-cannot-read.md) | What does byte-level cost besides sequence length? | `production` |

### Section 4 — `04-together`: the scoreboard, closed

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Four tokenizers, one table](parts/04-together/4.1-four-tokenizers-one-table.md) | What did each of Day 11's five findings cost to close? | `production` |

---

## §3 Setup — run this

**No new packages today** — `re`, `json`, `hashlib`, `codecs`, `time`, `random`, `collections`, `pathlib`.
Principle 3 holds for one more day: the hand-rolled byte-level BPE exists before any library is opened,
and Day 14 is when `tiktoken` and `tokenizers` arrive with pinned versions and `docs/PACKAGES.md` rows.

```bash
uv run python -c "import sys; print('python', sys.version.split()[0])"
uv run python -c "import hashlib, pathlib; print('corpus sha256[:16]', hashlib.sha256(pathlib.Path('docs/00_MASTER_PLAN.md').read_bytes()).hexdigest()[:16])"
./m scaffold 13
```

**Compare that hash against `9760f2b6d4340b97`** and write down what you get.

One thing to know before you start, because it shapes how you work: **train once, save, and reuse.** The
trainer is still Day 12's naive one, so `V = 1000` takes about 20 seconds. Every part in sections 1 and 3
loads a merge list from a file rather than retraining; part 3.1 is where it is produced.

Two conventions, both carried forward and both load-bearing today:

- **Every token is printed with `ascii()`.** After part 3.2 a token is a string of byte-mapped symbols and
  `Ġ` versus a space is the distinction you need most.
- **To ask what a token *means*, decode it to bytes first.** Part 2.3 measured an audit that skipped this
  step and reported fifteen merges that do not exist. This is the day's most transferable habit.

Day 12 parts 1.4, 2.1 and 2.3 are referenced throughout; Day 10 parts 2.2, 2.4 and 2.5 supply the UTF-8
facts and get cited rather than repeated.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `akshara/tokenizer/bpe.py` | [3.1](parts/03-byte-level-bpe/3.1-the-alphabet-becomes-256.md), [3.2](parts/03-byte-level-bpe/3.2-the-byte-to-unicode-trick.md) | `bytes_to_unicode`, `BYTE_ENCODER`, `BYTE_DECODER`, `to_symbols`, `from_symbols`; `train` with the 256-byte alphabet |
| `akshara/tokenizer/bpe.py` | [1.1](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md), [1.3](parts/01-encode-and-decode/1.3-from-tokens-to-ids.md) | `encode_chunk` by rank, `encode_ids`, `decode_ids`, and a frozen `Tokenizer` whose tables are all derived from `merges` |
| `akshara/tokenizer/pretok.py` | [2.2](parts/02-the-regex-pre-tokenizer/2.2-the-gpt-pattern-symbol-by-symbol.md) | `GPT_LIKE` assembled branch by branch with a comment per branch, and `pretokenize` with the tiling assertion inside it |
| `days/day-013-bpe-encode-decode-bytes/lab/stream.py` | [1.4](parts/01-encode-and-decode/1.4-the-token-that-was-half-a-character.md) | `StreamingDecoder` with `push` and `finish` |
| `days/day-013-bpe-encode-decode-bytes/lab/audit.py` | [2.3](parts/02-the-regex-pre-tokenizer/2.3-what-the-pattern-costs-and-buys.md), [3.4](parts/03-byte-level-bpe/3.4-the-vocabulary-you-cannot-read.md) | `real_text`, `kinds(via_bytes=True)`, `token_report` — **decoding is the default, raw symbols are opt-in** |
| `days/day-013-bpe-encode-decode-bytes/lab/compare.py` | [4.1](parts/04-together/4.1-four-tokenizers-one-table.md) | the four-row table, one `text` variable, coverage as a string |
| `tests/test_bpe_bytes.py` | [1.1](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md), [1.4](parts/01-encode-and-decode/1.4-the-token-that-was-half-a-character.md), [3.2](parts/03-byte-level-bpe/3.2-the-byte-to-unicode-trick.md), [3.3](parts/03-byte-level-bpe/3.3-zero-out-of-vocabulary.md) | the two-encoder oracle test, the streaming/batch agreement test, the byte-map bijection, the total-coverage assertion |

**`TODO(me)`:** part [2.4](parts/02-the-regex-pre-tokenizer/2.4-the-number-that-was-three-tokens.md)
showed the `cl100k` digit cap, `\p{N}{1,3}`, making number grouping depend on length rather than on the
corpus. Write down, in one paragraph and before Day 17, what you would measure to find out whether the
cap **helps a model** rather than merely making the input regular — and what you would compare against.

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_bpe_bytes.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| change `if r is not None` to `if r` in `encode_chunk` | more tokens, no error — rank 0 is skipped | the two-encoder oracle test |
| decode each prefix instead of using the incremental decoder | `U+FFFD` on any multi-byte probe | the streaming/batch agreement test |
| replace `cs = bs[:]` with `cs = bs` in `bytes_to_unicode` | fewer than 256 distinct symbols | the byte-map bijection test |
| build the vocabulary as merges-only, no alphabet | `KeyError` on the first non-ASCII byte | the total-coverage assertion |

The first row is the subtlest bug in the day: **rank `0` is the most frequent merge in the tokenizer**,
and a truthiness test skips it forever while everything still round-trips.

The second row **cannot fail on an English probe list** — that is the point of it. The test's probe list
has to contain a multi-byte character or it passes on a broken decoder, which is Silent Failure #5 in a
test suite.

---

## §6 Compute budget

**Tier: T0.** Python's standard library on a laptop CPU, over a 113,283-byte file in this repository.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** |
| Free notebook sessions | 0 |
| Network | none — nothing installed, nothing downloaded |
| Disk | negligible; one tokenizer file |
| Longest single step | **33.7 s** — training with the simple pattern in part 2.3 |

What T0 proves: **every claim in this day.** The encoder equivalence and its speed ratio, the pattern
comparison, the byte map's bijection, the coverage construction, the merge tax and the four-row table are
all exact counts, arithmetic, or timings on stated hardware.

Four labels to read carefully, all stated in the parts too:

- **The timings** (93×, 33.7 s, 18.2 s, 20.2 s) are wall-clock on Intel Core i3-1115G4 (2 cores / 4
  threads), 11.7 GB RAM, Windows 11, CPython 3.12.12. Every count and ratio is not hardware-dependent.
- **`GPT_LIKE` is a stdlib approximation** of the published pattern, because `\p{L}` and possessive
  quantifiers need the `regex` module. Part 2.2 quotes the original, names every difference, and verifies
  the approximation on six probes — and explicitly does not claim agreement beyond them.
- **Part 3.4's Devanagari scaling block is arithmetic** under a stated bytes-per-character ratio, not a
  measurement. This day has no Devanagari corpus.
- **Part 3.3's random blobs are seeded** with a stated seed, and the part explains why their id counts
  exceed their byte counts.

What T0 **cannot** show is whether any of this trains a better model. That is Day 17. Today decides what
it can on properties — losslessness, coverage, boundary discipline — which are checkable without a GPU.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| `if r:` on a merge rank | rank 0 skipped forever; more tokens, no error | [1.1](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md) |
| Building `ranks` from a `set` | valid output, twice as many tokens | [1.1](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md) |
| Rebuilding `stoi` or `ranks` inside `encode` | an `O(1)` lookup becomes an `O(V)` construction per call | [1.1](parts/01-encode-and-decode/1.1-encoding-applies-merges-by-rank.md), [1.3](parts/01-encode-and-decode/1.3-from-tokens-to-ids.md) |
| Assuming `encode(decode(y)) == y` | prompt pieces concatenated at a boundary encode never saw | [1.2](parts/01-encode-and-decode/1.2-decode-is-a-lookup-not-a-search.md) |
| Storing `vocab_size` in a config as well as the tokenizer | two sources of truth, and one is wrong after an early stop | [1.3](parts/01-encode-and-decode/1.3-from-tokens-to-ids.md) |
| Decoding a prefix after every token | `U+FFFD` on every multi-byte character | [1.4](parts/01-encode-and-decode/1.4-the-token-that-was-half-a-character.md) |
| Omitting `final=True` from the streaming flush | a truncated last character, silently | [1.4](parts/01-encode-and-decode/1.4-the-token-that-was-half-a-character.md) |
| A pre-tokenizer that splits only on whitespace | merges spanning digits, apostrophes and underscores | [2.1](parts/02-the-regex-pre-tokenizer/2.1-why-day-12s-pattern-is-not-enough.md) |
| `[A-Za-z]+` as the letter branch | non-Latin words match nothing; the pattern stops tiling | [2.2](parts/02-the-regex-pre-tokenizer/2.2-the-gpt-pattern-symbol-by-symbol.md) |
| Choosing a pre-tokenizer on compression | the worse one wins by 5% | [2.3](parts/02-the-regex-pre-tokenizer/2.3-what-the-pattern-costs-and-buys.md) |
| Auditing byte-level tokens without decoding | 15 letter-digit merges reported that do not exist | [2.3](parts/02-the-regex-pre-tokenizer/2.3-what-the-pattern-costs-and-buys.md), [3.4](parts/03-byte-level-bpe/3.4-the-vocabulary-you-cannot-read.md) |
| An unbounded digit branch | `2024` → `2` + `02` + `4`, grouping set by the corpus | [2.4](parts/02-the-regex-pre-tokenizer/2.4-the-number-that-was-three-tokens.md) |
| `cs = bs` instead of `cs = bs[:]` | two bytes share a symbol; almost-right text, no error | [3.2](parts/03-byte-level-bpe/3.2-the-byte-to-unicode-trick.md) |
| Building the vocabulary without the byte block first | `KeyError` on the first non-ASCII byte, or misaligned embeddings | [3.3](parts/03-byte-level-bpe/3.3-zero-out-of-vocabulary.md) |
| Reporting coverage as a percentage | invites re-measuring what is a construction | [3.3](parts/03-byte-level-bpe/3.3-zero-out-of-vocabulary.md) |
| Ranking the four tokenizers by compression | the lossy, gated one wins | [4.1](parts/04-together/4.1-four-tokenizers-one-table.md) |

Two of the plan's five silent failures are live. **#2, tokenizer/template mismatch**, appears twice: as
non-canonical id sequences from concatenated prompt pieces (part 1.2), and as a merge list encoded under
a different pre-tokenizer than it was trained with (parts 2.3 and 4.1) — neither raises. **#5, evaluated
on the format you trained on**, is part 1.4's streaming test, which passes on any English probe list, and
part 2.2's ASCII letter class, which works perfectly until it meets another script.

---

## §8 Verify before you code

Standard library only. Checked against the **Python 3.12.12** documentation on **2026-08-27**:

| Symbol | What was checked | Why it matters today |
| --- | --- | --- |
| `codecs.getincrementaldecoder(enc)` | returns a decoder class; `decode(chunk, final=False)` retains partial sequences | part 1.4's streaming fix |
| `re` alternation | alternatives are tried left to right at each position | why the pattern's branch order is its meaning — part 2.2 |
| `re` and `\W`, `\d`, `\w` | Unicode-aware by default in Python 3 | `[^\W\d_]` as the stdlib "any letter" — part 2.2 |
| `re.findall` with groups | returns tuples, not strings | part 2.1's loud failure |
| `str.isalpha`, `str.isprintable`, `str.isspace` | Unicode-property based | why the byte-mapping symbols fool a naive audit — part 2.3 |
| `max(iterable, key=...)` | returns the first maximal element | inherited from Day 12 part 2.5 |
| `random.Random(seed)` | a local generator; does not touch global state | parts 3.3's seeded blobs |

One external source was **fetched, not recalled**, on **2026-08-27**:

| Cited | What was taken from it | URL |
| --- | --- | --- |
| `tiktoken`'s `openai_public.py` | the `gpt2` (`r50k`) and `cl100k_base` `pat_str` values, quoted verbatim | `https://raw.githubusercontent.com/openai/tiktoken/main/tiktoken_ext/openai_public.py` |

Part 2.2 quotes the `gpt2` pattern exactly and part 2.4 quotes `cl100k_base`'s digit branch. Both use
`\p{L}`, `\p{N}` and possessive quantifiers, which Python's `re` does not support — hence the stdlib
approximation and its named differences.

---

## §9 Say it in an interview

*"How does a BPE tokenizer encode a word at inference time?"* — "You do not iterate over the merges; you
iterate over the pairs present in the word and repeatedly take the one with the lowest rank. The merge
list is a ranking and rank order is learning order. Walking the list gives the same answer and does a
scan per merge whether or not it applies — I measured 93× slower at 744 merges, and the gap widens with
vocabulary size."

*"Is encode the inverse of decode?"* — "One direction only. `decode(encode(s)) == s` always; `encode(decode(y)) == y`
only when `y` was already canonical. Decode is a many-to-one table lookup and encode is a search that
picks one particular cut — I can build two id sequences, five tokens and eleven, that decode to the same
string. Non-canonical sequences arise from concatenating separately encoded prompt pieces, from
truncation, and from the model's own sampling."

*"Why do BPE tokenizers use an elaborate regex pre-tokenizer?"* — "Every boundary it adds is a place
merges may not reach. Without one, `3.14` is a single chunk and merges join digits to the decimal point,
so a number tokenizes differently depending on whether it has a fractional part. Adding boundaries cost me
5% compression — 2.51 to 2.39 characters per token — and took mixed-kind merges from 88 to one, which is
the `'s` the pattern deliberately creates."

*"Why byte-level?"* — "It turns coverage from a measurement into a construction: every input is a byte
string, every byte is one of 256, and all 256 are the first vocabulary entries, so `encode` cannot raise.
The price is 0.24 characters per token on my corpus, plus merges spent reassembling multi-byte characters
— an em dash took three of my first twenty-two merges, two of which decode to nothing. And the merge list
becomes unreadable for exactly the languages you cannot check by eye, so any audit has to decode tokens to
bytes first."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 13` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined by
understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 13 | 2026-08-27 | TOK-09, TOK-10, TOK-11 | 13 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing installed. Day 14 is the first day with rows here.

`docs/DATASETS.md` — **no rows today.** Every measurement is over `docs/00_MASTER_PLAN.md`, a file in this
repository under its own licence.

`docs/MODELS.md` — **no rows today.** Nothing downloaded, nothing loaded. The `tiktoken` source file cited
in §8 was read on the web, not fetched into the repository.

`docs/RUNS.md` — **no rows today.** Nothing trains a model; the timings are tokenizer training.

Commit:

```text
day 013: BPE II — encode, decode, the pre-tokenizer and bytes — closes TOK-09, TOK-10, TOK-11
```
