---
day: 10
phase: 2
phase_name: "Tokenization"
title: "Unicode, code points and bytes — the layer under every tokenizer"
ids: ["TOK-03", "TOK-04"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18]
kind: tokenizer
plan_version: "v1.3.0"
parts: 11
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 10 — Unicode, code points and bytes

> **Yesterday (Day 9):** what a vocabulary is, why words and characters both fail, and the two
> failures that follow — a vocabulary that could not spell, and a tokenizer that did not match.
> **Today:** the layer underneath all of that. What the word "character" actually means, why the same
> word has two spellings that are not equal, what a person sees versus what `len()` counts, and how
> text becomes the bytes that are really in the file.
> **Tomorrow (Day 11):** character-level and word-level tokenizers, built as real modules — and where
> each one dies (TOK-05, TOK-06).

---

## §1 Where we are

Day 9 built a tokenizer over `sorted(set(text))` and called the result "every distinct character". Today
is about the fact that the word *character* in that sentence has three meanings, that they disagree
constantly, and that the disagreement is where a whole family of quiet bugs lives.

Here is the shape of it, before any terminology. Take a word with an accent in it. There are two ways
to write that word, both correct, both allowed by the standard, and both drawing identically on your
screen. They are not equal. They do not hash the same. One of them is in your dictionary and the other
is not. Nothing on the screen tells you which one you have, and the first symptom is usually a search
box that finds nothing, or a contact list with the same shop in it twice.

Now take an emoji of a family. A reader sees one thing. `len()` says seven. A browser's `.length` says
eleven. The file holds twenty-five bytes. Four numbers, one picture, and every one of them correct for
a different question.

Today measures all of that, on this laptop, and then follows it down to the layer where the ambiguity
stops. A file does not hold characters; it holds bytes. There are 256 of them. There were 256 before
Unicode existed and there will be 256 after the next twenty releases — while the assigned character set
grew by **54,030 characters** between the two Unicode tables CPython ships side by side, measured here
rather than recalled. That is the whole argument for byte-level tokenization, and it is a correctness
argument rather than a performance one: a byte vocabulary has zero out-of-vocabulary rate **by
construction**, for every input that has ever existed.

The price is length. A Devanagari sentence is 2.75 bytes per character where English is 1.00, and
because attention grows with the square of the sequence, that is 7.56× the attention work for the same
content. Bytes are not the answer; **bytes are the floor**, and Day 13 buys the length back with
merges.

Two of the eleven parts are failures reproduced on purpose, and neither of them starts with an
exception. In one, two strings that print identically fail to deduplicate, miss each other in a `dict`,
and produce two vocabularies with **the same size and different hashes** — seven review checks pass and
one fails. In the other, a data pipeline reading a file in 64-byte chunks raises on **139 of 157
chunks**, gets "fixed" with two words, and quietly loses **95 characters out of 5,600** — every one of
them non-ASCII.

Everything runs on the laptop with no packages installed. Every corpus in this day is built from
literal escapes inside the scripts, so **every figure here reproduces exactly** on any machine carrying
the same Unicode version, with no file on disk and nothing downloaded.

---

## §2 The map

Eleven parts, three sections. Section 1 is TOK-03 — what a character is, above the byte layer. Section
2 is TOK-04 — the byte layer itself. Section 3 puts all five units in one table. The day climbs
`foundation → working → production`, and each of the first two sections ends with something breaking.

### Section 1 — `01-code-points-and-graphemes`: TOK-03, what "character" means

Three levels with one name, and the standard-library operations that quietly pick one of them. This
section ends with the failure that follows from two spellings of the same word.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A character is three different things](parts/01-code-points-and-graphemes/1.1-a-character-is-three-different-things.md) | Why do four apps give four different lengths for one emoji? | `foundation` |
| 1.2 | [What `len`, slicing and reversing actually operate on](parts/01-code-points-and-graphemes/1.2-what-len-actually-counts.md) | Which of the three levels does the code you already write use? | `working` |
| 1.3 | [Normalization — one spelling for the same thing](parts/01-code-points-and-graphemes/1.3-normalization-one-spelling-for-the-same-thing.md) | If two spellings mean the same text, which one do you store? | `working` |
| 1.4 | [Graphemes — what a person sees](parts/01-code-points-and-graphemes/1.4-graphemes-what-a-person-sees.md) | How close can you get to "what a reader sees" without a library? | `working` |
| 1.5 | [💥 The string that was not equal to itself](parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md) | Why do seven reasonable checks pass on a mismatched pair? | `production` |

### Section 2 — `02-utf-8-and-bytes`: TOK-04, the layer underneath

What is actually in the file, the rule that puts it there, the property that makes it safe to cut, and
the argument that ends the vocabulary question. Then the failure that ships.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Text has to become bytes](parts/02-utf-8-and-bytes/2.1-text-has-to-become-bytes.md) | Why does the wrong encoding produce readable nonsense instead of an error? | `foundation` |
| 2.2 | [How UTF-8 encodes a code point](parts/02-utf-8-and-bytes/2.2-how-utf-8-encodes-a-code-point.md) | What do the bits actually say, and why did this design win? | `working` |
| 2.3 | [Self-synchronising — finding a boundary from anywhere](parts/02-utf-8-and-bytes/2.3-self-synchronising.md) | How do you cut a byte buffer safely without decoding it? | `working` |
| 2.4 | [256 is a vocabulary that is finished](parts/02-utf-8-and-bytes/2.4-256-is-a-vocabulary.md) | Which of the three units has a set you can finish enumerating? | `production` |
| 2.5 | [💥 The decode that split a character](parts/02-utf-8-and-bytes/2.5-the-decode-that-split-a-character.md) | Why does one chunk size make the whole bug disappear? | `production` |

### Section 3 — `03-together`: the day in one table

Eight strings, five units, five different totals — and the observation that four of the five columns
are trades while the fifth is settled by a property none of them has.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [One string, five layers, one table](parts/03-together/3.1-one-string-five-layers.md) | Which unit wins, and what does the losing side actually cost? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything is the Python standard library — `unicodedata`, `codecs`,
`locale`, `sys`, `hashlib`, `json`, `pathlib`, `collections`. That is not frugality: a tokenizer's
relationship with Unicode is exactly the thing a library would hide, and Principle 3 says the
hand-rolled version comes first.

```bash
uv run python -c "import sys, unicodedata; print('python', sys.version.split()[0], '| unicodedata', unicodedata.unidata_version)"
./m scaffold 10
```

**Print that second number and write it down.** Every count in section 1 is a property of the Unicode
data version, not of Python, and a machine with a different version will legitimately disagree. On the
machine this day was written on it prints `python 3.12.12 | unicodedata 15.0.0`. Section 2's numbers do
**not** depend on it, because the UTF-8 rules and the code point range are fixed — noticing which
half of the day is version-dependent is part of the point.

There is no corpus file today, deliberately. Day 9 measured over `docs/00_MASTER_PLAN.md`; this day
builds every test string from literal escapes inside the scripts, so nothing here can drift when a
document in this repository is edited. Where a corpus is needed — part 2.5 — it is a 50-byte unit
repeated 200 times, written out in the part.

One convention runs through the whole day and it is worth adopting before you start: **write non-ASCII
test data as escapes, and print it with `ascii()`.** Both spellings of an accented word are the same
pixels, so a literal in a file cannot tell you which one it is. There is a second reason on Windows: the
console encoding here is `cp1252`, and printing a combining accent raises `UnicodeEncodeError` half way
through the line. Part 2.1 measures both defaults.

Nothing from Days 2–8 is needed to run today's code. Day 9 parts 1.1, 2.1 and 2.4 are referenced
constantly, and rereading 2.1 — the round-trip property — before you start is worth it.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-010-unicode-code-points-bytes/lab/measure.py` | [1.1](parts/01-code-points-and-graphemes/1.1-a-character-is-three-different-things.md), [1.2](parts/01-code-points-and-graphemes/1.2-what-len-actually-counts.md) | `describe_length(s)` returning four named counts and **no key called `length`** |
| `days/day-010-unicode-code-points-bytes/lab/normalize.py` | [1.3](parts/01-code-points-and-graphemes/1.3-normalization-one-spelling-for-the-same-thing.md), [1.5](parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md) | `NORM` as a module constant, `normalize_text`, `check_tokenizer_normalization` |
| `days/day-010-unicode-code-points-bytes/lab/clusters.py` | [1.4](parts/01-code-points-and-graphemes/1.4-graphemes-what-a-person-sees.md) | `clusters_v2`, `cluster_count` — with a docstring that names its measured score and what it does not handle |
| `days/day-010-unicode-code-points-bytes/lab/bytes_io.py` | [2.2](parts/02-utf-8-and-bytes/2.2-how-utf-8-encodes-a-code-point.md), [2.3](parts/02-utf-8-and-bytes/2.3-self-synchronising.md), [2.5](parts/02-utf-8-and-bytes/2.5-the-decode-that-split-a-character.md) | `encode_utf8_by_hand`, `char_start`, `truncate_bytes`, `decode_stream` |
| `tests/test_unicode.py` | [2.2](parts/02-utf-8-and-bytes/2.2-how-utf-8-encodes-a-code-point.md), [2.3](parts/02-utf-8-and-bytes/2.3-self-synchronising.md), [2.5](parts/02-utf-8-and-bytes/2.5-the-decode-that-split-a-character.md) | the all-code-points encoder test, the safe-cut test, the chunked-decode test |

Nothing under `akshara/` today. Day 11 is where the tokenizer becomes a package module; today's code
lives in `lab/`, because these are the primitives Day 11 will import ideas from rather than files.

**`TODO(me)`:** part [1.4](parts/01-code-points-and-graphemes/1.4-graphemes-what-a-person-sees.md)'s
approximation agrees with a reader on six of ten cases. Write down, in one paragraph, which of the four
remaining failures you would fix next and what information you would need that `unicodedata` does not
give you — **before** looking at how a segmentation library does it.

---

## §5 The eval that must be able to fail

Three checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_unicode.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| change a `0x3F` mask to `0x7F` in `encode_utf8_by_hand` | passes on Latin and Devanagari, **fails on the emoji** | the all-code-points encoder test |
| delete the walk-back loop in `truncate_bytes` | `UnicodeDecodeError` on any non-ASCII input at most limits | the safe-cut test |
| replace `decode_stream` with a per-chunk `decode(..., errors="ignore")` | no exception; 95 fewer characters | the chunked-decode test |

The first row is the one worth doing by hand, because the result is counter-intuitive: measured in part
2.2, the wrong mask produces **byte-for-byte correct output** for `U+0936` and `U+20AC` and raises only
on the emoji. A sampled test passes. That is why the encoder test iterates all 1,112,064 valid code
points rather than a list of interesting ones — it runs on a laptop, and it is the only honest version.

The third row is the one that will actually happen to you. `errors="ignore"` is added to stop a crash
in a data pipeline roughly once per project, and it removes exactly the non-ASCII characters, silently,
with no count.

---

## §6 Compute budget

**Tier: T0.** Python's standard library on a laptop CPU. No packages, no network, no data files.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — nothing installed, nothing downloaded |
| Disk | one temporary file in part 2.1, written and deleted by the example |

The heaviest thing today is a loop over all 1,114,112 code point values, run a handful of times. That
is a laptop's work on one core, and it is what makes the counts exact rather than sampled.

What T0 proves: **every claim in this day.** The normalization counts, the assigned-character growth,
the UTF-8 widths and byte census, the walk-back bound, the byte-vocabulary round trip, the chunk-split
losses and the five totals in part 3.1 are all exact counts over strings written into the scripts. There
is no seed and no timing anywhere in this day.

What T0 **cannot** show is the only question that finally decides byte-level versus character-level:
whether it produces a better model at fixed compute. That needs training runs, it is Day 17, and no
amount of counting substitutes for it. The `attention vs English` column in part 2.4 is arithmetic from
a measured byte ratio — a projection, labelled as one — and not a benchmark.

Two labels to read carefully. The **`seen` column** in parts 1.4 and 3.1 is a claim about what a reader
perceives, not a measurement; it depends on your font and renderer, and both parts say so. The
**`cp1252` results** in part 2.1 are properties of *this* machine's locale; a Linux or macOS reader will
see `UTF-8` and no exception from the default file read, and that difference is the lesson rather than a
failed reproduction.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Two spellings of one word compared with `==` | `False`, and both print identically | [1.3](parts/01-code-points-and-graphemes/1.3-normalization-one-spelling-for-the-same-thing.md), [1.5](parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md) |
| Storing `NFKC` because it "normalizes more" | a joined `fi` becomes two letters in the user's own name, permanently | [1.3](parts/01-code-points-and-graphemes/1.3-normalization-one-spelling-for-the-same-thing.md) |
| Slicing a `str` by a number for display | an accent dropped, half a family emoji, no exception | [1.2](parts/01-code-points-and-graphemes/1.2-what-len-actually-counts.md), [1.4](parts/01-code-points-and-graphemes/1.4-graphemes-what-a-person-sees.md) |
| A helper called `grapheme_count` that is an approximation | six of ten, trusted like ten of ten | [1.4](parts/01-code-points-and-graphemes/1.4-graphemes-what-a-person-sees.md) |
| Two vocabularies checked by size | 16 and 16, different contents, different hashes | [1.5](parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md) |
| `vocab.get(c, UNK)` to stop a `KeyError` | the crash stops, the accent becomes `<unk>`, loss goes **down** | [1.5](parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md) |
| `open(path)` with no `encoding=` | `cp1252` here, `utf-8` on the build machine, same file | [2.1](parts/02-utf-8-and-bytes/2.1-text-has-to-become-bytes.md) |
| `decode("latin-1")` as a way to "never fail" | never fails, always wrong, five characters where four went in | [2.1](parts/02-utf-8-and-bytes/2.1-text-has-to-become-bytes.md) |
| A hand-written encoder with a seven-bit mask | correct on Latin and Devanagari, raises on emoji | [2.2](parts/02-utf-8-and-bytes/2.2-how-utf-8-encodes-a-code-point.md) |
| Cutting a byte buffer at a fixed offset | `unexpected end of data` on one side, `invalid start byte` on the other | [2.3](parts/02-utf-8-and-bytes/2.3-self-synchronising.md) |
| Comparing losses between two tokenizations | different token counts for the same text; the ordering is an artefact | [2.4](parts/02-utf-8-and-bytes/2.4-256-is-a-vocabulary.md) |
| A chunk size that divides your test corpus's period | 0 of 100 chunks raise; the bug is fully present | [2.5](parts/02-utf-8-and-bytes/2.5-the-decode-that-split-a-character.md) |
| Writing a number called `length` | five candidate values, differing by 3.7× | [3.1](parts/03-together/3.1-one-string-five-layers.md) |

Three of the plan's five silent failures are live today. **#2, tokenizer/template mismatch**, is part
1.5's whole subject — the check the plan prescribes, round-tripping a real training string through the
inference path, is written there as a function. **#5, evaluated on the format you trained on**, appears
twice in an unexpected costume: part 1.4's approximation scores four of four on the Latin rows a test
suite would contain, and part 2.5's chunk size makes the bug vanish on a periodic corpus. **#1,
contamination**, gets a mention in parts 1.5 and 2.1 for a specific reason: a document that appears
twice under two normalizations, or once correctly decoded and once as mojibake, is two different
documents to a hash-keyed deduplicator, so it survives deduplication and is trained on twice.

---

## §8 Verify before you code

Everything used today is the standard library. The symbols worth checking against the documentation for
**Python 3.12.12** — the version actually running here — were checked on **2026-08-26**:

| Symbol | What was checked | Why it matters today |
| --- | --- | --- |
| `unicodedata.normalize(form, s)` | takes the form as a string, one of four names; raises `ValueError` otherwise | the typo survives to run time — part 1.3 |
| `unicodedata.is_normalized(form, s)` | available from Python 3.8; answers without building a new string | the cheap guard in the boundary check |
| `unicodedata.name(ch)` | **raises `ValueError`** for code points with no name | the `try` in part 1.1 is required by the contract, not defensive |
| `unicodedata.ucd_3_2_0` | a second module object exposing the Unicode 3.2 database | part 2.4's growth figure comes from comparing it with the current table |
| `locale.getpreferredencoding(False)` | the encoding `open()` uses with no `encoding=`; `False` means do not re-read the locale | part 2.1's `cp1252` result |
| `codecs.getincrementaldecoder(enc)` | returns a decoder class; `decode(chunk, final=False)` retains partial sequences | part 2.5's fix, and the `final=True` flush |

Two external documents were fetched rather than recalled, both on **2026-08-26**:

| Cited | Revision | Dated | Unicode version | URL |
| --- | --- | --- | --- | --- |
| UAX #29, Unicode Text Segmentation | 41 | 2022-08-26 | 15.0.0 | `https://www.unicode.org/reports/tr29/tr29-41.html` |
| UAX #29, Unicode Text Segmentation | 43 | 2023-08-16 | 15.1.0 | `https://www.unicode.org/reports/tr29/tr29-43.html` |

The two revisions are cited together on purpose, and part 1.4 is built on the difference: revision 41
lists rules `GB1`–`GB13` and `GB999`; revision 43 adds `GB9c` for Indic conjuncts. **The definition of
"one character a person sees" changed between two Unicode releases**, which is the fact that disqualifies
the grapheme level as a vocabulary unit and hands the argument to bytes.

---

## §9 Say it in an interview

*"How long is a four-person family emoji?"* — "That has at least four answers and the right one depends
on who is asking: twenty-five UTF-8 bytes, seven code points, eleven UTF-16 code units, and one thing a
reader sees. The structure causing it is four people joined by three zero-width joiners — there is no
'family' code point anywhere in Unicode, it is an instruction to draw four things as one. Which is why
a length limit has to state its unit, and why a text pipeline should agree on one unit end to end."

*"Two identical-looking strings, one is in the dictionary and one is not. Where do you look?"* — "That
is almost always a normalization mismatch, not whitespace. `==` and `hash` work on code points, so I
would print `ascii()` of both and compare `unicodedata.normalize('NFC', …)` of both — if the normalized
forms match, the fix belongs at the boundary that let two spellings in, not at the comparison. And I
would check whether anything downstream has a `get(c, UNK)` fallback, because that turns a crash into a
quality regression nobody will attribute to this."

*"Why do modern tokenizers work at the byte level?"* — "It is a correctness argument. The byte set is
complete and fixed at 256, so out-of-vocabulary is impossible by construction. The assigned code point
set is not: I measured 95,221 characters in the Unicode 3.2 table CPython ships and 149,251 in the
current one, so a vocabulary frozen at the earlier version would emit `<unk>` for 54,030 characters that
exist today. The price is sequence length — 2.75 bytes per character on Devanagari against 1.00 on
English in my measurements, which is 7.56× the attention work — so byte-level is the floor under a
subword scheme, not the scheme itself."

*"You are streaming a large file and getting `UnicodeDecodeError` about half the time."* — "The chunk
boundary is landing inside a multi-byte character. The fix is an incremental decoder that carries the
partial bytes across the boundary, flushed at the end so a genuinely truncated file still raises. What
I would not do is add `errors='ignore'` — on a 10,000-byte test that dropped 95 characters out of
5,600 with no exception, and every single one was non-ASCII. And I would be careful about the test that
proves it fixed: the same code showed zero failures at one chunk size purely because that size divided
my test corpus's repeat period."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 10` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 10 | 2026-08-26 | TOK-03, TOK-04 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; everything used is the standard library.

`docs/DATASETS.md` — **no rows today**, and today the reason is stronger than Day 9's: there is no
corpus at all. Every string measured in this day is written out as escapes inside the part that uses
it, so there is nothing to license, nothing to download and nothing that can drift. **The first
`DATASETS.md` row is still Day 14's.**

`docs/MODELS.md` — **no rows today.** Nothing was downloaded and nothing was loaded.

`docs/RUNS.md` — **no rows today.** Nothing today trains. The one projected number in this day — part
2.4's `attention vs English` column — is labelled as arithmetic over a measured byte ratio, in the part
and again in §6, for exactly this reason.

Commit:

```text
day 010: Unicode, code points and bytes — closes TOK-03, TOK-04
```
