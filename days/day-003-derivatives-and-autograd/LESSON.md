---
day: 3
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Derivatives by hand and a scalar autograd engine"
ids: ["MATH-04", "MATH-05"]
principles: [1, 2, 3, 8, 10, 11, 12, 16, 17, 18]
kind: math
plan_version: "v1.3.0"
parts: 12
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 3 — Derivatives by hand, and a scalar autograd engine

> **Yesterday (Day 2):** what a tensor actually is — a flat buffer plus shape, strides, dtype and
> device — and the two permissive rules, broadcasting and matmul, that every later line of model code
> obeys, together with the four ways they produce a right-shaped wrong answer.
> **Today:** the other half of the ground. What a derivative *is*, why sensitivities multiply along a
> path and add across paths, why the backward direction is the cheap one — and then an engine, written
> from nothing, that differentiates any expression you can type.
> **Tomorrow (Day 4):** the same walk with matrices instead of scalars — the backward pass of a linear
> layer, the transpose everyone gets wrong, and finite differences used as a proof (MATH-06, MATH-07).

---

## §1 Where we are

Yesterday's tensors are containers. Today is the first thing that *moves*.

Here is the whole problem, stated without a single technical word. You have a knob and a number. Turning
the knob changes the number. You would like to know, before you turn it, **which way to turn it and how
far** — and you would like to know that for a hundred million knobs at once, for a number that is
computed from all of them through a long tangle of arithmetic.

The first half of the answer is small enough to fit in a sentence: nudge one knob a tiny bit and see how
much the number moved, per unit of nudge. That is a derivative, and there is nothing more to it than
that. The second half is the observation that makes the hundred million knobs affordable. When one thing
feeds another which feeds another, the sensitivities **multiply** along the path — three parts per
notch, two assemblies per part, five pounds per assembly, thirty pounds per notch — and each of those
three numbers was known locally, by a machine that had no idea the other two existed. And when one
thing reaches the answer by more than one route, its sensitivities **add**.

Multiply along, add across. That is the entire calculus of this curriculum, and everything after it is
bookkeeping.

The bookkeeping turns out to matter enormously, though, and that is the second half of the day. There
is a walk through the tangle that answers the question for **every** knob in roughly one pass, and a
walk that answers it for one knob per pass. With one number at the end and a hundred million knobs at
the start, those two are not close: one of them is a training run and the other is not a field. The
cheap direction is backwards, from the answer towards the knobs, which is why the algorithm has the
name it has.

Then you build it. About sixty lines, no libraries, and at the end an ordinary Python expression
constructs its own graph as a side effect of being evaluated, and one call fills in every derivative.
It is the same object that sits at the centre of every framework you will ever use, with a float where
they have an array.

And then — because this curriculum does not stop at the thing working — you measure what it costs, and
find that a 32×32 matrix multiply crashes it. That is not a disappointment. It is the argument for the
next change, and knowing precisely *why* the toy fails is what makes the real thing legible instead of
magical.

Everything today runs on the laptop, in pure Python. Four of the twelve parts are failures reproduced
on purpose, because every one of the ways this can go wrong produces a plausible number rather than an
error.

---

## §2 The map

Twelve parts, three sections. Section 1 is MATH-04 (the mathematics), section 2 is MATH-05 (the engine),
and section 3 is where the engine meets reality. The day climbs
`foundation → working → production`, and each section ends with something breaking.

### Section 1 — `01-the-derivative`: MATH-04, what a derivative is and how they compose

From the nudge question to the graph, in five steps: define it, chain it, generalise it to many inputs,
see it as a graph, then break the numerical version on purpose.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [The slope, from the definition](parts/01-the-derivative/1.1-the-slope-from-the-definition.md) | What question does a derivative actually answer? | `foundation` |
| 1.2 | [The chain rule](parts/01-the-derivative/1.2-the-chain-rule.md) | Why can three people who never spoke measure a sensitivity between them? | `working` |
| 1.3 | [Partial derivatives](parts/01-the-derivative/1.3-partial-derivatives.md) | When one input reaches the output twice, what happens to its two sensitivities? | `working` |
| 1.4 | [The graph, forward and backward](parts/01-the-derivative/1.4-the-graph-forward-and-backward.md) | Why is the backward direction the cheap one, and when would it not be? | `working` |
| 1.5 | [💥 The finite difference that lied](parts/01-the-derivative/1.5-the-finite-difference-that-lied.md) | "Smaller `h` is better" — up to where, and what happens past it? | `production` |

### Section 2 — `02-the-autograd-engine`: MATH-05, sixty lines that differentiate anything

One idea per document: the node, the local rule, the ordering, the accumulation, and the state that
leaks. The last two are failures, and both are one character.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [A Value that remembers](parts/02-the-autograd-engine/2.1-a-value-that-remembers.md) | Where does the computation graph come from, if nobody wrote one? | `foundation` |
| 2.2 | [The local derivative](parts/02-the-autograd-engine/2.2-the-local-derivative.md) | What is the one line every operation's backward pass contains? | `working` |
| 2.3 | [Topological order](parts/02-the-autograd-engine/2.3-topological-order.md) | Why can't the backward pass just recurse from the loss? | `working` |
| 2.4 | [💥 Accumulate, never assign](parts/02-the-autograd-engine/2.4-accumulate-never-assign.md) | How does one character halve every gradient behind a residual connection? | `production` |
| 2.5 | [💥 zero_grad, the state that leaks](parts/02-the-autograd-engine/2.5-zero-grad-the-state-that-leaks.md) | Why can't the engine clear the gradients for you? | `production` |

### Section 3 — `03-scaling-up`: what the engine costs, and what it retains

The engine is correct. This section is what happens when you point it at something real.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [From scalars to tensors](parts/03-scaling-up/3.1-from-scalars-to-tensors.md) | What exactly stops you training a model with this, and what single change fixes it? | `production` |
| 3.2 | [💥 The graph that was never freed](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md) | Why does keeping one number cost you every step's graph? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything in section 1 and section 2 is the standard library. `numpy` —
pinned yesterday — appears only to *generate inputs* for the benchmarks in parts 1.4 and 3.1, never to
compute a derivative.

```bash
# nothing to install. Confirm what you already have:
uv run python -c "import sys, numpy; print(sys.version.split()[0], numpy.__version__)"

# today's scratch space
./m scaffold 3

# the engine goes in your lab, not in akshara/ — it is a teaching artifact,
# and the tensor version that replaces it arrives later (part 3.1)
touch days/day-003-derivatives-and-autograd/lab/engine.py
touch days/day-003-derivatives-and-autograd/lab/test_engine.py
```

One standard-library import worth knowing before part
[2.1](parts/02-the-autograd-engine/2.1-a-value-that-remembers.md) and part
[3.2](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md): `tracemalloc`, which reports what the
allocator has actually handed out. Both parts use it instead of `sys.getsizeof`, and both say why.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `lab/engine.py` | [2.1](parts/02-the-autograd-engine/2.1-a-value-that-remembers.md), [2.2](parts/02-the-autograd-engine/2.2-the-local-derivative.md), [2.3](parts/02-the-autograd-engine/2.3-topological-order.md) | `Value` with `data`, `grad`, `_prev`, `_backward`; `+`, `*`, `**`, `tanh`, `exp`, the reflected operators, and `backward()` |
| `lab/test_engine.py` | [2.3](parts/02-the-autograd-engine/2.3-topological-order.md), [2.4](parts/02-the-autograd-engine/2.4-accumulate-never-assign.md), [2.5](parts/02-the-autograd-engine/2.5-zero-grad-the-state-that-leaks.md) | the fan-out test, the accumulation test, the leak test — each watched **red** before green |
| `lab/sweep.py` | [1.5](parts/01-the-derivative/1.5-the-finite-difference-that-lied.md) | the `h` sweep, on **your** machine, and the `h` you will use on Day 4 |
| `lab/cost.py` | [3.1](parts/03-scaling-up/3.1-from-scalars-to-tensors.md), [3.2](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md) | the scalar-vs-numpy timing at two sizes, and the memory-slope measurement |

```text
TODO(me): replace the recursive topological sort with an iterative one (part 3.1 shows the
          shape). Then re-run the N=32 matmul from part 3.1 and record what happens —
          it should stop raising and start merely being slow. Both facts are the finding.

TODO(me): add `log()` to the engine. Derivative: d ln(x)/dx = 1/x. Then write its gradient
          check AND its edge case: what does your implementation do at x = 0, and what
          SHOULD it do? Day 6 needs this and will meet real zeros.

TODO(me): add a `draw()` that walks _prev and prints the graph as a mermaid diagram, using
          _op as the node label. You will use it every time a gradient surprises you.

TODO(me): write `numeric_grad(f, args, i)` as a reusable helper, with the h you measured in
          lab/sweep.py — not the h this document used. Day 4 imports it.

TODO(me): work out on paper what `_prev` being a set (rather than a list) means for the
          expression x * x. How many entries? How many gradient contributions? Write the
          two numbers down and say why they differ.
```

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11). Three of them go
red by a one-character edit, which is the point.

```bash
# 1 - fan-out: the traversal must not push a half-finished gradient
uv run python -c "
from lab.engine import Value
a = Value(3.0); b = a * 2
((b + 1) + (b * 3)).backward()
print('dL/da =', a.grad, ' expected 8.0')
"

# 2 - accumulation: the same node used twice must sum its contributions
uv run python -c "
from lab.engine import Value
x = Value(3.0); (x * x).backward()
print('d(x*x)/dx =', x.grad, ' expected 6.0')
"

# 3 - no leak between steps: three identical steps, three identical gradients
uv run python -c "
from lab.engine import Value
w = Value(1.0); out = []
for _ in range(3):
    w.grad = 0.0
    (w * w * 3).backward()
    out.append(w.grad)
print(out, ' expected [6.0, 6.0, 6.0]')
"

# 4 - the engine agrees with an independent method
#     run lab/sweep.py first; use YOUR measured h, not this document's
```

**How to make each one go red, and what you should see:**

- Check 1: move `order.append(node)` **above** the `for child` loop in `backward()`. Expect a number
  that is not `8.0`.
- Check 2: change one `+=` to `=` in `__mul__`'s closure. Expect `3.0` — exactly half. **Note that
  check 1 still passes**, which is why both tests exist.
- Check 3: delete the `w.grad = 0.0`. Expect `[6.0, 12.0, 18.0]`.
- Check 4: use `h = 1e-16`. Expect the numerical side to return `0.0` and the check to pass or fail for
  reasons that have nothing to do with your gradients.

---

## §6 Compute budget

**Tier: T0.** Pure Python on a laptop CPU.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU, and nothing today needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages are installed today |
| Disk | negligible |

The heaviest thing you will run is the scalar matmul benchmark in part
[3.1](parts/03-scaling-up/3.1-from-scalars-to-tensors.md), which measured 113 ms at `N = 24` on the
reference machine and **raises `RecursionError` at `N = 32`**. The memory experiment in part
[3.2](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md) peaks at about 76 MiB for the
deliberately-broken variant.

What T0 proves today: the **mathematics** (exact, hardware-independent), the **algorithm** (a backward
pass is one traversal, and the ordering constraint is real and measurable), and the **failure modes**
(all four reproduce in microseconds). What it does not prove: any statement about a real framework's
speed. The 52,523× in part 3.1 is this implementation against numpy on this laptop and belongs to
nobody else.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| `w = w - lr * grad` with a `+` | the loss climbs smoothly; looks like "not learning yet" | [1.1](parts/01-the-derivative/1.1-the-slope-from-the-definition.md) |
| Assuming a small local derivative is harmless | `0.5 ** 50 = 8.9e-16`, nine orders below `float32` eps — the update is exactly zero | [1.2](parts/01-the-derivative/1.2-the-chain-rule.md) |
| Taking one route of a fan-out | `8.0` or `6.0` instead of `14.0`; both plausible, neither right | [1.3](parts/01-the-derivative/1.3-partial-derivatives.md) |
| A severed graph | some parameters never move; no error, no warning | [1.4](parts/01-the-derivative/1.4-the-graph-forward-and-backward.md) |
| `h = 1e-16` "to be safe" | the derivative of `sin` measures **exactly `0.0`** | [1.5](parts/01-the-derivative/1.5-the-finite-difference-that-lied.md) |
| A gradient check in `float32` with a `float64` tolerance | a failing test on a correct gradient | [1.5](parts/01-the-derivative/1.5-the-finite-difference-that-lied.md) |
| Gradient-checking a ReLU at zero | the central difference returns `0.5`; no framework returns `0.5` | [1.5](parts/01-the-derivative/1.5-the-finite-difference-that-lied.md) |
| A closure reading `self.data` instead of capturing it | correct today, wrong from Day 8 when the optimizer mutates `.data` | [2.2](parts/02-the-autograd-engine/2.2-the-local-derivative.md) |
| `order.append` before the child loop | `14.0` instead of `8.0`, and 12,285 calls instead of 36 | [2.3](parts/02-the-autograd-engine/2.3-topological-order.md) |
| `=` instead of `+=` in a backward | exactly half the gradient — and a chain-only test suite passes | [2.4](parts/02-the-autograd-engine/2.4-accumulate-never-assign.md) |
| Forgetting `zero_grad` | 6, 12, 18, 24 — and a run that diverges at *any* learning rate | [2.5](parts/02-the-autograd-engine/2.5-zero-grad-the-state-that-leaks.md) |
| `zero_grad` after the step, with a `continue` above it | leaks only on iterations following a skip — looks like noise | [2.5](parts/02-the-autograd-engine/2.5-zero-grad-the-state-that-leaks.md) |
| Benchmarking at one size | 0.24 ms at `N = 4` says nothing; the cost grows as `N³` | [3.1](parts/03-scaling-up/3.1-from-scalars-to-tensors.md) |
| `losses.append(loss)` instead of `loss.data` | memory grows linearly with the step count, forever | [3.2](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md) |
| A running average built from live nodes | the same leak with no list to notice | [3.2](parts/03-scaling-up/3.2-the-graph-that-was-never-freed.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement**, and today it arrives through
*the gradient itself* rather than through a seed or a shape. Every one of the four deliberate failures
produces a run that still trains: part 2.4 halves the gradients behind every residual connection, part
2.5 grows them linearly with the step count, part 2.3's ordering bug inflates them by a factor of
nearly two, and part 1.5's badly-chosen `h` makes the check that would have caught any of them either
fire spuriously or pass on a broken gradient. None of these is noise, so **running more seeds does not
find any of them** — which is precisely why they are dangerous, and why today's answer is a value check
against hand-computed arithmetic rather than a statistical one. Day 4 makes that check formal and
Day 119 makes the statistical half formal.

---

## §8 Verify before you code

Everything today is standard-library Python plus the numpy pinned yesterday. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| `https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types` | the exact names and dispatch order of `__add__`, `__mul__`, `__pow__` and the reflected `__r*__` forms |
| `https://docs.python.org/3/library/tracemalloc.html` | that `get_traced_memory()` returns `(current, peak)` — parts 2.1 and 3.2 read index `0` |
| `https://docs.python.org/3/library/math.html` | `math.tanh`, `math.exp` — and that both raise `OverflowError` rather than returning `inf` |
| `https://docs.python.org/3/library/sys.html#sys.setrecursionlimit` | that the limit is a guard against a real stack overflow, not an arbitrary cap |
| `numpy` doc `reference/random/generator.html` | `default_rng(seed)`, used only to generate benchmark inputs reproducibly |
| Day 2 part 1.2's own output | `float32` eps `1.1920929e-07` and `float64` eps `2.220446049250313e-16`, both re-used in parts 1.2 and 1.5 |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.10**, with
**numpy 2.5.2** where inputs were generated, seed **1337**, on **2026-08-26**. No figure in this day was
recalled and none came from another machine.

---

## §9 Say it in an interview

"I wrote a scalar autograd engine before I used a framework, and the two things I took from it were not
the ones I expected. The first is that every operation only ever needs to know its own derivative — the
chain rule is a product along a path and a sum across paths, and that locality is the whole reason a
hundred-million-parameter model is differentiable at all. The second is how *quiet* the failure modes
are. I changed `+=` to `=` in one backward pass and `d(x·x)/dx` went from 6 to 3 — exactly half, no
error — and every test I had at the time still passed, because they were all straight chains with no
value used twice. That's the bug that halves the gradient behind every residual connection in a
transformer. I also measured what the engine costs before deciding it was a toy: 52,000× slower than
numpy on a 24×24 matmul, 512 bytes a node against 8, and a `RecursionError` on a 32×32. That last one
was useful, because it told me the fix isn't a faster node — it's one node per array — and that's
exactly what a real framework is."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 3` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 3 | 2026-08-26 | MATH-04, MATH-05 | 12 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed. Everything in section 1 and section 2 is
the standard library, and the numpy used to generate benchmark inputs was pinned on Day 2.

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The timings in parts 1.4, 3.1 and 3.2 are microbenchmarks; they belong in the parts
that measured them, next to the hardware line, and not in the run ledger.

Commit:

```text
day 003: Derivatives by hand and a scalar autograd engine — closes MATH-04, MATH-05
```
