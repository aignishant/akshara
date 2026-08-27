# Day 12 — CHECKLIST

**IDs closed:** TOK-07, TOK-08
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0 · longest step 50.8 s

> `./m done 12` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **written** count reads 13, then one commit reading
`day 012: BPE from scratch I, the merge loop — closes TOK-07, TOK-08`.

---

## Setup

- [ ] Day 11's checklist is fully ticked and `./m done 11` committed
- [ ] `./m scaffold 12` run; the lab directory exists
- [ ] **No packages installed today** — confirmed; everything used is the standard library
- [ ] The corpus sha256 printed and compared against `9760f2b6d4340b97`; you recorded yours
- [ ] Day 11 part 2.5 re-read — you can quote the sentence the word tokenizer could not say
- [ ] You know that training is slow here and have decided to train once and reuse, not retrain in a loop

## TOK-07 — the merge loop (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] Can state the four steps of the merge rule from memory
- [ ] Can say what `V` is in terms of the alphabet and the merge count
- [ ] Can explain why an unseen word is not a problem for BPE and was for Day 11's word tokenizer
- [ ] Reproduced the tie between `lo` and `ow` and can say which wins and why
- [ ] Ran the unweighted version (`+= 1`) and can say what kind of tokenizer it produces
- [ ] Read 1.2; ran its check-yourself
- [ ] Traced six merges by hand and checked at least two of the pair counts by counting letters
- [ ] Saw `est` appear, and can say what told the algorithm to look for a suffix (nothing)
- [ ] Can say why each merge saves exactly the pair's count, and what that implies about the curve
- [ ] Can explain how a five-character token comes out of an algorithm that only merges pairs
- [ ] Read 1.3; ran its check-yourself
- [ ] Ran the loop to exhaustion and saw every word become one token
- [ ] Can name the two conditions that stop the loop on their own, and what the tokenizer has become
- [ ] Can say why the alphabet is a floor that no target can go below, and what happens if you ask for less
- [ ] Read 1.4; ran its check-yourself
- [ ] Can name the two jobs a pre-tokenizer does
- [ ] Confirmed `"".join(chunks) == text` for your pattern — and confirmed it is `False` for `r"\S+"`
- [ ] Can say why a token in this scheme may begin with a space
- [ ] Read 1.5; ran its check-yourself
- [ ] Trained with and without the pre-tokenizer and counted the boundary tokens in each
- [ ] Can name three costs of letting merges cross a word boundary
- [ ] Confirmed that the round trip holds for **both** tokenizers, and can say what that means about
      losslessness as a test
- [ ] Noticed that the worse tokenizer compresses **better** on the training text, and can say why that
      is the wrong thing to compare

## TOK-08 — training a vocabulary (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] `akshara/tokenizer/bpe.py` written by hand, with `save`, `load` and `sha256`
- [ ] Can name the three fields a BPE tokenizer file must contain
- [ ] Shuffled the merge list and measured the token count change on a probe
- [ ] Confirmed **both** the ordered and the shuffled version round-trip, and can say why that matters
- [ ] Can say why the merges cannot be stored as a set, sorted, or as a JSON object
- [ ] Read 2.2; ran its check-yourself
- [ ] Trained at three or more target sizes and recorded characters per token for each
- [ ] Can state where the character and word tokenizers sit on the characters-per-token scale
- [ ] Computed the gain **per merge spent** and can say which direction it moves
- [ ] Can say why compression measured on training text is fine for this question and not for others
- [ ] Read 2.3; ran its check-yourself
- [ ] Printed the first two dozen merges and read them
- [ ] Identified at least three merges that are formatting rather than language
- [ ] Found at least two English suffixes the merges discovered
- [ ] Printed the longest tokens and can say what they tell you about the corpus
- [ ] Encoded a word with no single token and watched it decompose — and round-trip
- [ ] Confirmed the alphabet still fails on an unseen script, and can say why no number of merges helps
- [ ] Read 2.4; ran its check-yourself
- [ ] Can state the cost shape of the naive trainer in terms of its two factors
- [ ] Measured the collapse factor on your own corpus and can say which line of part 1.1 earns it
- [ ] Noticed the per-merge cost **falling** as training proceeds, and can explain it
- [ ] Projected the cost for a larger corpus and can state the assumption the projection rests on
- [ ] Wrote the `TODO(me)` paragraph on what an indexed trainer would have to store — **before** Day 14
- [ ] Read 2.5; ran its check-yourself
- [ ] Reproduced two merge lists diverging from the same words in a different order
- [ ] Can say exactly where the nondeterminism enters an algorithm with no random number generator
- [ ] Can write the one-line fix and say why the tuple makes the tie-break total
- [ ] Can name three checks that pass on **both** of the two different tokenizers

## Section 3 — together

- [ ] Read 3.1; ran its check-yourself
- [ ] Built the three-row table on your own machine, every row from **one** text variable
- [ ] Can say which of Day 11's five findings Day 12 closed and which it did not
- [ ] Can say why the word tokenizer's compression figure is not comparable with the other two
- [ ] Encoded Day 11 part 2.5's sentence with BPE and compared the two outputs side by side
- [ ] Can state the one-line change that closes the remaining gate

## The eval that can go red (Principle 11)

- [ ] `tests/test_bpe.py` exists and runs CPU-only, offline, deterministically
- [ ] **Observed red before green:** changed the tie-break to `max(pairs, key=pairs.get)` → the
      order-independence test failed
- [ ] Confirmed that same change **passes** a test comparing only the first ten merges — and can say why
- [ ] **Observed red before green:** dropped the lookahead guard in `merge_word` → the toy fixture failed
- [ ] **Observed red before green:** changed `PATTERN` to `r"\S+"` → the tiling assertion failed
- [ ] **Observed red before green:** stored the merges as a JSON object → the artifact round trip failed
- [ ] The toy-trace fixture is hand-checked: you verified at least two of its expected pair counts by
      counting letters yourself

## Silent failures ruled out (plan §6)

- [ ] **#2 tokenizer/template mismatch** — you can describe two artifacts with the same `V`, both
      lossless, that produce different ids, and name the one check that distinguishes them
- [ ] **#4 noise mistaken for improvement** — you can explain how removing the pre-tokenizer improves
      compression while making the tokenizer worse, and name the metric that misled you

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with the corpus hash beside it
- [ ] You did **not** copy this day's `1.72`, `2.07`, `2.63`, `3.30`, `42130`, `349`, `16 of 60`,
      `merge 24`, `5863` or `3.46x` figures into your notes as if they were yours
- [ ] Your training **durations** are recorded with your own hardware line — and you can say which
      numbers in this day are hardware-dependent and which are not
- [ ] Part 2.4's projections are labelled in your notes as **arithmetic under a stated assumption**
- [ ] Part 2.5's shuffle seed is recorded, and you ran it with a second seed
- [ ] Where your corpus hash differed from this document's, you **recorded that** and did not reuse this
      document's merge list

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] Longest single step recorded, with hardware
- [ ] You can name the one question about tokenization schemes this day **cannot** answer, and which day
      answers it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md` — **confirmed no rows**
- [ ] `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can say why tokenizer training is not a run row
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-07 and TOK-08 closed on day 12
- [ ] `./m done 12` committed with the message from §11
