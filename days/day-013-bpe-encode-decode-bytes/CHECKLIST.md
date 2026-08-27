# Day 13 — CHECKLIST

**IDs closed:** TOK-09, TOK-10, TOK-11
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18
**Parts:** 13 across 4 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0 · longest step 33.7 s

> `./m done 13` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **written** count reads 14, then one commit reading
`day 013: BPE II — encode, decode, the pre-tokenizer and bytes — closes TOK-09, TOK-10, TOK-11`.

---

## Setup

- [ ] Day 12's checklist is fully ticked and `./m done 12` committed
- [ ] `./m scaffold 13` run; the lab directory exists
- [ ] **No packages installed today** — confirmed; Day 14 is the first day that installs anything
- [ ] Corpus sha256 printed and compared against `9760f2b6d4340b97`; yours recorded
- [ ] You trained once at `V = 1000`, saved the merge list, and reused it — you did not retrain per part

## TOK-09 — encode and decode (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] `encode_chunk` written by hand, with `is not None` on the rank
- [ ] Kept Day 12's sequential encoder as a **test oracle** and can say why
- [ ] Measured the speed ratio on your own machine and confirmed the outputs are identical
- [ ] Broke it with `if r:` and can say why rank 0 is the dangerous one
- [ ] Read 1.2; ran its check-yourself
- [ ] Built two id sequences of different lengths that decode to the same string
- [ ] Can say which direction of the round trip always holds and which does not
- [ ] Can name two ordinary things in a serving path that produce non-canonical ids
- [ ] Read 1.3; ran its check-yourself
- [ ] Can state `V = 256 + len(merges)` and say why it is knowable before the corpus is read
- [ ] Verified that ids 0..255 are the byte symbols, in order
- [ ] Can say what an id below 256 tells you about that position in the word
- [ ] Can say why nothing derived from the merge list is stored in the tokenizer file
- [ ] Read 1.4; ran its check-yourself
- [ ] Reproduced a replacement character in the middle of a correct id sequence
- [ ] Wrote `StreamingDecoder` and confirmed it agrees with batch decoding
- [ ] Deleted the `final=True` flush and can say exactly what went missing
- [ ] Your streaming probe list contains a multi-byte character — you checked that it *can* fail

## TOK-10 — the regex pre-tokenizer (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Can name four ordinary strings Day 12's pattern keeps as one chunk and this one splits
- [ ] Can say which direction compression moves when you add boundaries, and why that means compression
      is the wrong way to choose a pre-tokenizer
- [ ] Read 2.2; ran its check-yourself
- [ ] Can name the seven branches of the published pattern in order
- [ ] Can say what the optional leading space in four of them is for
- [ ] Can say what `(?!\S)` forces the whitespace branch to give up, and what it matters for
- [ ] Confirmed `\p{L}` raises in stdlib `re`, and can say what you would install to use it
- [ ] Ran the ASCII-only letter class on a non-Latin word and saw the pattern stop tiling
- [ ] Read 2.3; ran its check-yourself
- [ ] Trained with both patterns and recorded compression, distinct chunks and training time
- [ ] Can explain why the trainer got **faster** when the chunk count went up
- [ ] **Ran the naive merge audit and the byte-aware one, and can say why they disagree**
- [ ] Can name the one mixed-kind merge that survives, and say why it is there by design
- [ ] Read 2.4; ran its check-yourself
- [ ] Encoded six numbers and recorded six different grouping shapes
- [ ] Can say why the letter/digit boundary does not help inside a number
- [ ] Applied the three-digit cap and can say what it fixes and what it does not
- [ ] Wrote the `TODO(me)` paragraph on what you would measure to know whether the cap helps a **model**

## TOK-11 — byte-level BPE (section 3)

- [ ] Read 3.1; ran its check-yourself
- [ ] Made the one-line change and retrained
- [ ] Can name the two properties it buys and the one it costs
- [ ] Can say why the compression gap at `V = 500` is arithmetic rather than a fact about bytes
- [ ] Read 3.2; ran its check-yourself
- [ ] `bytes_to_unicode` written by hand, with `cs = bs[:]`
- [ ] Asserted the bijection: 256 keys, 256 distinct printable non-space values, exact inverse
- [ ] Can say which byte `Ġ` stands for and how many bytes map to themselves
- [ ] Read 3.3; ran its check-yourself
- [ ] Round-tripped five scripts, the empty string and whitespace — **with no `try` anywhere**
- [ ] Can state the difference between a coverage percentage and a coverage construction
- [ ] Can write the one-line check that establishes the construction
- [ ] Noticed the Cyrillic row costs one token per byte, and can say what that means
- [ ] Read 3.4; ran its check-yourself
- [ ] Found the merges that reassemble a multi-byte character and decoded them
- [ ] Can say what merges 16 and 20 are tokens *for* (nothing)
- [ ] Measured the non-ASCII and incomplete merge counts on your own corpus
- [ ] Can say which end of the merge list the tax falls on and why that matters

## Section 4 — together

- [ ] Read 4.1; ran its check-yourself
- [ ] Built the four-row table from **one** `text` variable
- [ ] Can list Day 11's five findings and say which day closed each and at what cost
- [ ] Can say why `coverage` is a string column rather than a numeric one
- [ ] Can name three things Day 13 did **not** fix

## The eval that can go red (Principle 11)

- [ ] `tests/test_bpe_bytes.py` exists and runs CPU-only, offline, deterministically
- [ ] **Observed red before green:** `if r:` instead of `if r is not None` → the oracle test failed
- [ ] **Observed red before green:** per-prefix decoding → the streaming test failed on a multi-byte probe
- [ ] Confirmed that same change **passes** on an English-only probe list — and can say why
- [ ] **Observed red before green:** `cs = bs` → the bijection test failed
- [ ] **Observed red before green:** vocabulary without the byte block → the coverage assertion failed
- [ ] The coverage assertion takes **no probes** and you can say why that makes it stronger

## Silent failures ruled out (plan §6)

- [ ] **#2 tokenizer/template mismatch** — you can describe two ways it appears today (non-canonical ids
      from concatenation; a merge list encoded under the wrong pattern) and say what catches each
- [ ] **#5 evaluated on the format you trained on** — you can name two checks in this day that pass on an
      English-only probe list while the code is broken

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with the corpus hash beside it
- [ ] You did **not** copy this day's `93x`, `2.39`, `2.51`, `46311`, `744`, `4.0%`, `0.24` or `18.2s`
      figures into your notes as if they were yours
- [ ] Your **timings** carry your own hardware line, and you can say which numbers in this day are
      hardware-dependent and which are not
- [ ] Your notes record that `GPT_LIKE` is a **stdlib approximation**, and name at least two differences
      from the published pattern
- [ ] Part 3.4's Devanagari scaling is labelled in your notes as **arithmetic under a stated ratio**
- [ ] Part 3.3's random-blob seed is recorded, and you can say why the id counts exceed 64

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] Longest single step recorded, with hardware
- [ ] You can name the one question this day **cannot** answer, and which day answers it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**, and you know Day 14 is the first day with any
- [ ] `docs/DATASETS.md` — **confirmed no rows**
- [ ] `docs/MODELS.md` — **confirmed no rows**, and you can say why reading a source file on the web is
      not a model row
- [ ] `docs/RUNS.md` — **confirmed no rows**
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-09, TOK-10 and TOK-11 closed
      on day 13
- [ ] `./m done 13` committed with the message from §11
