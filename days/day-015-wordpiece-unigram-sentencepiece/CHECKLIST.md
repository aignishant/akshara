# Day 15 — CHECKLIST

**IDs closed:** TOK-14, TOK-15
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18
**Parts:** 13 across 4 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0 · longest step 39.0 s

> `./m done 15` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **written** count reads 16, then one commit reading
`day 015: the other families — WordPiece, Unigram and SentencePiece — closes TOK-14, TOK-15`.

---

## Setup

- [ ] Day 14's checklist is fully ticked and `./m done 14` committed
- [ ] `./m scaffold 15` run; the lab directory exists
- [ ] `sentencepiece` version looked up **live** on PyPI, not recalled
- [ ] `uv add "sentencepiece==0.2.2"` run with an exact pin; `uv.lock` committed
- [ ] Licence read from the installed `METADATA`, and you noticed PyPI's JSON returns `null` for it
- [ ] `docs/PACKAGES.md` row written, dated
- [ ] **`docs/MODELS.md` — confirmed no rows**, and you can say why today needs none
- [ ] Corpus sha256 printed and compared against `9760f2b6d4340b97`; yours recorded

## TOK-14 — WordPiece (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] Wrote both scoring rules and can state the one line that differs
- [ ] **Saw the unguarded likelihood rule pick a pair seen once, scoring 1.0**
- [ ] Swept `min_frequency` and watched the answer become sensible
- [ ] Can say why BPE's rule needs no such guard
- [ ] Read 1.2; ran its check-yourself
- [ ] Counted the `##` entries in your own vocabulary and the strings existing in both positions
- [ ] Can name the three whitespace conventions and say which one collides with real text
- [ ] Asserted that a token and its `##` form have different ids
- [ ] Read 1.3; ran its check-yourself
- [ ] **`wordpiece_encode` written by hand and agreeing with the library on every probe**
- [ ] Traced `dollars` by hand and can say why position 2 gave `##l` and not `##ll`
- [ ] **Shuffled the vocabulary and confirmed nothing changed** — and can say why a BPE merge list differs
- [ ] Confirmed the length guard fires at 101 characters and not at 99
- [ ] Read 1.4; ran its check-yourself
- [ ] Measured the `[UNK]` rate on the training corpus and got **zero**
- [ ] Measured it on words your corpus does not contain and got **all of them**
- [ ] **Confirmed `[UNK]` decodes to the empty string**, and found the `skip_special_tokens` default
- [ ] Measured the `#` characters destroyed by the marker collision on your own corpus
- [ ] Ran the same words through your Day 13 byte-level tokenizer and got exact round trips

## TOK-15 — Unigram (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Counted your own candidate pool and the fraction pruned
- [ ] **Measured training time falling as `V` rises**, and can explain it from the direction of travel
- [ ] Can say why the timing comparison against Day 12's BPE proves less than it appears to
- [ ] **Found that `.tokens` reports `'é'` while the id is `0`** — and can state the rule that follows
- [ ] Read 2.2; ran its check-yourself
- [ ] Sorted the vocabulary by score and read what the top says about your corpus
- [ ] Summed the probability mass and got something just under 1.0; can say where the rest went
- [ ] Can say why `<unk>` scoring `0.0` is a sentinel and not a probability
- [ ] Demonstrated the underflow that makes log space mandatory
- [ ] Read 2.3; ran its check-yourself
- [ ] **`viterbi` written by hand and agreeing with brute force *and* the library**
- [ ] Enumerated every segmentation of one word and scored them all
- [ ] Can state the recurrence in one sentence and say why `best[0] = 0.0`
- [ ] Confirmed `<unk>` in the score table is **inert** here, and can say why
- [ ] Read 2.4; ran its check-yourself
- [ ] Sampled 400 encodings at two `alpha` values and saw the argmax share move
- [ ] **Measured the token overhead** on your corpus (mine: 42%)
- [ ] Confirmed every sampled encoding still round-trips
- [ ] Recorded that your counts are samples, with the spread, not single numbers
- [ ] Read 2.5; ran its check-yourself
- [ ] **Watched `assert_same_tokenizer(t, t)` fail against the same object**
- [ ] Counted distinct id sequences from 50 calls
- [ ] Wrote the guarded version that raises `ValueError`, not `AssertionError`
- [ ] Ran the positive control: with sampling off, the guarded check passes
- [ ] Can say what Day 14's check assumed without writing it down

## TOK-15 — SentencePiece (section 3)

- [ ] Read 3.1; ran its check-yourself
- [ ] Ran the whitespace probes and found **which two do not round-trip**
- [ ] Can name the flag that eats a leading space, and the Day 14 part it is
- [ ] **Measured that a tab is destroyed by the decoder**, and that your corpus hides it
- [ ] Counted cross-word tokens and got zero; can say which parameter forbids them
- [ ] Asserted U+2581 does not occur in your corpus
- [ ] Read 3.2; ran its check-yourself
- [ ] Trained with and without `byte_fallback` and **measured the compression cost**
- [ ] Confirmed exactly 256 `<0xNN>` entries appear
- [ ] **Tested on scripts absent from your corpus**, asserted absent first
- [ ] Saw `DecodePieces` round-trip where `Decode(ids)` does not, and can say why
- [ ] Can state the difference between a coverage percentage and a coverage construction
- [ ] Read 3.3; ran its check-yourself
- [ ] **Measured the corpus loss from the default normalizer** — mine 1.24%
- [ ] Named the characters destroyed, including the two compatibility foldings
- [ ] Ran `Normalize` directly, without training, as the cheap audit
- [ ] Turned all three flags off and confirmed an exact round trip
- [ ] Can say why `tokenizers` Unigram round-trips this corpus and SentencePiece Unigram does not

## Section 4 — together

- [ ] Read 4.1; ran its check-yourself
- [ ] Built the nine-row table from **one** `text` variable and **your** corpus hash
- [ ] Defined an OOV probe set and **asserted your corpus does not contain it**
- [ ] Can name a row that is lossless but incomplete, and one that is complete but lossy
- [ ] Can itemize what the only both-passing `V = 1000` row costs
- [ ] Can name three columns the table lacks

## The eval that can go red (Principle 11)

- [ ] `tests/test_tokenizer_families.py` exists and runs CPU-only, offline, deterministically
- [ ] **Observed red before green:** likelihood rule with no `min_frequency` → picks a count-1 pair
- [ ] **Observed green where it matters:** shuffling a WordPiece vocabulary → nothing changes
- [ ] **Observed red before green:** multiplying probabilities → underflow to `0.0`
- [ ] **Observed red before green:** sampling on → `assert_same_tokenizer(t, t)` fails
- [ ] **Observed red before green:** WordPiece on `café` → decodes to `''`
- [ ] **Observed red before green:** SentencePiece defaults → 1,646 newlines destroyed
- [ ] You have at least **five** assertions that assert a *non*-effect or a *failure*, and can say what
      boundary each one pins

## Silent failures ruled out (plan §6)

- [ ] **#5 evaluated on the format you trained on** — you can name **four** measurements in this day that
      look perfect on the training corpus and fail on ordinary held-out text
- [ ] **#2 tokenizer/template mismatch** — you can say how sampling and a default normalizer each create it
- [ ] **#4 noise mistaken for improvement** — your part 2.4 numbers are recorded as samples with a spread,
      and you can give the standard error for 400 draws

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with the corpus hash beside it
- [ ] You did **not** copy this day's `56957`, `444`, `158`, `0.9724`, `201000`, `11.2%`, `1369` or
      `50493` figures into your notes as if they were yours
- [ ] Your **timings** carry your own hardware line
- [ ] Your part 2.4 counts are recorded as **samples**, with more than one run
- [ ] Your notes record that `remove_extra_whitespace` (singular) is **not** a field — verified by the
      trainer refusing it, not assumed
- [ ] Your notes record that the `sentencepiece` `train` docstring is empty, so its arguments were verified
      by calling them
- [ ] You can name the one claim in this day that is **cited, not measured** (arXiv:1804.10959's BLEU
      results) and say why it could not be measured here

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] Longest single step recorded, with hardware
- [ ] You can name the one question this day **cannot** answer, and what it would cost

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **one row**, dated, version looked up live
- [ ] `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**
- [ ] `pyproject.toml` and `uv.lock` committed together
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-14 and TOK-15 closed on day 15
- [ ] `./m done 15` committed with the message from §11
