---
day: 4
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Backprop through a layer and gradient checking"
ids: ["MATH-06", "MATH-07"]
principles: [1, 2, 3, 8, 10, 11, 16, 17, 18, 20]
kind: math
plan_version: "v1.3.0"
parts: 11
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 4 — Backprop through a layer, and gradient checking

> **Yesterday (Day 3):** derivatives from the definition, the chain rule as multiply-along and
> add-across, and a scalar autograd engine written from nothing — plus four ways it can be wrong that
> all produce plausible numbers.
> **Today:** the same walk with matrices. The three gradients of a linear layer, the transpose that
> everyone gets wrong, and the method that means you never have to remember where it goes — then the
> independent check that proves a derivation, and the four blind spots that make it necessary and not
> sufficient.
> **Tomorrow (Day 5):** probability over a vocabulary — logits, softmax, temperature, and sampling from
> a categorical distribution (MATH-08, MATH-09).

---

## §1 Where we are

Yesterday's engine differentiates any expression you can type, one scalar at a time. Today it stops
being one at a time.

Almost everything in a transformer that holds a number is a linear layer: take a batch of inputs,
measure each one against every column of a weight matrix, add a bias. `Y = X @ W + b`. The attention
projections are that. The feed-forward block is two of them. The output head is one. So there is
really only one backward pass to derive in this entire curriculum, and today is the day it gets
derived.

The derivation itself is short — three sums, one per input, each one an application of yesterday's
two rules. What takes the day is that the *matrix* form of those sums has a transpose in it, and the
transpose is where everyone goes wrong. Not because it is hard: because there are four plausible
arrangements of two operands and only one is right, and the wrong ones are wrong in a specific and
horrible way. In a layer whose dimensions happen to be equal — which describes every attention
projection in every transformer — **all four arrangements are legal, all four produce the right
shape, and the wrong ones still train.** Measured today: a gradient nearly perpendicular to the true
one, cosine similarity 0.0868, and a loss curve that goes down.

Which is why the second half of the day is about a different kind of check. Not "does the shape
match", because it does. Not "does the loss go down", because it does. The only thing that finds an
85-degree error in a gradient is a second, independent computation of the same quantity — and there is
exactly one available: nudge the input by a tiny amount, watch the loss move, divide. It is far too
slow to train with, which is the point; it is a *test*, and it is the first genuinely mathematical
thing that will run on every commit for the rest of the project.

And then the honest part, which is three documents long. A gradient check proves your backward pass
agrees with your forward pass, and nothing else. Delete the bias from the layer and the check reports
a relative error of `8.1e-11` — a clean pass, on a layer that has lost a term. Run it at a point where
the activation is saturated and it awards a *perfect* score of `0.000e+00` to a backward pass that
returns nothing but zeros. Test it with an all-ones input and a transposed gradient differs from the
correct one by exactly zero.

Every one of those is a green test. Knowing precisely what green means, and what else you have to run
alongside it, is the day.

Everything is on the laptop, in numpy, at shapes of two, three and five — deliberately, and the
reason why is one of the things today teaches.

---

## §2 The map

Eleven parts, three sections. Section 1 is MATH-06 (deriving the backward pass), section 2 is MATH-07
(proving it), and section 3 assembles both into the routine you run for every operation from here on.
The day climbs `foundation → working → production`, and sections 1 and 2 each end with something
breaking.

### Section 1 — `01-the-linear-layer`: MATH-06, the only backward pass you really need

The forward pass, its three gradients, the shape-first method that determines every transpose, the
broadcast rule for the bias — and what happens when the shapes stop telling you anything.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A layer is a matmul plus a vector](parts/01-the-linear-layer/1.1-a-layer-is-a-matmul-plus-a-vector.md) | What exactly is the thing that holds every parameter in a transformer? | `foundation` |
| 1.2 | [The three gradients](parts/01-the-linear-layer/1.2-the-three-gradients.md) | Three inputs, three gradients — which axis does each one sum over, and why? | `working` |
| 1.3 | [The transpose everyone gets wrong](parts/01-the-linear-layer/1.3-the-transpose-everyone-gets-wrong.md) | How do you get the formula right without remembering it? | `working` |
| 1.4 | [The bias gradient is a sum](parts/01-the-linear-layer/1.4-the-bias-gradient-is-a-sum.md) | What does backpropagating through a broadcast turn into? | `working` |
| 1.5 | [💥 The transpose that trained anyway](parts/01-the-linear-layer/1.5-the-transpose-that-trained-anyway.md) | Why does a gradient 85° off the truth still reduce the loss? | `production` |

### Section 2 — `02-gradient-checking`: MATH-07, the independent second opinion

The oracle, the criterion, the test file — and then two documents on exactly what it does not prove.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Finite differences as an oracle](parts/02-gradient-checking/2.1-finite-differences-as-an-oracle.md) | What makes a second method worth more than checking your work twice? | `foundation` |
| 2.2 | [The relative error criterion](parts/02-gradient-checking/2.2-the-relative-error-criterion.md) | How do you pick a threshold you can defend, and why does the dtype change it? | `working` |
| 2.3 | [Making it a test](parts/02-gradient-checking/2.3-making-it-a-test.md) | What turns a check you ran once into one that protects every future commit? | `working` |
| 2.4 | [What it cannot catch](parts/02-gradient-checking/2.4-what-it-cannot-catch.md) | What does a passing gradient check actually prove? | `production` |
| 2.5 | [💥 The gradcheck that passed on zeros](parts/02-gradient-checking/2.5-the-gradcheck-that-passed.md) | How does a backward pass that computes nothing score a perfect zero? | `production` |

### Section 3 — `03-together`: the routine

Four checks, four different questions, and the gaps between them measured.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Gradcheck the layer you wrote](parts/03-together/3.1-gradcheck-the-layer-you-wrote.md) | Which bug does each of the four checks catch that none of the others does? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything uses the numpy pinned on Day 2, plus `pytest` from the Day 0 dev
group.

```bash
# confirm what you already have
uv run python -c "import numpy; print('numpy', numpy.__version__)"
uv run python -m pytest --version

# today's scratch space
./m scaffold 4

# today produces the first real test file in the project
mkdir -p tests
touch tests/test_linear.py
```

`tests/` is where today's work lands, and it must satisfy this repository's four rules (CLAUDE.md):
CPU-only, deterministic, offline, and fast. A gradient check meets all four naturally — part
[2.3](parts/02-gradient-checking/2.3-making-it-a-test.md) says why — and from today `./m check`
verifies a derivation rather than only checking formatting.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-004-backprop-and-gradcheck/lab/linear.py` | [1.1](parts/01-the-linear-layer/1.1-a-layer-is-a-matmul-plus-a-vector.md), [1.2](parts/01-the-linear-layer/1.2-the-three-gradients.md) | `linear_forward` and `linear_backward`, with the three shape assertions inside |
| `days/day-004-backprop-and-gradcheck/lab/gradcheck.py` | [2.1](parts/02-gradient-checking/2.1-finite-differences-as-an-oracle.md), [2.2](parts/02-gradient-checking/2.2-the-relative-error-criterion.md), [2.5](parts/02-gradient-checking/2.5-the-gradcheck-that-passed.md) | `numerical_gradient`, `relative_error`, and the `judged` guard |
| `tests/test_linear.py` | [2.3](parts/02-gradient-checking/2.3-making-it-a-test.md), [3.1](parts/03-together/3.1-gradcheck-the-layer-you-wrote.md) | the four checks, parametrised, each watched **red** |
| `days/day-004-backprop-and-gradcheck/lab/sweep.py` | [2.2](parts/02-gradient-checking/2.2-the-relative-error-criterion.md) | your machine's `h` sweep in `float64` **and** `float32`, and the `RTOL` you derive from it |

```text
TODO(me): extend linear_backward to the (B, T, C) case from part 1.4 — the bias sums over
          two axes and dW contracts two. Write it with einsum AND with a reshape, and
          assert the two agree. Say in a comment which you would ship and why.

TODO(me): write `unbroadcast(grad, shape)` from part 1.4 and use it in place of the
          hand-written axis list. Then delete the axis list and confirm the tests still pass.

TODO(me): parametrise the gradient check over at least three shape triples, including one
          with a size-1 axis. Predict which triple would catch a transpose bug and which
          would not, then verify by introducing one.

TODO(me): add a test that asserts the JUDGED FRACTION, and make it go red by moving the
          test point into tanh saturation. Part 2.5 is the argument; the demonstration is
          yours.

TODO(me): work out on paper why the backward pass costs roughly twice the forward pass for
          this layer. One sentence and two flop counts.
```

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11). Each goes red by
a different one-line edit, which is the whole argument for having four.

```bash
uv run python -m pytest tests/test_linear.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| delete `+ b` from `linear_forward` | `ACTUAL: array([[11.]])  DESIRED: array([[21.]])` | 2 — the value test |
| `dW = dY.T @ X` | `AssertionError: dW (5, 3) != W (3, 5)` | 1 — the shape assertion |
| `dW = X @ dY` at **square** shapes | `relative error 1.000e+00 exceeds 1e-06` | 3 — the gradient check |
| `W + lr * dW` instead of `-` | `one step did not reduce the loss: 7.467132 -> 7.493422` | 4 — the loss decrease |
| gradcheck at `tanh(25.0)` | `only 0% of entries judged — pick another point` | 3′ — the judged-fraction guard |

The third row **needs square shapes** to reproduce, and that is itself a finding: with `B, C, C_out =
2, 3, 5` the same bug is caught earlier and more cheaply by check 1. Try both.

The fifth row is the one that does not exist in most people's gradient checkers. Without the
`judged.mean()` assertion, that case **passes** — a perfect `0.000e+00` on a backward pass that returns
zeros.

---

## §6 Compute budget

**Tier: T0.** numpy on a laptop CPU, at shapes of two, three and five.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed today |
| Disk | negligible |

The heaviest thing today is a gradient check: `2n` forward passes for `n` parameter elements, which at
these shapes is **52 forward passes** on `(2, 3)` matrices. That is not a compromise forced by the
zero-budget rule — it is what a gradient check should be, because the correctness of `dW = X.T @ dY`
does not depend on `C` being 5 or 5000.

What T0 proves today: the **derivation** (exact algebra, transfers to any size and any hardware), the
**shape rules** (identical everywhere) and the **failure modes** (all structural, all reproduced in
milliseconds). What it does not prove: anything about throughput, and anything about numerical
behaviour in narrow dtypes at real scale — which is Day 7 and Day 78.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Stacking linear layers with no nonlinearity | `(X @ W1) @ W2 == X @ (W1 @ W2)` — the depth bought nothing | [1.1](parts/01-the-linear-layer/1.1-a-layer-is-a-matmul-plus-a-vector.md) |
| Forgetting `dW` needs `X` | the forward input must survive to the backward pass — that is activation memory | [1.2](parts/01-the-linear-layer/1.2-the-three-gradients.md) |
| `db = dY.sum(axis=1)` | a `(B,)` where a `(C_out,)` was meant; raises at the update, not at the sum | [1.2](parts/01-the-linear-layer/1.2-the-three-gradients.md) |
| Reaching for `.T` at whichever operand is nearest | a legal matmul of the wrong thing whenever the other dims line up | [1.3](parts/01-the-linear-layer/1.3-the-transpose-everyone-gets-wrong.md) |
| Not knowing which layout `W` is stored in | `X.T @ dY` and `dY.T @ X` are both right, under different conventions | [1.3](parts/01-the-linear-layer/1.3-the-transpose-everyone-gets-wrong.md) |
| `dY.sum(axis=0)` on a `(B, T, C_out)` tensor | a `(T, C_out)` gradient that **broadcasts** into the bias — the bias silently becomes a matrix | [1.4](parts/01-the-linear-layer/1.4-the-bias-gradient-is-a-sum.md) |
| Testing at square shapes | every wrong transpose is legal; cosine 0.0868 and the loss still falls | [1.5](parts/01-the-linear-layer/1.5-the-transpose-that-trained-anyway.md) |
| Treating a decreasing loss as evidence | any direction within 90° of downhill reduces the loss | [1.5](parts/01-the-linear-layer/1.5-the-transpose-that-trained-anyway.md) |
| Forgetting `param[i] = original` in the numerical gradient | plausible nonsense; the check fails against a **correct** backward pass | [2.1](parts/02-gradient-checking/2.1-finite-differences-as-an-oracle.md) |
| A loss that reads a copy of the parameter | the numerical gradient is identically zero and the comparison is vacuous | [2.1](parts/02-gradient-checking/2.1-finite-differences-as-an-oracle.md) |
| An absolute error threshold | the same correct gradient, inputs ×1000: absolute error ×360,000 | [2.2](parts/02-gradient-checking/2.2-the-relative-error-criterion.md) |
| A `float64` threshold on a `float32` check | `3.3e-02` on a **correct** gradient — a failing test with nothing wrong | [2.2](parts/02-gradient-checking/2.2-the-relative-error-criterion.md) |
| Taking the **mean** relative error | one wrong row hidden among a thousand right ones | [2.2](parts/02-gradient-checking/2.2-the-relative-error-criterion.md) |
| A threshold with no headroom | `dX` measured `8.978e-09` against `1e-7` — one order, and a flaky test | [2.3](parts/02-gradient-checking/2.3-making-it-a-test.md) |
| Believing a passing gradient check | a bias-free layer passes at `8.135e-11` | [2.4](parts/02-gradient-checking/2.4-what-it-cannot-catch.md) |
| All-ones test data | right and wrong `dW` differ by **exactly 0.0000** | [2.4](parts/02-gradient-checking/2.4-what-it-cannot-catch.md) |
| Gradient-checking at a saturated point | relative error `0.000e+00` for a backward pass of zeros | [2.5](parts/02-gradient-checking/2.5-the-gradcheck-that-passed.md) |
| Running fewer than four checks | every gap between them is a measured failure from today | [3.1](parts/03-together/3.1-gradcheck-the-layer-you-wrote.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement.** Today it arrives through a
gradient that is *wrong but still descends*. Part
[1.5](parts/01-the-linear-layer/1.5-the-transpose-that-trained-anyway.md) measures a run whose final
loss is 3.69× worse than it should be, with a monotonically decreasing curve throughout — a constant,
silent handicap of exactly the size you would later be trying to measure between real changes. It is
not noise, so more seeds do not find it; and parts
[2.4](parts/02-gradient-checking/2.4-what-it-cannot-catch.md) and
[2.5](parts/02-gradient-checking/2.5-the-gradcheck-that-passed.md) show that the obvious check can pass
on it too. The four-check routine in part
[3.1](parts/03-together/3.1-gradcheck-the-layer-you-wrote.md) is today's answer; Day 51's
overfit-one-batch is the model-level version, and Day 119 is the statistical one.

---

## §8 Verify before you code

Everything today is numpy 2.5.2 (pinned Day 2) and the standard library. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| `numpy` doc `reference/generated/numpy.matmul.html` | the gufunc signature `(n?,k),(k,m?)->(n?,m?)`, quoted verbatim in the error messages of parts 1.1 and 1.3 |
| `numpy` doc `reference/generated/numpy.nditer.html` | that `flags=["multi_index"]` yields a tuple index usable on an array of any rank |
| `numpy` doc `reference/generated/numpy.einsum.html` | the subscript convention used for the rank-3 `dW` in part 1.4 |
| `numpy` doc `reference/generated/numpy.linalg.norm.html` | that the default on a 2-D array is the Frobenius norm — part 1.5's cosine similarity |
| `numpy` doc `reference/generated/numpy.testing.assert_allclose.html` | the default `rtol=1e-07`, and the exact failure text quoted in parts 3.1 and §5 |
| `pytest` doc on `parametrize` and fixtures | the per-case reporting relied on in part 2.3 |
| Day 2 part 1.2's own output | `float32` eps `1.1920929e-07`, `float64` eps `2.220446049250313e-16` — the argument in part 2.2 |
| Day 3 part 1.5's own output | the measured optimum `h = 1e-5` for a `float64` central difference |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.10, numpy 2.5.2**,
seed **1337**, on **2026-08-26**. No figure was recalled and none came from another machine.

---

## §9 Say it in an interview

"The thing I'd point at from that week is that I stopped trusting a decreasing loss. I had a linear
layer where I'd dropped a transpose — `X @ dY` instead of `X.T @ dY` — and because the layer was square
it was perfectly legal and every shape assertion passed. I measured the cosine similarity between that
gradient and the correct one: 0.0868, so about 85 degrees apart, and the loss still went down for forty
steps, just to a final value 3.7 times worse than it should have been. Anything within 90 degrees of
downhill still descends. So now I gradient-check every backward pass I write against a central
difference, and I test at shapes like 2, 3 and 5 rather than 4, 4 and 4, because a square layer hides
transposes for free. And I learned the limits of the check the same week: a gradient check passes at
`8e-11` on a layer whose bias I'd deleted, because it only proves the backward agrees with the forward.
At a saturated `tanh` it gives a *perfect* score to a backward pass that returns zeros. So I run four
things now — shapes, a hand-computed forward value, the gradient check with a judged-fraction guard,
and one small step that has to reduce the loss — and I've watched every one of them go red on purpose."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 4` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 4 | 2026-08-26 | MATH-06, MATH-07 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; numpy was pinned on Day 2 and `pytest`
on Day 0.

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The forty-step loop in part
[1.5](parts/01-the-linear-layer/1.5-the-transpose-that-trained-anyway.md) is a demonstration on four
synthetic numbers, not a run; it belongs in the part that measured it, next to the hardware line.

Commit:

```text
day 004: Backprop through a layer and gradient checking — closes MATH-06, MATH-07
```
