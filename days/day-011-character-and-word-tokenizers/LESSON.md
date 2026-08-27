---
day: 11
phase: 2
phase_name: "Tokenization"
title: "Character-level and word-level tokenizers, built — and where each one dies"
ids: ["TOK-05", "TOK-06"]
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

# Day 11 — Character-level and word-level tokenizers

> **Yesterday (Day 10):** what a character actually is — code points, graphemes and bytes — normalization,
> UTF-8, and the argument that only the 256 bytes form a set that is finished.
> **Today:** both obvious tokenizers, built as real modules with `save`, `load` and a hash, and then
> measured until each one breaks. One is lossless and enormous; the other is compact and cannot say the
> word.
> **Tomorrow (Day 12):** byte-pair encoding — the merge loop, run by hand on a toy corpus, then trained
> (TOK-07, TOK-08).

---

## §1 Where we are

Day 9 argued that words and characters both fail. Day 10 established what a character even is. Today you
build both tokenizers properly and find out what those arguments feel like as measured numbers on your
own machine.

The character tokenizer wins the argument nobody expected it to win: it is **lossless**. Encode the whole
corpus, decode it, and you get the corpus back, byte for byte — 151 entries, no exceptions, no fallbacks.
And then it loses on everything else. The same text is 5.56× longer in tokens, which is 30.9× the
attention work, and a 1,024-token context window that would hold 1,024 words holds **184**. That last
number is not a speed problem: no amount of compute makes the model see the second page.

The word tokenizer wins on all of those and then fails in a way that no setting repairs. Capped at 1,000
words it cannot represent 19.29% of held-out tokens. Uncapped — every single word type the training text
contained — it still cannot represent **10.41%**, and the words it loses average 6.60 characters against
4.07 for the ones it keeps, so it is preferentially deleting the words that carry the meaning. There is
nothing underneath a word to fall back on, so `the tokenizer <unk> its vocabulary and cannot <unk>
anything <unk>` is the best it can do, and **no id sequence in that vocabulary produces the word
`spell`** at all.

Two of the eleven parts are failures reproduced on purpose. In one, a `.get(ch, 0)` hotfix turns a
Russian greeting into six blank lines — because id 0 in a `sorted(set(text))` table is the newline — and
the reported loss on a corpus damaged that way goes **down** in proportion to the damage. In the other,
five ordinary output checks pass on a sentence with three words silently deleted from it.

Everything runs on the laptop with no packages. Every measurement is over one file already in this
repository, and **every script prints that file's sha256 first**, so a reader whose numbers differ knows
immediately why — which is Day 10's provenance lesson applied to this day's inputs.

---

## §2 The map

Eleven parts, three sections. Section 1 is TOK-05 — the character tokenizer, built and broken. Section 2
is TOK-06 — the word tokenizer, the same. Section 3 sorts the findings into trades and gates. The day
climbs `foundation → working → production` and each of the first two sections ends with something
breaking.

### Section 1 — `01-character-level`: TOK-05, lossless and enormous

From Day 9's nine lines to a module with an artifact and a hash, then the three ways it hurts: what
"character" means in code, how long the sequences get, and what it does with a character it has never
seen.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [From a script to a module](parts/01-character-level/1.1-from-a-script-to-a-module.md) | What does a class add that nine lines did not? | `foundation` |
| 1.2 | [What counts as a character, decided in code](parts/01-character-level/1.2-what-counts-as-a-character.md) | Which of five vocabularies is the one you are allowed to build? | `working` |
| 1.3 | [The sequence-length problem](parts/01-character-level/1.3-the-sequence-length-problem.md) | Which of the three costs can compute not fix? | `working` |
| 1.4 | [The unknown-character policy](parts/01-character-level/1.4-the-unknown-character-policy.md) | Raise, substitute or fall back — and why is the default the one that crashes? | `working` |
| 1.5 | [💥 The character tokenizer that met a new alphabet](parts/01-character-level/1.5-the-character-tokenizer-that-met-a-new-alphabet.md) | How does a `KeyError` become a falling loss curve? | `production` |

### Section 2 — `02-word-level`: TOK-06, compact and unable to spell

The same class with a splitter and a cap — then the wall, what the kept slots are actually spent on, and
the sentence the model can never say.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [What counts as a word](parts/02-word-level/2.1-what-counts-as-a-word.md) | Why does every splitter fail the contract before meeting an unknown word? | `foundation` |
| 2.2 | [Building a word vocabulary, with a cap](parts/02-word-level/2.2-building-a-word-vocabulary.md) | Why must a word tokenizer have a cap when a character one need not? | `working` |
| 2.3 | [The out-of-vocabulary wall](parts/02-word-level/2.3-the-out-of-vocabulary-wall.md) | What does keeping *every* training word still fail to cover? | `working` |
| 2.4 | [One meaning, six slots](parts/02-word-level/2.4-one-meaning-six-slots.md) | What are the slots you did keep actually spent on? | `production` |
| 2.5 | [💥 The word tokenizer that could not say the word](parts/02-word-level/2.5-the-word-tokenizer-that-could-not-say-the-word.md) | Why do five output checks pass on a sentence with three words deleted? | `production` |

### Section 3 — `03-together`: trades and gates

Both tokenizers, one held-out text, six columns — and the observation that one of the two gates has a
handle on it.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Two tokenizers, one table](parts/03-together/3.1-two-tokenizers-one-table.md) | Which failures are budgets and which are dead ends? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything is the standard library — `unicodedata`, `hashlib`, `json`, `re`,
`collections`, `pathlib`. Principle 3 is in force: the hand-rolled tokenizer exists before any library
is opened, and Day 14 is where the library arrives.

```bash
uv run python -c "import sys, unicodedata; print('python', sys.version.split()[0], '| unicodedata', unicodedata.unidata_version)"
uv run python -c "import hashlib, pathlib; print('corpus sha256[:16]', hashlib.sha256(pathlib.Path('docs/00_MASTER_PLAN.md').read_bytes()).hexdigest()[:16])"
./m scaffold 11
```

**Compare that second line against `9760f2b6d4340b97` and write down what you get.** Every measurement
in this day is over `docs/00_MASTER_PLAN.md` at one revision, and that file grows as this curriculum
does. A different hash does not make this day wrong — it means your corpus is a different corpus and
your numbers are the correct ones for it. **Every script in every part prints the hash first for exactly
this reason**, which is the habit Day 10 spent a whole day arguing for.

Two conventions the day uses throughout, both inherited from Day 10:

- **Non-ASCII test data is written as escapes and printed with `ascii()`.** The two spellings of an
  accented word are the same pixels, and on this machine `sys.stdout.encoding` is `cp1252`, so printing
  a combining accent raises.
- **The corpus is split by position, 80/20**, and the vocabulary is built from the training side only.
  Part [2.2](parts/02-word-level/2.2-building-a-word-vocabulary.md) explains why a random split would be
  worse and why measuring coverage on training text always gives zero.

Day 9 parts 2.1 and 2.3 and Day 10 parts 1.3 and 2.4 are referenced constantly. Rereading Day 9 part 2.1
— the round-trip contract — before starting is worth it, because today is largely about which tokenizers
can honour it.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `akshara/tokenizer/char.py` | [1.1](parts/01-character-level/1.1-from-a-script-to-a-module.md), [1.2](parts/01-character-level/1.2-what-counts-as-a-character.md), [1.4](parts/01-character-level/1.4-the-unknown-character-policy.md) | `CharTokenizer` — `NORM`, `from_text`, `encode`, `decode`, `save`, `load`, `sha256` |
| `akshara/tokenizer/word.py` | [2.1](parts/02-word-level/2.1-what-counts-as-a-word.md), [2.2](parts/02-word-level/2.2-building-a-word-vocabulary.md) | `WordTokenizer` — `PATTERN`, `UNK` at slot 0, `from_text(text, max_size)`, the same six methods |
| `days/day-011-character-and-word-tokenizers/lab/coverage.py` | [1.4](parts/01-character-level/1.4-the-unknown-character-policy.md), [2.3](parts/02-word-level/2.3-the-out-of-vocabulary-wall.md) | `coverage_report`, `CoverageReport`, `assert_source_is_covered` — **per source, never averaged** |
| `days/day-011-character-and-word-tokenizers/lab/compare.py` | [3.1](parts/03-together/3.1-two-tokenizers-one-table.md) | the six-column table, every row from **one** held-out variable |
| `tests/test_tokenizers.py` | [1.1](parts/01-character-level/1.1-from-a-script-to-a-module.md), [1.2](parts/01-character-level/1.2-what-counts-as-a-character.md), [2.1](parts/02-word-level/2.1-what-counts-as-a-word.md) | the corpus round trip, the probe round trip, the save/load hash, the pre-tokenizer losslessness test |

This is the first day that writes into `akshara/`. The tokenizer is a package module from here on; Day
12 adds `akshara/tokenizer/bpe.py` beside these two and Day 13 finishes it.

**`TODO(me)`:** part [2.4](parts/02-word-level/2.4-one-meaning-six-slots.md) found that 15.57% of the
word vocabulary is a stem plus a suffix, and that in this corpus the bare stem `learn` is *rarer* than
`learning`. Write down, in one paragraph and before reading Day 12, what you would have to count to
discover the piece `ing` **without** a suffix list — and why counting whole words can never find it.

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_tokenizers.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| add `.casefold()` inside `CharTokenizer.from_text` | `V` drops 151 → 125, corpus round trip fails | the corpus round-trip test |
| move `normalize` out of `encode`, leaving it in `from_text` | passes on ASCII, `KeyError` on a decomposed accent | the probe round-trip test |
| drop `sort_keys=True` from the `sha256` payload | same table, hash changes between runs | the save/load hash test |
| swap `WordTokenizer.PATTERN` for `r"[A-Za-z]+"` | `don't` becomes two tokens; the vocabulary changes | the pre-tokenizer losslessness test |

The second row is the one worth doing by hand. It passes every ASCII test and fails only on text
containing a combining mark, which is Day 10 part
[1.5](../day-010-unicode-code-points-bytes/parts/01-code-points-and-graphemes/1.5-the-string-that-was-not-equal-to-itself.md)
arriving inside code you wrote today.

The fourth row is the one to think about rather than just run: **the pre-tokenizer test cannot pass**, for
any word-level splitter, because part [2.1](parts/02-word-level/2.1-what-counts-as-a-word.md) measured
that all five lose the whitespace. Write the test so that it asserts the property, watch it fail, and
then decide deliberately whether to mark it as an expected failure or to keep it red as a standing
reminder. **A test you cannot make pass is telling you something about the design, not about the test.**

---

## §6 Compute budget

**Tier: T0.** Python's standard library on a laptop CPU, over a 113,283-byte file already in this
repository.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — nothing installed, nothing downloaded |
| Disk | negligible; the largest artifact written is a 1,286-byte tokenizer file |

What T0 proves: **every claim in this day.** The vocabulary sizes, the coverage curve, the sequence-length
ratio, the morphology share, the `<unk>` counts and the six-column table are all exact counts over one
file, plus arithmetic. There is no seed, no timing and no hardware dependence anywhere.

What T0 **cannot** show is the question underneath the whole day: which scheme trains a better model at
fixed compute. That needs runs, it is Day 17, and today deliberately decides what it can on **correctness**
grounds instead — losslessness and coverage are properties of a table, countable without a GPU, and they
narrow the field before a single run is spent.

Three labels to read carefully, all of them stated in the parts as well:

- The `30.9×` attention multiplier in part [1.3](parts/01-character-level/1.3-the-sequence-length-problem.md)
  is **arithmetic from a measured token ratio**, not a benchmark. Day 31 is where attention gets timed.
- The loss table in part [1.5](parts/01-character-level/1.5-the-character-tokenizer-that-met-a-new-alphabet.md)
  is **arithmetic over an explicitly described, deliberately stupid model**. It establishes the direction
  of the bias, which is the claim; the magnitude is Day 17's.
- The `15.57%` in part [2.4](parts/02-word-level/2.4-one-meaning-six-slots.md) is a **lower bound** from a
  nine-suffix heuristic, not a morphological analysis, and the function's own key names say so.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Rebuilding the tokenizer from the corpus at serving startup | a different table the moment the corpus changes; every id above the insertion shifts | [1.1](parts/01-character-level/1.1-from-a-script-to-a-module.md) |
| `.casefold()` or `.lower()` in `from_text` | `V` drops 17%, and the model can never emit a capital letter | [1.2](parts/01-character-level/1.2-what-counts-as-a-character.md) |
| Sizing a byte vocabulary from a corpus | 143 distinct bytes here; the answer is 256 whatever the corpus says | [1.2](parts/01-character-level/1.2-what-counts-as-a-character.md) |
| `ids[:block_size]` in the serving path | valid batches, right shapes, the model sees the first 184 words | [1.3](parts/01-character-level/1.3-the-sequence-length-problem.md) |
| `stoi.get(ch, 0)` to stop a `KeyError` | id 0 is the newline; foreign text becomes blank lines | [1.4](parts/01-character-level/1.4-the-unknown-character-policy.md) |
| An averaged fallback rate | 2% overall while one source is at 100% | [1.4](parts/01-character-level/1.4-the-unknown-character-policy.md), [1.5](parts/01-character-level/1.5-the-character-tokenizer-that-met-a-new-alphabet.md) |
| Partial script coverage | 3 of 4 Devanagari characters present; the failure is intermittent | [1.5](parts/01-character-level/1.5-the-character-tokenizer-that-met-a-new-alphabet.md) |
| A regex written without `r"..."` | `SyntaxWarning`, and a pattern that is not what you wrote | [2.1](parts/02-word-level/2.1-what-counts-as-a-word.md) |
| `re.findall(r"[A-Za-z']+", "3.14")` | `[]` — the document encodes to zero tokens, no error | [2.1](parts/02-word-level/2.1-what-counts-as-a-word.md) |
| Measuring OOV against the text the vocabulary was built from | `12.33%` instead of the honest `19.29%` — plausible and wrong | [2.3](parts/02-word-level/2.3-the-out-of-vocabulary-wall.md) |
| Confusing `max_size` with `V` | cap 1000 gives `V = 1001`; an embedding sized from the config is one row short | [2.2](parts/02-word-level/2.2-building-a-word-vocabulary.md) |
| Reading a comparison cell without its conditions | "character-level has no OOV problem" — true in-distribution, false on Cyrillic | [3.1](parts/03-together/3.1-two-tokenizers-one-table.md) |

Three of the plan's five silent failures are live today. **#1, contamination**, is part
[2.2](parts/02-word-level/2.2-building-a-word-vocabulary.md)'s split discipline and part 2.3's
`12.33%`-versus-`19.29%` measurement — evaluating on data the artifact was built from. **#2,
tokenizer/template mismatch**, is part [1.1](parts/01-character-level/1.1-from-a-script-to-a-module.md)'s
whole reason for existing: the hash exists so that a mismatch is loud. **#5, evaluated on the format you
trained on**, appears in part [3.1](parts/03-together/3.1-two-tokenizers-one-table.md) as two cells that
are in-distribution artefacts, and in part 1.5 as an English test suite that passes on a tokenizer which
cannot read four of five scripts.

---

## §8 Verify before you code

Everything used today is the standard library. The symbols worth checking against the documentation for
**Python 3.12.12** — the version actually running here — were checked on **2026-08-26**:

| Symbol | What was checked | Why it matters today |
| --- | --- | --- |
| `collections.Counter.most_common(n)` | returns the `n` most common; ties broken by insertion order | the cap's tie-break is not defined by frequency — part 2.2 |
| `re.findall(pattern, s)` | returns all non-overlapping matches, left to right; groups change the result | the splitter comparison — part 2.1 |
| `re` and `\w` | matches Unicode word characters by default in Python 3 | the difference between one-language and many-language splitting |
| `json.dumps(..., ensure_ascii=True)` | escapes every non-ASCII character in the output | the tokenizer file stays pure ASCII and reviewable — part 1.1 |
| `json.dumps(..., sort_keys=True)` | sorts by key, producing stable bytes | the hash is over contents, not over dict order |
| `str.casefold()` | more aggressive than `lower()`; not reversible | the transform that breaks the contract — part 1.2 |
| `unicodedata.normalize(form, s)` | four forms; `NFC`/`NFD` lossless, `NFKC`/`NFKD` not | inherited from Day 10 part 1.3 |
| `dict` insertion order | guaranteed from Python 3.7 | why printing a splitter table's header separately is safe |

No external documents were fetched today; nothing in this day depends on a standard outside Python's own
documentation, and the Unicode facts it uses were fetched and cited on Day 10.

---

## §9 Say it in an interview

*"Character-level or word-level?"* — "Neither, and the numbers say why. Character-level is lossless — I
round-tripped 110,837 characters exactly — and costs 5.56× the tokens, which is 30.9× the attention work
and turns a 1,024-token context window into 184 words. Word-level is compact and cannot represent 10.41%
of held-out tokens even with no cap at all, because there is nothing underneath a word to fall back on.
The first is a trade you can budget for; the second is a gate."

*"Your loss dropped after a data pipeline change. What do you check?"* — "Whether the data got easier
rather than the model getting better. I have seen a `.get(ch, 0)` fallback turn a whole language into
newlines — id 0 in a `sorted(set(text))` table is the newline — and newlines are trivially predictable,
so the reported loss falls in proportion to how much text was destroyed. I would look at the token
distribution for a spike in one id, and round-trip a sample of every source."

*"How do you split text into words?"* — "The question has no language-independent answer, so the real
question is which pre-tokenization rule, and the property that decides it is whether the pieces reassemble
exactly. On my corpus, `split()` gave 5,494 types with 64% of them occurring once, mostly punctuation
variants; a letters-only regex silently produced zero tokens for `3.14`; and none of the five splitters I
tried reconstructed the corpus. That is why real pre-tokenizers keep whitespace as part of the token."

*"Why do subword tokenizers work so well?"* — "Three things at once. In my corpus, 15.57% of the word
vocabulary was a stem plus a common suffix, and no single form of `learn` had more than nine observations
while the family had 25 between them — so a shared stem token pools the statistics, frees the slots the
inflections were using, and lets the model spell a form it has never seen. And it finds the pieces from
frequency alone, with no grammar and no per-language rules."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 11` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 11 | 2026-08-26 | TOK-05, TOK-06 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; everything used is the standard library.

`docs/DATASETS.md` — **no rows today.** Every measurement is over `docs/00_MASTER_PLAN.md`, a file in
this repository under this repository's own licence. It was not downloaded and it is not a dataset. The
first `DATASETS.md` row is still Day 14's.

`docs/MODELS.md` — **no rows today.** Nothing was downloaded and nothing was loaded.

`docs/RUNS.md` — **no rows today.** Nothing today trains. The two projected figures — part 1.3's `30.9×`
and part 1.5's loss table — are labelled as arithmetic in their parts and again in §6, for exactly this
reason.

Commit:

```text
day 011: Character-level and word-level tokenizers — closes TOK-05, TOK-06
```
