# Day 9 — CHECKLIST

**IDs closed:** TOK-01, TOK-02
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 20
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 9` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 10 days complete, then one commit reading
`day 009: The vocabulary problem and what a tokenizer is for — closes TOK-01, TOK-02`.

---

## Setup

- [ ] Day 8's checklist is fully ticked and `./m done 8` committed
- [ ] `./m scaffold 9` run; the lab directory exists
- [ ] **No packages installed today** — confirmed; everything used is the standard library
- [ ] You can name the two tokenization conventions in play today and say which parts use which
- [ ] Day 5 part 1.1 re-read — you can state what a language model's output actually is

## TOK-01 — the vocabulary problem (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] Can say why the vocabulary is a permanent limit rather than a preprocessing choice
- [ ] Can say what happens to text the tokenizer has no way to encode — and that there is no third
      behaviour
- [ ] Can name the two matrices whose size is `V`, and say what changing `V` does to them
- [ ] Read 1.2; ran its check-yourself
- [ ] Measured the vocabulary growth curve yourself and can say whether it reaches zero
- [ ] Can state the hapax rate you measured, and say why a slot spent on a once-seen word is nearly
      wasted
- [ ] Can say why the words most likely to be cut are the ones carrying the most information
- [ ] Read 1.3; ran its check-yourself
- [ ] Measured the characters-per-token ratio on your own machine
- [ ] Can say which of the linear, quadratic and context costs settles the argument, and why
- [ ] Read 1.4; ran its check-yourself
- [ ] Can state the **two rules** a subword vocabulary follows
- [ ] Can say which of the two makes `<unk>` disappear rather than merely shrink
- [ ] Ran the probe table and saw a compression ratio **below 1.0** on unfamiliar input
- [ ] Wrote the `TODO(me)` paragraph on what you would rank candidate pieces by — **before** reading
      Day 12
- [ ] Read 1.5; ran its check-yourself
- [ ] Reproduced the falling loss and can explain, in one sentence, why destroying text lowers it
- [ ] Can name the one number that must be reported alongside a loss for that loss to mean anything
- [ ] Read the list of words your vocabulary destroyed, out loud, and can say what they have in common
- [ ] Can say why a byte-level fallback makes this failure **impossible** rather than merely rarer

## TOK-02 — what a tokenizer is (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Can state the two functions and the one property connecting them
- [ ] Ran the round-trip on the **whole corpus**, not on a hand-picked string, and saw `True`
- [ ] Broke it with `.lower()` and saw readable output that was not the input
- [ ] Can name two more ordinary-looking lines that break the round trip without raising
- [ ] Saw the `KeyError` on a character outside the table, and can say why that is better news than a
      silently shorter list
- [ ] Read 2.2; ran its check-yourself
- [ ] Can name the two steps at which a character exists, and the six at which one does not
- [ ] Can say where `T` is decided, and that it is not decided by the model
- [ ] Can say why a model cannot detect that it was handed ids from the wrong vocabulary
- [ ] Read 2.3; ran its check-yourself
- [ ] Can say what a checkpoint contains and what a tokenizer file contains, and why neither validates
      the other
- [ ] Verified that two different tables can have the same `V` and different hashes
- [ ] Removed `sort_keys=True` and confirmed the hash stopped being stable
- [ ] Read 2.4; ran its check-yourself
- [ ] Can name the three costs of a larger vocabulary and say which scales linearly, which
      quadratically and which logarithmically
- [ ] Worked out the vocabulary as a **fraction of the model** at your own planned `C` and depth
- [ ] Can say what quantity you would compare instead of loss when two runs have different `V`
- [ ] Read 2.5; ran its check-yourself
- [ ] Reproduced `'lbitparqwt sjyxtcjd'` on your own machine
- [ ] Confirmed all five checks pass on it — size, alphabet, range, length, printability
- [ ] Fixed it with one word, and can name the word
- [ ] Can say which kind of output — fluent or broken — points at the tokenizer rather than the model

## Section 3 — together

- [ ] Read 3.1; ran its check-yourself
- [ ] Built the six-column table on your own machine, on one paragraph, all rows on the **same** text
- [ ] Can say which column is a **gate** rather than a trade, and what that disqualifies
- [ ] Can say why the scheme that wins no column is the one everybody uses
- [ ] Added the `T × V` column and can say which scheme wins it — and whether that surprised you

## The eval that can go red (Principle 11)

- [ ] `tests/test_tokenizer.py` exists and runs CPU-only, offline, with no seed needed
- [ ] **Observed red before green:** added `.lower()` to `encode` → the round-trip test failed
- [ ] **Observed red before green:** built the vocabulary with `list(set(text))` → the mismatch test
      failed
- [ ] **Observed red before green:** double-counted spaces → the invariant test failed
- [ ] The round-trip test uses **two separately-constructed** tokenizers, not one object round-tripping
      through itself — you checked that it *can* fail
- [ ] The probe list in the round-trip test includes the empty string, a bare space, a tab, a
      double space, an apostrophe, and leading/trailing whitespace

## Silent failures ruled out (plan §6)

- [ ] **#2 tokenizer/template mismatch** — you can state the check the plan prescribes, and you wrote
      it as a function
- [ ] **#4 noise mistaken for improvement** — you can explain how part 1.5 is an instance of it, and
      why the metric moving in the right direction is not evidence

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with hardware and date — or cited
- [ ] You did **not** copy this day's `5.60`, `31.4`, `35.7%`, `18.31%`, `150`, `5,411` or `2,376`
      figures into your notes as if they were yours
- [ ] Every figure you recorded names **which convention** produced it — whitespace tokens or
      lowercased alphabetic runs
- [ ] The `5.6437` nats figure is labelled in your notes as **arithmetic over a described model**, not
      as the result of a training run
- [ ] Where your machine disagreed with this document, you **recorded the disagreement**

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can name the one thing about tokenization this day **cannot** demonstrate, and which day
      measures it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md` — **confirmed no rows**, and you can say why the master plan is not a dataset
      row
- [ ] `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can say why part 1.5's number is not a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-01 and TOK-02 closed on
      day 9
- [ ] `./m done 9` committed with the message from §11
