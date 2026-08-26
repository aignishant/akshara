# Day 5 — CHECKLIST

**IDs closed:** MATH-08, MATH-09
**Principles served:** 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 20
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 5` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 6 days complete, then one commit reading
`day 005: Logits, softmax and sampling — closes MATH-08, MATH-09`.

---

## Setup

- [ ] Day 4's checklist is fully ticked and `./m done 4` committed
- [ ] `./m scaffold 5` run; the lab directory exists
- [ ] **No packages installed today** — confirmed
- [ ] You know why the `NaN` demonstrations wrap themselves in `np.errstate`, and why you must never
      write that in real code

## MATH-08 — logits and probabilities (section 1)

- [ ] Read 1.1; ran its check-yourself — `argmax` token, sum `1.0`, and the two summed shapes
- [ ] Can state the two conditions that make a list of numbers a distribution
- [ ] Can say what a language model outputs and what it deliberately does not do
- [ ] Can say why the reduction axis is written `axis=-1` and not `axis=2`
- [ ] Read 1.2; ran its check-yourself — `argmax` agrees, sums `2.6` and `1.0`, counts `4` and `3`
- [ ] **Saw the shift-by-100 change nothing** (`4.857e-16`) and can say what that implies
- [ ] Can name the two constraints logits do not satisfy and the one property they share
- [ ] Read 1.3; ran its check-yourself — sum `1.0`, ratios all `2.718282`, and `[nan nan nan]`
- [ ] Can say why the consecutive ratios are `e`, and what that means about logit *gaps*
- [ ] Can explain why subtracting the maximum is **exact** rather than an approximation
- [ ] Provoked the `keepdims` error with `V != T`, and can say why it would be **silent** at `V == T`
- [ ] Read 1.4; swept the temperature and **recorded the entropy column on your machine**
- [ ] Confirmed `p ** (1/T)` renormalised equals `softmax(z/T)`
- [ ] Saw `softmax(z / 0.0)` give `[nan nan nan nan]`, and a negative `T` give a **valid reversed**
      distribution
- [ ] Can say what temperature scales, name both limits, and say why `T = 0` is a separate branch
- [ ] Read 1.5; ran its check-yourself — a count near `1190`, and a shortfall equal to `float32` eps
- [ ] **Re-ran the accumulator in `float16`** and predicted the shortfall first
- [ ] Can say why a softmax output does not sum to exactly one
- [ ] Can name the two things that must never be written against such a sum, and what to write instead

## MATH-09 — sampling (section 2)

- [ ] Read 2.1; wrote the two-part sampler with the generator passed **in**
- [ ] Ran its check-yourself — frequencies within `0.002` of target, all six exact mappings `ok`
- [ ] Changed `<` to `<=`, saw the frequencies barely move and **one exact case flip**
- [ ] Can name the two parts of any sampler and which one carries the randomness
- [ ] Can explain why a frequency test cannot establish that a zero-probability token is never emitted
- [ ] Read 2.2; ran its check-yourself — ten mappings, two disagreeing boundary answers, `0` out of range
- [ ] The `searchsorted` frequencies **match part 2.1's loop with the same seed**
- [ ] Saw `searchsorted(p, 0.3)` return `4` for a vocabulary of size 4
- [ ] Can say what the CDF is and why it can be binary-searched
- [ ] Can explain why the boundary convention is invisible to a frequency test and decisive after
      truncation
- [ ] Read 2.3; ran its check-yourself — `True`, `False`, and three differing frequency rows
- [ ] **Wrote down your seed-to-seed spread** — the floor below which no comparison means anything
- [ ] Drew one extra number before the loop and confirmed the results changed
- [ ] Can say what a seed fixes and what it does not
- [ ] Can explain why passing a generator differs from seeding a global, using the word *order*
- [ ] Read 2.4; ran its check-yourself — sampled fraction near `p[argmax]`, and a **visible loop**
- [ ] Distinct-state counts recorded for greedy and sampled
- [ ] Can state the two different questions greedy and sampling answer
- [ ] Can explain why the most likely token at each step is not the most likely sequence
- [ ] Read 2.5; ran its check-yourself — shortfall == `float32` eps, fall-throughs **not zero**, `None`
- [ ] Added `return len(p) - 1` and watched it become `49`
- [ ] Re-ran in `float16` and predicted the shortfall from Day 2 part 1.2's table first
- [ ] Can say why the fall-through rate equals the dtype's epsilon
- [ ] Can describe how to write a **deterministic** test for a one-in-eight-million bug

## Together (section 3)

- [ ] Read 3.1; ran its check-yourself — four rows, distinct counts `1, 4, 6, 8`
- [ ] **Removed each of the six guards in turn** and recorded what each removal produced
- [ ] Noted which removals produced **nothing visible** — those are the dangerous ones
- [ ] Can name the eight steps from hidden state to token
- [ ] Can state the rule about where the distribution may be reshaped and how many softmaxes there are

## Build brief

- [ ] `lab/distributions.py` written — `softmax` with the max subtraction **and** `keepdims`
- [ ] `lab/sampling.py` written — `next_token` with all six guards
- [ ] `tests/test_sampling.py` written — exact mapping, frequencies, fall-through, guards
- [ ] `lab/sweeps.py` written — **your** temperature/entropy sweep and **your** softmax-sum rates
- [ ] `next_token` vectorised over a batch, with **one** `searchsorted` and no Python loop
- [ ] The softmax-sum failure rate measured in `float64`, `float32` **and** `float16`, predicted first
- [ ] The `p ** (1/T)` form implemented and asserted equal to `softmax(z/T)`
- [ ] The degeneration report written and run on both greedy and sampled sequences
- [ ] The "how many draws to distinguish `T = 0.9` from `T = 1.0`" arithmetic done **on paper**

## The evals that must be able to fail

- [ ] `uv run python -m pytest tests/test_sampling.py -q` green
- [ ] `<` → `<=` in the loop → **one exact mapping flips**, frequencies unmoved
- [ ] Max subtraction removed → `[nan nan nan]` at logits of 1000
- [ ] `isclose` → `==` on the sum → **red about six times in ten**, and you ran it enough times to see
      both outcomes
- [ ] `cdf[-1] = 1.0` and the clamp removed → `None` at `np.nextafter(1.0, 0.0)`
- [ ] Negative temperature → the guard fires, with its message
- [ ] Everything put back; the suite is green
- [ ] `./m depth 5` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 8, 9, 10)

- [ ] Every number you wrote down is **measured on your machine**, with hardware, **seed** and date —
      or cited. None was recalled.
- [ ] You did **not** copy this day's `1190/2000`, `9 in 50,000,000`, `0.6295` or `0.0868` figures into
      your notes as if they were yours
- [ ] Every measurement involving randomness records **which seed** produced it
- [ ] Where your machine disagreed with this document, you **recorded the disagreement**

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say why every failure in this day reproduces identically on any hardware

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**, and you can say why
      a fifty-million-draw microbenchmark is not a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-08 and MATH-09 closed on
      day 5
- [ ] `./m done 5` committed with the message from §11
