---
day: 8
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Gradient descent and Adam"
ids: ["MATH-15", "MATH-16"]
principles: [1, 2, 3, 8, 10, 11, 12, 16, 17, 18, 20]
kind: math
plan_version: "v1.3.0"
parts: 12
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 8 — Optimization: gradient descent, momentum, Adam and the learning rate

> **Yesterday (Day 7):** 💥 numerical reality — what a float is, where the gaps come from, where `exp`
> overflows in each dtype, and log-sum-exp, plus the `fp16` softmax that zeroed 980 of 1000 tokens and
> still summed to one.
> **Today:** the thing that consumes every gradient you have learned to compute. What a loss surface is,
> why one learning rate cannot serve two directions whose curvatures differ by a hundred, and the four
> refinements — momentum, per-parameter scaling, bias correction, decoupled decay — that turn
> `w ← w − lr·g` into the optimizer that trains every transformer. Ends with the test Principle 12
> makes mandatory.
> **Tomorrow (Day 9):** the vocabulary problem — why not words, why not letters, and exactly where a
> tokenizer sits in the stack (TOK-01, TOK-02). Phase 2 begins.

---

## §1 Where we are

Five days have been spent computing gradients. Today is what you do with one.

Start with a picture and no mathematics. Training is a walk on a landscape in fog. The height is the
loss, the horizontal directions are the parameters, and the walker has exactly one instrument: a spirit
level that says which way the ground tilts *right here*. No map, no view, no idea where the bottom is.
Every optimizer in this curriculum is a different rule for what to do with that one reading, and the
question to ask of a new one is always the same — **what does it remember, and what does it do with the
memory?**

Astonishingly, the tilt is enough. Step against it and the loss goes down. But two conditions attach,
and both are the day's real content.

The first is the size of the step, and it has an exact answer. For a bowl-shaped surface, the walk
converges if and only if the step is below `2/L`, where `L` is the *curvature*. Below that, it
descends. Above it, the walker crosses the valley and lands higher than she started, and then higher
again, forever. Measured today: at a step one percent past the boundary, four thousand iterations
produce no overflow, no error and no convergence — the run was unrecoverable from the first step and
looks completely normal for its entire first hour. **Divergence is not an explosion; it is a constant
percentage growth**, and by the time you see a `nan` the useful evidence is two thousand steps in the
past.

The second is worse, and it is what the rest of the day is about. `L` is the *largest* curvature across
every direction — so the most sensitive parameter in the model sets the step size for all of them. On
today's test surface the two parameters' gradients differ by a factor of a hundred: any single step is
either fifty times too big for one or a hundred times too small for the other. **There is no third
option, and no cleverer scalar.**

Four ideas remove it, in the order they were invented, each repairing the last. Remember the recent
gradients, so consistent directions add up and oscillating ones cancel — measured: 138 steps where
plain descent needed 653. Divide each parameter's step by the typical size of its *own* gradients, so
the learning rate stops meaning "how much gradient" and starts meaning "how far". Correct the two
running averages for having started at zero — and here the folklore is backwards: the uncorrected first
step is `3.16×` too *large*, not too small. And apply weight decay outside the division rather than
inside it, because inside, a single decay setting produced shrinkages of 9.09% and 0.10% on two
parameters — **a 91-fold disparity nobody chose.**

Then the day ends where Principle 12 says every training day begins: sixteen examples, trained until
the loss is essentially zero. A model that cannot memorise sixteen examples has a bug, not a
hyperparameter problem.

Twelve parts. Everything on the laptop, on a two-parameter surface whose exact optimum is known — which
is what makes today's numbers checkable rather than merely observed.

---

## §2 The map

Twelve parts, three sections. Section 1 is MATH-15: the surface, the step, the boundary, and momentum.
Section 2 is MATH-16: the four refinements that make up AdamW, and what its state costs. Section 3 is
the test. The day climbs `foundation → working → production` and each of the first two sections ends
with something breaking.

### Section 1 — `01-gradient-descent`: MATH-15, the walk and the step size

From a landscape you cannot see to the exact learning rate at which the walk stops working — and the
one line that fixes the zigzag.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [The loss surface you cannot see](parts/01-gradient-descent/1.1-the-loss-surface.md) | What can an optimizer actually observe, and what makes a problem hard? | `foundation` |
| 1.2 | [Gradient descent, one step at a time](parts/01-gradient-descent/1.2-gradient-descent-one-step.md) | Why does subtracting the gradient work, and what does `lr` supply that `g` cannot? | `working` |
| 1.3 | [The learning rate is the whole algorithm](parts/01-gradient-descent/1.3-the-learning-rate.md) | At exactly what step size does gradient descent stop converging? | `working` |
| 1.4 | [💥 The step that diverged, and took 1940 steps to admit it](parts/01-gradient-descent/1.4-the-step-that-diverged.md) | What does divergence actually look like before the `nan`? | `production` |
| 1.5 | [Momentum — the ball with inertia](parts/01-gradient-descent/1.5-momentum.md) | How do you speed up the flat direction without touching the stability bound? | `working` |

### Section 2 — `02-adam`: MATH-16, four repairs and a memory bill

Per-parameter scaling, the two moments, the correction everyone gets backwards, what the state costs,
the `W`, and the piece of state that goes missing on every resume.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [One learning rate cannot fit every parameter](parts/02-adam/2.1-one-learning-rate-is-not-enough.md) | What do you divide by, so every parameter moves at a comparable rate? | `foundation` |
| 2.2 | [Adam — momentum and per-parameter scale together](parts/02-adam/2.2-adam.md) | What are the two moments, and why is `lr` now a distance? | `working` |
| 2.3 | [Bias correction — the two lines everyone deletes](parts/02-adam/2.3-bias-correction.md) | Is the uncorrected first step too large or too small — and by how much? | `working` |
| 2.4 | [The optimizer's memory](parts/02-adam/2.4-the-optimizers-memory.md) | How many bytes per parameter does training actually cost? | `production` |
| 2.5 | [AdamW — why weight decay is not L2](parts/02-adam/2.5-adamw.md) | How does one `λ` become a 91× disparity between two parameters? | `production` |
| 2.6 | [💥 The optimizer state that outlived its parameters](parts/02-adam/2.6-the-optimizer-state-that-outlived-its-parameters.md) | Which piece of Adam's state does every checkpoint forget? | `production` |

### Section 3 — `03-together`: the test Principle 12 requires

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Overfit one batch](parts/03-together/3.1-overfit-one-batch.md) | What is the cheapest possible proof that a training pipeline is wired correctly? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything uses the numpy pinned on Day 2.

```bash
uv run python -c "import numpy; print('numpy', numpy.__version__)"
./m scaffold 8
```

Today builds directly on code the previous days told you to write, and **does not re-derive any of
it**:

- Day 3's `lab/engine.py` — the `Value` class with `data` and `grad`. Part
  [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md)'s update mutates `data` and reads
  `grad`, which is exactly why Day 3 separated them.
- Day 4's `lab/linear.py` and `lab/gradcheck.py` — the layer whose `dW` and `db` the optimizer
  consumes, and the finite-difference check that proves them. **Run `gradcheck` on your gradients
  before you trust part 3.1's test**, because a gradient bug inside the test would defeat the point.
- Day 6's `lab/loss.py` and Day 7's `lab/stable.py` — the loss part 3.1 minimises, computed the stable
  way.

One thing to have in mind: everything in section 1 uses a **two-parameter quadratic with curvatures
`[1, 100]`**, minimum at the origin, condition number 100. It is not a language model. It is the
smallest surface that shows the problem, and its exact optimum is known, so every claim today can be
checked rather than believed.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-008-gradient-descent-and-adam/lab/surface.py` | [1.1](parts/01-gradient-descent/1.1-the-loss-surface.md) | `quadratic(A)` returning `f` and `grad`, plus `condition_number` |
| `days/day-008-gradient-descent-and-adam/lab/optim.py` | [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md), [1.5](parts/01-gradient-descent/1.5-momentum.md), [2.2](parts/02-adam/2.2-adam.md), [2.5](parts/02-adam/2.5-adamw.md) | `sgd_step`, `momentum_step`, `adam_step`, `adamw_step` — **one signature, per-parameter state** |
| `days/day-008-gradient-descent-and-adam/lab/diagnose.py` | [1.3](parts/01-gradient-descent/1.3-the-learning-rate.md), [1.4](parts/01-gradient-descent/1.4-the-step-that-diverged.md) | `lr_range_test`, `log_step_health`, `assert_not_diverging` |
| `days/day-008-gradient-descent-and-adam/lab/memory.py` | [2.4](parts/02-adam/2.4-the-optimizers-memory.md) | `training_memory_report` for **your** planned model shape |
| `tests/test_optim.py` | [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md), [2.3](parts/02-adam/2.3-bias-correction.md), [2.6](parts/02-adam/2.6-the-optimizer-state-that-outlived-its-parameters.md), [3.1](parts/03-together/3.1-overfit-one-batch.md) | the descent test, the first-step test, the resume test, **the overfit-one-batch test** |

```text
TODO(me): derive 2/L on paper for f(w) = 5w^2 and for f(w) = 0.5*(w0^2 + 100*w1^2), then
          verify each by sweeping until it diverges. Two predictions, two confirmations.
          Report the grid resolution you used — a prediction confirmed on a coarse grid is
          a weaker confirmation and the write-up should say so.

TODO(me): write momentum BOTH ways -- v = b*v + g and v = b*v + (1-b)*g -- and find the
          learning rates at which they behave identically. State the relationship between
          the two rates as a formula, then explain why a config file that omits the
          convention is underspecified.

TODO(me): implement adam_step and assert its FIRST step is exactly lr for three gradient
          magnitudes spanning six orders of magnitude. Then delete only the v-hat line and
          record the new first step. Predict it from the table in part 2.3 first.

TODO(me): run part 2.5's AdamW-vs-Adam+L2 comparison with YOUR OWN choice of curvatures and
          optimum, and report the disparity ratio you get. Then answer in writing: what
          property of your surface made the ratio come out at the value it did?

TODO(me): compute the training memory for the model you expect to build on Day 39 -- your
          own parameter count, your own optimizer, with and without mixed precision. Show
          the arithmetic. Day 66 will check this prediction against a real GPU.

TODO(me): write the overfit-one-batch test as a pytest test, then BREAK it five ways --
          flip the update sign, freeze one parameter tensor, shift the labels by one, mask
          the loss to zero, and start t at 0 -- and record which failure message each one
          produced. One of the five will still pass; find out which and say why.
```

---

## §5 The eval that must be able to fail

Five checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_optim.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| flip the sign in the update | the loss rises smoothly and looks like training | the one-step descent test |
| set `lr` 1% above `2/L` | no `nan` in 4000 steps, and no convergence either | the divergence-trend test |
| delete the `v̂` bias-correction line | the first step is `31.6×` `lr` instead of `1×` | the first-step test |
| reset `t` to 1 on resume | converged parameters move by `4.2e-03`; loss changes 31× | the resume test |
| freeze one parameter tensor | the loss plateaus far above zero on 16 examples | **the overfit-one-batch test** |

The fifth row is the day's centrepiece and the plan's Principle 12. **It is also the cheapest test in
the curriculum** — sixteen examples, a fraction of a second, and it catches five distinct classes of
bug that all present as "the loss plateaued".

The fourth row is worth doing by hand, because **the buggy version produced a lower loss** — `4.28e-05`
against the correct `1.33e-03`. A bug that is rewarded is a bug that survives.

---

## §6 Compute budget

**Tier: T0.** numpy on a laptop CPU, on a two-parameter quadratic and a `(16, 8) × (8, 4)` linear
layer.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed today |
| Disk | negligible |

The heaviest thing today is a hundred thousand iterations of a two-element update, and part
[2.4](parts/02-adam/2.4-the-optimizers-memory.md)'s deliberate 74.5 GiB allocation failure, which is
instant because it never allocates.

What T0 proves: **every structural claim in this day.** The `2/L` bound, the `2(1+β)/L` bound with
momentum, the `3.162×` bias-correction factor, the `91×` decay disparity, the `31×` resume difference
and the whole memory table are properties of the arithmetic and the geometry, not of the hardware, and
they reproduce at seed **1337** on any conforming machine.

What T0 **cannot** show is the two things optimizers exist for at scale. First, **gradient noise**: a
full-batch quadratic has none, so momentum's variance-reduction half and Adam's robustness to noisy
gradients are named here and measured on Day 25. Second, **a surface whose curvature changes as you
move**, which is what makes schedules and warmup necessary — Day 55. **This day gives you the exact
answers on the surface where exact answers exist**, and names precisely what it is not covering.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| A gradient that broadcasts instead of matching | `(4,)` against `(8, 4)` — every weight in a column gets the same update, no error | [1.1](parts/01-gradient-descent/1.1-the-loss-surface.md) |
| Reading a flattening loss curve as convergence | one number averaging over directions that are doing opposite things | [1.1](parts/01-gradient-descent/1.1-the-loss-surface.md) |
| A wrong update sign | a smooth, monotone, plausible curve — **pointing up** | [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md) |
| Gradients not zeroed | descends for two steps, then walks past the optimum and away | [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md) |
| `params = params - lr*g` instead of `-=` | a second full copy of every tensor, every step | [1.2](parts/01-gradient-descent/1.2-gradient-descent-one-step.md) |
| `lr` far too small | fifty steps, 10% progress, no warning — indistinguishable from a hard problem | [1.3](parts/01-gradient-descent/1.3-the-learning-rate.md) |
| `lr` exactly at `2/L` | a **perfectly flat** loss curve at the starting value, forever | [1.3](parts/01-gradient-descent/1.3-the-learning-rate.md) |
| `lr` 1% above `2/L` | 4000 steps, no `nan`, no convergence, unrecoverable from step 1 | [1.4](parts/01-gradient-descent/1.4-the-step-that-diverged.md) |
| Waiting for `nan` to detect divergence | the cause is ~1940 steps before the symptom | [1.4](parts/01-gradient-descent/1.4-the-step-that-diverged.md) |
| Concluding "it converged, so the rate was fine" | on a convex saturating loss, `lr = 5000` also converges | [1.4](parts/01-gradient-descent/1.4-the-step-that-diverged.md) |
| Quoting `lr` without the momentum convention | a factor of `1/(1−β)` between two configs that look identical | [1.5](parts/01-gradient-descent/1.5-momentum.md) |
| Assuming momentum's stability bound is `2/L` | it is `2(1+β)/L` — measured `0.0400` at `β = 0.99` | [1.5](parts/01-gradient-descent/1.5-momentum.md) |
| `v = b2*v + (1-b2)*(g**2).sum()` | a scalar divisor — per-parameter scaling silently switched off | [2.1](parts/02-adam/2.1-one-learning-rate-is-not-enough.md) |
| `ε` inside the square root | a **99×** difference in the step for small-gradient parameters | [2.1](parts/02-adam/2.1-one-learning-rate-is-not-enough.md) |
| `t` starting at 0 | `ZeroDivisionError` in Python, `inf` then `nan` in numpy | [2.2](parts/02-adam/2.2-adam.md) |
| Writing `m̂` back into `m` | the correction compounds; `5.26` where `1.0` was correct, at `t = 2` | [2.2](parts/02-adam/2.2-adam.md) |
| "Uncorrected early steps are too small" | they are **3.16× too large** | [2.3](parts/02-adam/2.3-bias-correction.md) |
| Estimating training memory as `params × 4` | wrong by **4×** for Adam; the failure arrives at the optimizer step | [2.4](parts/02-adam/2.4-the-optimizers-memory.md) |
| "Mixed precision halves the memory" | at the parameter level it changes it by **exactly zero** | [2.4](parts/02-adam/2.4-the-optimizers-memory.md) |
| `Adam(weight_decay=...)` | that is L2 inside the adaptive step — a **91×** per-parameter disparity | [2.5](parts/02-adam/2.5-adamw.md) |
| Weight-decaying layer-norm gains | a gain of `1.0` becomes `4.5e-05` in 10,000 steps, silently | [2.5](parts/02-adam/2.5-adamw.md) |
| Resuming by loading weights and rebuilding the optimizer | `m`, `v` and `t` all dropped; no error | [2.6](parts/02-adam/2.6-the-optimizer-state-that-outlived-its-parameters.md) |
| Accepting "the loss always jumps a bit on restart" | a correct resume is **indistinguishable** from not stopping | [2.6](parts/02-adam/2.6-the-optimizer-state-that-outlived-its-parameters.md) |
| Reading "overfit one batch passed" as quality | it proves the machinery, not the model | [3.1](parts/03-together/3.1-overfit-one-batch.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement.** Today it appears twice, and
both times the *bug produced a better number*.

Part [2.6](parts/02-adam/2.6-the-optimizer-state-that-outlived-its-parameters.md) measures a resume
that dropped Adam's step counter reaching a final loss of `4.28e-05` where the correct resume reached
`1.33e-03` — **thirty-one times "better"**. Part
[2.3](parts/02-adam/2.3-bias-correction.md) measures a run with the bias correction deleted reaching
`2.96e+01` after five steps where the correct one reached `4.56e+01`. In both cases a single-number
comparison endorses the broken version, and the only way to tell is to check the *mechanism* — is `t`
continuous across the resume, is the first step exactly `lr` — rather than the outcome. **A metric that
moved in the direction you wanted is not evidence that the change was correct**, and §6's fix — three
seeds, report the spread — does not help here either, because the bug is deterministic.

**Silent Failure #3 is what part [3.1](parts/03-together/3.1-overfit-one-batch.md) exists to catch.** A
loss computed over padding or masked positions produces a curve that descends and plateaus, which is
indistinguishable from a hard problem — until you demand that sixteen examples be memorised, where
"hard" is not an available explanation.

---

## §8 Verify before you code

Everything today is numpy 2.5.2 (pinned Day 2) and the standard library. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| **arXiv:1412.6980** — *Adam: A Method for Stochastic Optimization* | abstract opened at `https://arxiv.org/abs/1412.6980` on **2026-08-26**; confirmed the title and that the method is "based on adaptive estimates of lower-order moments". **The abstract does not state default hyperparameters** — part 2.2 carries a `TODO(verify)` with the lookup rather than attributing `0.9`/`0.999`/`1e-8` to the paper. |
| **arXiv:1711.05101** — *Decoupled Weight Decay Regularization* | abstract opened at `https://arxiv.org/abs/1711.05101` on **2026-08-26**; confirmed the claim that L2 and weight decay "are equivalent for standard stochastic gradient descent (when rescaled by the learning rate)" but not for adaptive methods, and that "many implementations misleadingly call L₂ regularization weight decay" |
| `numpy` doc `reference/generated/numpy.zeros_like.html` | allocating optimizer state with the parameter's exact shape and dtype |
| `numpy` doc `reference/generated/numpy.linalg.norm.html` | the update-to-weight ratio in parts 1.3 and 1.4 |
| `numpy` doc `reference/generated/numpy.median.html` | used instead of `mean` in the divergence-trend check, so one noisy step cannot fire it |
| `numpy` doc `reference/generated/numpy.ptp.html` | confirmed `np.ptp` exists as a **function** in numpy 2.5.2 (the ndarray method was removed in numpy 2.0) — used in Day 7 part 2.5's collapse check |
| `numpy` doc `reference/generated/numpy.errstate.html` | which warnings the divergence demonstrations must suppress |
| Day 3 part 2.5's own output | that gradients accumulate, and where `zero_grad` belongs in the four-line loop |
| Day 4 part 1.2's own output | `dW` and `db` shapes, and the assertion that a gradient matches its parameter |
| Day 7 part 1.5's own output | `fp16` weight `1.0` unchanged after 1000 steps at `lr·g = 1e-05` — the update that rounds away |
| Day 6 part 3.2's own output | that an untrained `V`-way model starts at `ln(V)` — part 3.1's step-zero check |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.12, numpy 2.5.2**,
seed **1337** where randomness is involved, on **2026-08-26**. No figure was recalled and none came
from another machine. Where a value is a *convention* rather than a measurement — `β₁ = 0.9`,
`β₂ = 0.999`, `ε = 1e-8`, `lr = 1e-3` — the part that uses it says so in those words.

---

## §9 Say it in an interview

"The thing I got wrong for a long time was thinking the learning rate was a tuning knob rather than the
algorithm. For a quadratic it's exact: gradient descent converges if and only if `lr < 2/L`, and `L` is
the *largest* curvature across every direction — so the most sensitive parameter in the model sets the
step size for all of them. I measured that at 1% past the boundary you get four thousand steps with no
`nan` and no convergence, so the run was dead from step one and looked completely normal for its first
hour. That's why I log the update-to-weight ratio and `max|param|` rather than waiting for a `nan` —
by the time the loss is `nan` the cause is about two thousand steps back. The condition-number problem
is what Adam actually solves: dividing each parameter's step by the running RMS of its own gradients
makes `lr` a distance rather than a gradient multiplier, which is why Adam's learning rate transfers
across architectures where SGD's doesn't. Two things about it I'd flag. The bias correction is usually
explained backwards — because `β₂` biases the second moment by a thousand and it enters under a square
root, the uncorrected first step is `√1000/10 = 3.16×` too *large*, not too small. And `Adam(weight_decay=...)`
is L2 inside the adaptive step, so the decay each parameter feels gets divided by its own gradient
magnitude — I measured 9.09% shrinkage on one parameter and 0.10% on another from a single `λ`, a 91×
disparity. AdamW moves it outside the division and both come out at 0.475%. The other thing I always
do first, though, is overfit one batch: sixteen examples, no regularisation, train until the loss is
essentially zero. If it plateaus, it's a bug — sign, detached gradient, label misalignment, masked loss
— and not a hyperparameter, and finding that out costs a second instead of a GPU session."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 8` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 8 | 2026-08-26 | MATH-15, MATH-16 | 12 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; numpy was pinned on Day 2.

`docs/DATASETS.md`, `docs/MODELS.md` — **no rows today.** Nothing was downloaded.

`docs/RUNS.md` — **no rows today**, and the distinction matters. Part
[3.1](parts/03-together/3.1-overfit-one-batch.md) minimises a real loss with a real optimizer, but on
sixteen synthetic examples from a seeded generator with no held-out set. **It is a test, not a run.**
The first `RUNS.md` row is Day 25's, and it will carry the `overfit-1-batch passed` that this day built.

Commit:

```text
day 008: Gradient descent and Adam — closes MATH-15, MATH-16
```
