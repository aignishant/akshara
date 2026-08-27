# Day 10 — CHECKLIST

**IDs closed:** TOK-03, TOK-04
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 10` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **complete** count has gone up by one and whose
**written** count reads 11, then one commit reading
`day 010: Unicode, code points and bytes — closes TOK-03, TOK-04`.

> **Read the status line carefully before ticking anything.** `./m status` distinguishes days
> *written* from days *complete*, and a day is complete only when its row is in `docs/PROGRESS.md`. If
> the complete count is `0` while the written count is `11`, the ledger and the repository disagree —
> **fix that before starting Day 11**, because `./m done` and the day generator both read the ledger,
> not the folders.

---

## Setup

- [ ] Day 9's checklist is fully ticked and `./m done 9` committed
- [ ] `./m scaffold 10` run; the lab directory exists
- [ ] **No packages installed today** — confirmed; everything used is the standard library
- [ ] `unicodedata.unidata_version` printed and **written down** — you can say which half of this day
      depends on it and which half does not
- [ ] `locale.getpreferredencoding(False)` printed on your machine, and you can say what `open(path)`
      would do with no `encoding=`
- [ ] Day 9 part 2.1 re-read — you can state the one property that makes two functions a tokenizer

## TOK-03 — what a character is (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] Can name the three things the word "character" can mean, and which one `len()` counts
- [ ] Reproduced four different lengths for one family emoji on your own machine
- [ ] Can say which of the three levels has a set that is finished
- [ ] Read 1.2; ran its check-yourself
- [ ] Can name the unit every Python string operation works on
- [ ] Sliced a word between a letter and its accent and got a **valid string with the accent gone**,
      with no exception
- [ ] Can name one job where code points are the right unit and two where they are wrong
- [ ] Read 1.3; ran its check-yourself
- [ ] Can name the two independent choices that produce the four normalization forms
- [ ] Can say which two forms you may store and which two you may not, and what the `K` does
- [ ] Saw `NFC` turn `U+0958` into **two** code points, and can say what that does to "NFC is shortest"
- [ ] Measured how many code points each form rewrites, on your own machine
- [ ] Read 1.4; ran its check-yourself
- [ ] Confirmed for yourself that the standard library has **no** grapheme function
- [ ] Scored the naive approximation and got **four of ten**, then six of ten with one rule added
- [ ] Can say why a regional indicator's `category` makes the flag row impossible to get right by
      category alone
- [ ] Can say what changed about grapheme rules between Unicode 15.0 and 15.1, and why that matters for
      a stored "character count"
- [ ] **Checked the `seen` column against your own screen** and recorded any row where your renderer
      disagrees
- [ ] Read 1.5; ran its check-yourself
- [ ] Reproduced `a == b` being `False` for two words that draw identically
- [ ] Saw a `set` of four identical-looking names deduplicate to **two**, and to one after `NFC`
- [ ] Built two vocabularies with the **same size and different hashes** from the same text
- [ ] Saw the `KeyError` land on a combining accent rather than on a word
- [ ] Added `vocab.get(c, 0)`, watched the error disappear, and can say what it cost

## TOK-04 — the byte layer (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Can say what a byte sequence records about which encoding produced it
- [ ] Reproduced mojibake: five characters out where four went in, **no exception**
- [ ] Ran the file round trip and saw what `read_text()` with no `encoding=` does on your machine
- [ ] Can name the four `errors=` handlers and say which one round-trips and which one deletes data
- [ ] Read 2.2; ran its check-yourself
- [ ] Can state what the first byte announces and what every following byte starts with
- [ ] Encoded one code point **by hand** and checked it against Python's encoder
- [ ] Counted the byte values that never appear in valid UTF-8 and can say why `c0` is one of them
- [ ] Can name the three properties that made UTF-8 win, and what each one bought
- [ ] Read 2.3; ran its check-yourself
- [ ] Can state the one-line bit test for a continuation byte
- [ ] Measured the walk-back distance for every offset and saw the maximum is **three**
- [ ] Wrote `truncate_bytes` and can name one thing it guarantees and one thing it does not
- [ ] Can say why UTF-16 has no equivalent property at the byte level
- [ ] Read 2.4; ran its check-yourself
- [ ] Measured the assigned-character count in **both** Unicode tables CPython ships
- [ ] Encoded a mixed-script string with a 256-entry vocabulary, with **no `try` anywhere**
- [ ] Can say why the byte vocabulary has 256 entries and not 243
- [ ] Can state the byte-level out-of-vocabulary rate and why it is that number rather than a small one
- [ ] Can name the price with a measured multiplier, and say which day buys it back
- [ ] Read 2.5; ran its check-yourself
- [ ] Reproduced a majority of chunks raising, and can read the two error messages apart
- [ ] Saw `errors='ignore'` lose characters silently, and **counted them**
- [ ] Confirmed every lost character was non-ASCII
- [ ] Found the chunk size at which **zero** chunks raise, and can say why that is a property of the
      corpus and not of the code
- [ ] Used an incremental decoder, including the `final=True` flush, and can say what the flush catches

## Section 3 — together

- [ ] Read 3.1; ran its check-yourself
- [ ] Built the eight-row table on your own machine and got five different totals
- [ ] Can say which column is settled by a property none of the others has, and name that property
- [ ] Can state the largest-to-smallest ratio across the five totals
- [ ] Added a string in a script you actually use, predicted which column would grow fastest, and
      checked whether you were right
- [ ] Adopted the naming rule: **no variable, field or JSON key called `length` or `size`**

## The eval that can go red (Principle 11)

- [ ] `tests/test_unicode.py` exists and runs CPU-only, offline, with no seed needed
- [ ] **Observed red before green:** changed a `0x3F` mask to `0x7F` → the all-code-points encoder test
      failed
- [ ] Confirmed that same change **passes** on a sampled test of Latin and Devanagari — and can say why
- [ ] **Observed red before green:** deleted the walk-back in `truncate_bytes` → the safe-cut test failed
- [ ] **Observed red before green:** swapped `decode_stream` for per-chunk `errors="ignore"` → the
      chunked-decode test failed on a byte-count comparison, not a length comparison
- [ ] The encoder test iterates **all** valid code points, not a list of interesting ones — you checked
      that it *can* fail

## Silent failures ruled out (plan §6)

- [ ] **#2 tokenizer/template mismatch** — you can state the check the plan prescribes and you wrote it
      as a function with the form in a module-level constant
- [ ] **#5 evaluated on the format you trained on** — you can name the two places today where a test
      would have passed with the bug fully present, and say what you would add to the fixtures
- [ ] **#1 contamination** — you can explain how two normalizations of one document, or one document
      plus its mojibake twin, survive a hash-keyed deduplicator

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with hardware and date — or cited
- [ ] You did **not** copy this day's `13233`, `149251`, `95221`, `54030`, `2.75`, `7.56`, `139`, `95`,
      `60.9%` or `70` figures into your notes as if they were yours
- [ ] Every count you recorded says **which Unicode version** produced it, or says that it does not
      depend on one
- [ ] The `seen` counts in your notes are labelled as **a claim about what you saw**, not as a
      measurement
- [ ] Part 2.4's `attention vs English` column is labelled in your notes as **arithmetic over a measured
      byte ratio**, not as a timing
- [ ] Where your machine disagreed with this document — encoding defaults especially — you **recorded
      the disagreement**

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can name the one question about byte-level tokenization this day **cannot** answer, and which
      day answers it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md` — **confirmed no rows**, and you can say why today has no corpus at all
- [ ] `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can say why part 2.4's multiplier is not a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-03 and TOK-04 closed on
      day 10
- [ ] `./m done 10` committed with the message from §11
