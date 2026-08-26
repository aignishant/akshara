# Day 7 — CHECKLIST

**IDs closed:** MATH-13, MATH-14
**Principles served:** 1, 2, 3, 8, 10, 11, 16, 17, 18, 20
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 7` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 8 days complete, then one commit reading
`day 007: Numerical reality — floating point and log-sum-exp — closes MATH-13, MATH-14`.

---

## Setup

- [ ] Day 6's checklist is fully ticked and `./m done 6` committed
- [ ] `./m scaffold 7` run; the lab directory exists
- [ ] **No packages installed today** — confirmed
- [ ] You can say why every `nan` demonstration needs `np.errstate`, and why that must never appear in
      real code
- [ ] You have hit the numpy promotion trap at least once and can say why `s += v` and
      `s = np.float16(s + v)` behave differently

## MATH-13 — floating point (section 1)

- [ ] Read 1.1; ran its check-yourself — three zero mantissas and a reconstruction matching numpy
- [ ] Can give the value formula naming all three fields, from memory
- [ ] Can say why `0.1 + 0.2 != 0.3` **without** using the phrase "floating point is imprecise"
- [ ] Can say why the gap between representable numbers is not constant
- [ ] Read 1.2; ran its check-yourself — one `inf` with a warning, one `0.0` without
- [ ] **Wrote down the bit split of all three formats** — `fp32`, `fp16`, `bf16`
- [ ] Can say which of `fp16` and `bf16` you would train in, and what the other one needs added
- [ ] Computed the megabytes of a `(50257, 768)` embedding in each of the three formats
- [ ] Saw that `bf16` cannot distinguish `1.0` from `1.005` and can say why that is survivable
- [ ] Read 1.3; ran its check-yourself — three gaps six orders of magnitude apart
- [ ] **Wrote down the value at which `x + 1 == x`** for `fp16`, `fp32` and `fp64`
- [ ] Can say what a `float16` token counter does after 2048
- [ ] Can say why tolerances are relative and when `atol` is the correct choice
- [ ] Read 1.4; ran its check-yourself — one sum that drifted and one that **stopped**
- [ ] Watched the `fp16` sum give `256.0` for both 10,000 and 100,000 terms
- [ ] Can name the two regimes — drift and stall — and say which dtype gets which
- [ ] Can give the three fixes in the order you would try them
- [ ] Ran `np.sum` against the hand-written loop on the same terms and recorded both numbers
- [ ] Read 1.5; ran its check-yourself — **1000 training steps that changed nothing**
- [ ] Can say why mixed precision keeps an `fp32` master copy, with the arithmetic
- [ ] Can say whether mixed precision makes the weights take more memory or less, and why
- [ ] Can say what loss scaling is for and why `bf16` does not need it
- [ ] Can name the three things that stay in `fp32` and why each one needs the bits

## MATH-14 — the stable softmax and log-sum-exp (section 2)

- [ ] Read 2.1; ran its check-yourself — three thresholds and one `nan` from three ordinary integers
- [ ] **Wrote down `ln(max)` for `fp16`, `fp32` and `fp64`** — `11.09`, `88.72`, `709.78`
- [ ] Can say what a softmax row looks like after one entry overflows, **and why the others go to zero**
- [ ] Worked out whether `1/sqrt(hs)` scaling at `hs = 64` keeps a raw dot product under `11.09`
- [ ] Can say why overflow is fatal and underflow is benign **after** the max subtraction
- [ ] Read 2.2; ran its check-yourself — one `inf`, one `-inf`, and the same answer twice, shifted
- [ ] Can state both bounds on `lse(z)` and say when each is reached exactly
- [ ] Can state the shift identity and say why it makes the function safe rather than convenient
- [ ] Saw `lse(z + 1e6) == lse(z) + 1e6` return **`True`** with exact float equality
- [ ] Can say what `keepdims=True` is for and what a square test batch hides
- [ ] Read 2.3; ran its check-yourself — one `-inf` and one `-800.0` from the same logits
- [ ] Can write `log_softmax` as an expression with **no exponential in it**
- [ ] Can say why `cross_entropy` takes logits, and what happens if the model already ends in a softmax
- [ ] Can say why `-inf` is worse than a very negative number
- [ ] Noticed that no `(B, T, V)` probability tensor is created anywhere in the loss
- [ ] Read 2.4; ran its check-yourself and **saw a row sum to `1.0000000000` with 980 entries zeroed**
- [ ] Can say why "the probabilities sum to 1" cannot detect this failure
- [ ] Can name the check that does, and say where the `fp32` cast has to happen
- [ ] **Answered in writing: the lost mass is `5.15e-07` — why does it still matter?**
- [ ] Saw the same information survive intact as log-probabilities in the same dtype
- [ ] Read 2.5; ran its check-yourself — three softpluses, one of them unusable
- [ ] Can state the rule for when you need `lse`
- [ ] Can name three places other than the softmax where `lse` appears
- [ ] Can describe the one-line running-maximum update that makes `lse` streamable
- [ ] Can say what `argmax` returns on an array of all zeros, and what that does to a beam searcher

## Section 3 — the battery

- [ ] Read 3.1; ran its check-yourself — `nan` from **`float32`**, and three stable losses agreeing
- [ ] Can name the three invariants that hold for any correct `log_softmax`
- [ ] Can say which invariant catches an axis error and which two do not
- [ ] Can say why a test batch should never be square
- [ ] Ran the battery at a logit scale 40× larger and recorded which dtypes produced `nan`

## Build brief

- [ ] `lab/floats.py` written — `unpack_float32`, `to_bf16`, `gap_at`, `format_table`
- [ ] `lab/summation.py` written — naive, Kahan, and the stability check
- [ ] `lab/stable.py` written — `logsumexp`, `log_softmax`, `softplus`, `log_sigmoid`, `online_lse`
- [ ] `lab/battery.py` written — `check_numerics` returning the loss and the relative error
- [ ] `tests/test_numerics.py` written — overflow, accumulation, zero-tail, three invariants
- [ ] `ln(finfo.max)` computed for all three dtypes, with the `hs = 64` attention arithmetic worked
- [ ] `to_bf16` verified against its three defining properties
- [ ] The accumulation demonstration written as a test that **goes red**, then fixed by one line
- [ ] The 980/1000 result reproduced at `V = 32000` with your own seed, and the mass reported
- [ ] `online_lse` asserted **bit-identical** to the one-pass version at three block sizes
- [ ] The battery run on a square `(4, 50, 50)` batch with `keepdims` removed, and the catching
      invariant recorded

## The evals that must be able to fail

- [ ] `uv run python -m pytest tests/test_numerics.py -q` green
- [ ] Max subtraction removed from `logsumexp` → **`inf`** at logits of 1000
- [ ] `0.1` summed 10,000 times in `float16` → **`256.0`**, not `1000.0`
- [ ] `log(softmax(z))` used instead of `z - lse(z)` → **`-inf`** for `[0, -400, -800]`
- [ ] Softmax run in `float16` on a peaked distribution → **980 exact zeros, row sum `1.0`**
- [ ] `keepdims=True` dropped on a square batch → `lse - max` **outside `[0, ln V]`**
- [ ] Everything put back; the suite is green
- [ ] `./m depth 7` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 8, 10)

- [ ] Every number you wrote down is **measured on your machine**, with hardware, seed and date — or
      cited. None was recalled.
- [ ] **Every threshold you recorded names its dtype** (`11.09` without `fp16` beside it is a rumour)
- [ ] **Every sum you recorded names its accumulator dtype and its term count**
- [ ] You did **not** copy this day's `980/1000`, `256.0`, `9998.557` or `5.15e-07` figures into your
      notes as if they were yours
- [ ] Where your machine disagreed with this document, you **recorded the disagreement** — including
      the CPython patch version, if yours differs from the `3.12.12` in §8

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say why **every** result in this day reproduces bit-for-bit on any conforming machine
- [ ] You can say which half of the mixed-precision argument this day **cannot** prove, and which day
      measures it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-13 and MATH-14 closed on
      day 7
- [ ] `./m done 7` committed with the message from §11
