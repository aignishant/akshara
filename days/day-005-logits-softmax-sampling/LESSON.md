---
day: 5
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Logits, softmax and sampling"
ids: ["MATH-08", "MATH-09"]
principles: [1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 20]
kind: math
plan_version: "v1.3.0"
parts: 11
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 5 — Logits, softmax and sampling

> **Yesterday (Day 4):** the backward pass of a linear layer, the transpose everyone gets wrong, and
> the independent check that proves a derivation — together with the three blind spots that make a
> passing gradient check necessary and not sufficient.
> **Today:** the other end of the model. What the output layer actually produces, the map that turns
> it into a distribution over the vocabulary, the one dial that reshapes that distribution, and the
> machinery for drawing a token out of it — with six measured ways each of those goes silently wrong.
> **Tomorrow (Day 6):** information — entropy, cross-entropy, KL and perplexity, and **why the loss is
> the loss** (MATH-10, MATH-11, MATH-12).

---

## §1 Where we are

A language model does not choose a word. It hands you a list.

One number per entry in its vocabulary — thirty-two thousand of them, say — and then it stops. It has
no opinion about what happens next, and everything you have ever seen a language model do is a
decision somebody made *after* that list existed. Take the largest and you get one kind of system.
Draw from it in proportion and you get another. Flatten it first and you get a third. Same weights,
same list, three different products.

So today is about that list and what is done to it, and it splits cleanly in half.

The first half is the list itself. The numbers coming out of the output layer are not probabilities —
they are unconstrained reals, positive and negative, measured today spanning `-11` to `+9` on a random
head. Getting from those to a distribution takes one operation with two steps, and the operation has a
property that is easy to state and easy to forget: **it depends only on the gaps between the numbers,
not on the numbers.** Add a hundred to every one and nothing changes at all. Divide every one by two
and everything does — and that division is the temperature dial, the whole of it, one line.

The second half is drawing a token. That turns out to be two things bolted together: one uniform
random number, and a completely deterministic rule for turning it into an index. Keeping those two
apart is what makes a generation reproducible, testable, and auditable — and it is also what lets you
swap greedy for sampling for beam search without the model knowing.

And then the day's real subject, which is that **almost nothing here fails loudly**. A softmax output
does not sum to one — measured at 1190 times out of 2000, on this machine. Greedy decoding produces
`1, 2, 1, 2, 1, 2` forever while every single step is the model's top choice. A hand-rolled sampler
returns `None` once in eight million draws in `float32`, and once in a thousand in `float16` — so a
sampler that has been correct for a year starts failing the week somebody quantizes the model. None of
those raises. Two of them look like nothing at all.

By the end there is one function, thirteen lines, with six guards in it, and a table saying which
measured failure each guard is for. That table is the day.

Everything runs on the laptop, in numpy, at vocabularies of four and fifty.

---

## §2 The map

Eleven parts, three sections. Section 1 is MATH-08 (the distribution), section 2 is MATH-09 (drawing
from it), and section 3 assembles both into the function every later day calls. The day climbs
`foundation → working → production`, and sections 1 and 2 each end with something breaking.

### Section 1 — `01-logits-and-probabilities`: MATH-08, what the model actually outputs

From "a list of numbers" to a distribution: what the constraint is, what the model gives you instead,
the map between them, the one dial that reshapes it — and why the result does not quite sum to one.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A distribution over a vocabulary](parts/01-logits-and-probabilities/1.1-a-distribution-over-a-vocabulary.md) | What does a language model actually output, and what does it deliberately not do? | `foundation` |
| 1.2 | [Logits are not probabilities](parts/01-logits-and-probabilities/1.2-logits-are-not-probabilities.md) | Why does confusing the two survive months undetected? | `working` |
| 1.3 | [Softmax — the map to the simplex](parts/01-logits-and-probabilities/1.3-softmax-the-map-to-the-simplex.md) | Why `exp`, and why is subtracting the maximum exact rather than approximate? | `working` |
| 1.4 | [Temperature is a scale on the logits](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md) | What does the one dial do, and why must `T = 0` be a separate branch? | `working` |
| 1.5 | [💥 The probabilities that summed to almost one](parts/01-logits-and-probabilities/1.5-the-probabilities-that-summed-to-almost-one.md) | What is wrong with `assert p.sum() == 1.0`? | `production` |

### Section 2 — `02-sampling`: MATH-09, turning a distribution into a token

One uniform number and a deterministic rule — then the boundary that decides the rule, the seed that
makes it reproducible, the choice between greedy and sampling, and the rare failure that only appears
in production.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Sampling from a categorical](parts/02-sampling/2.1-sampling-from-a-categorical.md) | How do you test a function that returns something different every time? | `foundation` |
| 2.2 | [The inverse-CDF trick](parts/02-sampling/2.2-the-inverse-cdf-trick.md) | Why is the boundary convention invisible to a frequency test and decisive once you truncate? | `working` |
| 2.3 | [Seeds and generators](parts/02-sampling/2.3-seeds-and-generators.md) | What does a seed guarantee, and what does it not? | `working` |
| 2.4 | [Argmax versus sampling](parts/02-sampling/2.4-argmax-versus-sampling.md) | Why doesn't taking the most likely token give the most likely sequence? | `production` |
| 2.5 | [💥 The sampler that fell through](parts/02-sampling/2.5-the-sampler-that-fell-through.md) | How do you write a deterministic test for a bug that happens once in eight million draws? | `production` |

### Section 3 — `03-together`: the function every later day calls

Eight steps, six guards, and a table saying which measured failure each guard is for.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [The full path](parts/03-together/3.1-the-full-path.md) | Which guard catches which measured failure, and what breaks if you remove it? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything uses the numpy pinned on Day 2.

```bash
uv run python -c "import numpy; print('numpy', numpy.__version__)"
./m scaffold 5
```

One thing to know before part
[1.3](parts/01-logits-and-probabilities/1.3-softmax-the-map-to-the-simplex.md): this repository sets
`filterwarnings = ["error::RuntimeWarning"]` in `pyproject.toml`, from Day 0. That turns numpy's
overflow and divide-by-zero **warnings** into exceptions, which is why the `NaN`-producing
demonstrations in parts 1.3 and 1.4 wrap themselves in `np.errstate(...)` to run at all. **Never write
`np.errstate` in real code** — it is the setting that turns a caught overflow into a silent `NaN`, and
it appears in this day only so a failure can be printed rather than raised.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-005-logits-softmax-sampling/lab/distributions.py` | [1.3](parts/01-logits-and-probabilities/1.3-softmax-the-map-to-the-simplex.md), [1.4](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md) | `softmax(z, axis=-1)` with the max subtraction and `keepdims`, and `assert_distribution` |
| `days/day-005-logits-softmax-sampling/lab/sampling.py` | [2.1](parts/02-sampling/2.1-sampling-from-a-categorical.md), [2.2](parts/02-sampling/2.2-the-inverse-cdf-trick.md), [3.1](parts/03-together/3.1-the-full-path.md) | `index_from_uniform`, the `searchsorted` form, and `next_token` with all six guards |
| `tests/test_sampling.py` | [2.1](parts/02-sampling/2.1-sampling-from-a-categorical.md), [2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md), [3.1](parts/03-together/3.1-the-full-path.md) | the exact-mapping test, the frequency test with a derived tolerance, the fall-through test, the guard tests |
| `days/day-005-logits-softmax-sampling/lab/sweeps.py` | [1.4](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md), [1.5](parts/01-logits-and-probabilities/1.5-the-probabilities-that-summed-to-almost-one.md) | your machine's temperature/entropy sweep and your own softmax-sum measurement |

```text
TODO(me): vectorise next_token over a batch. Take hidden (B, C) and return (B,) token ids
          with ONE searchsorted call and no Python loop. Part 2.2 has the shape; the
          batched cdf needs cumsum along axis -1 and the pin becomes cdf[:, -1] = 1.0.

TODO(me): measure YOUR machine's softmax-sum failure rate in float64, float32 and float16.
          Three numbers, one table, with your hardware line and the date. Predict each one
          from Day 2 part 1.2's epsilon table BEFORE you measure.

TODO(me): implement temperature the second way — p ** (1/T), renormalised — and assert it
          agrees with softmax(z/T) to 1e-12. Then say in a comment which you would ship and
          why, given that one of them needs the logits and the other does not.

TODO(me): write the degeneration report from part 2.4 (distinct-token ratio and
          unique-bigram ratio over a window) and run it on the greedy and sampled sequences
          from that part. Two numbers each. Day 25 will log these on every generation.

TODO(me): work out on paper how many draws you would need to distinguish T = 0.9 from
          T = 1.0 on a vocabulary of 50, given part 2.3's measured seed-to-seed spread of
          0.026 on a probability of 0.5. One number, and it is larger than you expect.
```

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_sampling.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| `if u < total` → `if u <= total` | one of six exact mappings flips | the exact-mapping test |
| remove the max subtraction from `softmax` | `[nan nan nan]` at logits of 1000 | the large-logit test |
| `assert p.sum() == 1.0` instead of `isclose` | red about 60% of the time | **the flakiness is the finding** |
| remove `cdf[-1] = 1.0` and the clamp | `None` at `u = np.nextafter(1.0, 0.0)` | the fall-through test |
| pass a negative temperature | a valid distribution, exactly reversed | the guard test in part 3.1 |

The third row is the one to sit with. An exact-equality assertion does not fail *always* — it fails
**about six times in ten**, which reads as flakiness rather than as a wrong assertion. A flaky test in
this repository is indistinguishable from Silent Failure #4 and must be fixed, never re-run
(CLAUDE.md), and here the thing to fix is the test.

The fourth row is the one that cannot be found by drawing more samples. Part
[2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md) measures the rate at 9 in 50,000,000, and
the test works by **constructing the `u` that triggers it** — `np.nextafter(1.0, 0.0)` — turning a
one-in-eight-million event into a deterministic assertion.

---

## §6 Compute budget

**Tier: T0.** numpy on a laptop CPU, at vocabularies of 4 and 50.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed today |
| Disk | negligible |

The heaviest thing today is part
[2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md)'s fifty million uniform draws, done in
ten chunks of five million to bound memory at about 40 MB, and completing in seconds.

What T0 proves: **every failure in this day**, because all six are properties of IEEE-754 arithmetic or
of the algorithms rather than of the hardware — the softmax sum, the `NaN` at `T = 0`, the overflow at
logits of 1000, the greedy loop, the fall-through rate equalling the dtype's epsilon. All of them
reproduce identically anywhere. What T0 does not show is the cost of any of them at production scale,
which is Day 69 onward.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Treating logits as probabilities | `argmax` agrees, so greedy decoding works forever and nothing reveals it | [1.2](parts/01-logits-and-probabilities/1.2-logits-are-not-probabilities.md) |
| A threshold applied to logits | `0.05` keeps 4 tokens as probabilities and 3 as logits | [1.2](parts/01-logits-and-probabilities/1.2-logits-are-not-probabilities.md) |
| `softmax` without the max subtraction | `[nan nan nan]` at logits of 1000 — and only a *warning* first | [1.3](parts/01-logits-and-probabilities/1.3-softmax-the-map-to-the-simplex.md) |
| `z.max(axis=-1)` without `keepdims` | raises when `V != T`, **broadcasts silently when `V == T`** | [1.3](parts/01-logits-and-probabilities/1.3-softmax-the-map-to-the-simplex.md) |
| Temperature applied to probabilities | sum becomes `2.0` or `0.5`, and the ratios are **unchanged** — no effect at all | [1.4](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md) |
| `T = 0` passed as a value | `[nan nan nan nan]`, because `inf - inf` is `nan` | [1.4](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md) |
| A negative temperature | a perfectly valid distribution, exactly reversed | [1.4](parts/01-logits-and-probabilities/1.4-temperature-is-a-scale-on-the-logits.md) |
| `assert p.sum() == 1.0` | red 1190 times in 2000, on correct code | [1.5](parts/01-logits-and-probabilities/1.5-the-probabilities-that-summed-to-almost-one.md) |
| `np.bincount` without `minlength` | a short array on unlucky seeds; a shape bug that comes and goes | [2.1](parts/02-sampling/2.1-sampling-from-a-categorical.md) |
| `searchsorted` on `p` instead of `cdf` | index `4` for a vocabulary of size 4 — out of range, no warning | [2.2](parts/02-sampling/2.2-the-inverse-cdf-trick.md) |
| Changing `side` between two implementations | frequencies identical to five decimals; one exact case flips | [2.2](parts/02-sampling/2.2-the-inverse-cdf-trick.md) |
| A global or unseeded generator | results depend on what other code drew first | [2.3](parts/02-sampling/2.3-seeds-and-generators.md) |
| Quoting one seed's number | three correct runs spanned `0.494`–`0.520` on the same distribution | [2.3](parts/02-sampling/2.3-seeds-and-generators.md) |
| `argmax` with no axis | one index into `B × T × V` — a valid-looking integer, complete nonsense | [2.4](parts/02-sampling/2.4-argmax-versus-sampling.md) |
| Greedy decoding on a long generation | `1, 2, 1, 2, 1, 2…` forever, every step the top choice | [2.4](parts/02-sampling/2.4-argmax-versus-sampling.md) |
| A sampler loop with no statement after it | `None`, once in 8.4 million in `float32`, **once in a thousand in `float16`** | [2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md) |
| `None` used as a numpy index | it is `np.newaxis` — adds a dimension and returns the whole vocabulary, no error | [2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement**, and today it is the day's
structural theme rather than one trap among many. A sampler's output is *supposed* to differ every
time, so the usual instinct — look at the output — cannot work here. Part
[2.3](parts/02-sampling/2.3-seeds-and-generators.md) measures three correct runs of the same
distribution spanning `0.026` on a probability of `0.5`, which is the floor below which no
single-seed comparison means anything. Part
[2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md) shows the complementary problem: a real
bug at a rate of `1.8e-07`, which no amount of sampling in a test suite would ever surface. **The
answers are the same on both sides — test the deterministic half exactly, and construct the input that
makes the rare case certain** — and Day 119 is where the statistical half becomes formal.

---

## §8 Verify before you code

Everything today is numpy 2.5.2 (pinned Day 2) and the standard library. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| `numpy` doc `reference/generated/numpy.searchsorted.html` | the meaning of `side="left"` / `"right"`, and that the first argument is **assumed** sorted without checking |
| `numpy` doc `reference/random/generator.html` | `default_rng(seed)`, and that `Generator.random()` returns values in `[0, 1)` |
| `numpy` doc `reference/random/bit_generators/generated/numpy.random.SeedSequence.html` | `spawn(n)` for independent streams from one seed — part 2.3 |
| `numpy` doc `reference/generated/numpy.cumsum.html` | that it is a plain running total with no normalisation |
| `numpy` doc `reference/generated/numpy.bincount.html` | that `minlength` is required to keep the output shape fixed |
| `numpy` doc `reference/generated/numpy.nextafter.html` | that `nextafter(1.0, 0.0)` is the largest `float64` below 1 — the constructed worst case in part 2.5 |
| `numpy` doc `reference/generated/numpy.finfo.html` | the epsilons re-used from Day 2 part 1.2 |
| Day 2 part 1.2's own output | `float32` eps `1.1920928955078125e-07`, `float16` eps `0.0009765625` — the fall-through rates in part 2.5 |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.10, numpy 2.5.2**,
seeds **1337**, **2026**, **5** and **20260826** as stated per part, on **2026-08-26**. No figure was
recalled and none came from another machine.

---

## §9 Say it in an interview

"The thing that changed how I think about generation is that the model doesn't choose anything — it
emits a distribution and stops, and everything after that is a decision I made. Once that's clear,
temperature stops being a mystery: it divides the logits, so it scales the *gaps* between them, and
`T → 0` is greedy and `T → ∞` is uniform. Two things from that week still shape how I write code.
First, greedy decoding isn't a safe default — I built a four-state chain where it enters a two-cycle at
step one and never leaves, and every single step is the model's top choice, so nothing looks wrong.
Second, I measured that a softmax output doesn't sum to exactly one: 1190 times out of 2000 on my
laptop, off by an epsilon. That sounds academic until you write the obvious sampler — accumulate until
you pass a uniform draw — and it returns `None` when the total falls short. I measured that at nine
occurrences in fifty million draws in `float32`, and the rate *is* the dtype's epsilon, so it's
8000 times worse in `float16`. A sampler that's been fine for a year starts failing the week someone
quantizes the model. I test that deterministically now by constructing the largest possible uniform
draw rather than hoping to see it."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 5` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 5 | 2026-08-26 | MATH-08, MATH-09 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; numpy was pinned on Day 2.

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The fifty-million-draw measurement in part
[2.5](parts/02-sampling/2.5-the-sampler-that-fell-through.md) is a microbenchmark, not a run; it
belongs in the part that measured it, next to the hardware line and the seed.

Commit:

```text
day 005: Logits, softmax and sampling — closes MATH-08, MATH-09
```
