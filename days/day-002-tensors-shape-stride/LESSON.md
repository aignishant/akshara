---
day: 2
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Tensors — shape, stride, dtype, device"
ids: ["MATH-01", "MATH-02", "MATH-03"]
principles: [1, 2, 3, 6, 7, 8, 10, 11, 15, 16, 17, 18, 20]
kind: math
plan_version: "v1.3.0"
parts: 13
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 2 — Tensors: shape, stride, dtype, device

> **Yesterday (Day 1):** the repository became Akshara's memory — a layout that says what it refuses
> to hold, one home for the Hugging Face token, the ledgers that record what a checkpoint cannot, and
> the free-compute accounts with their costs measured rather than assumed.
> **Today:** the first mathematics. What a tensor actually is in memory, the four independent things
> that describe it, the two rules — broadcasting and matmul — that every later line of model code
> obeys, and the four ways those rules produce a right-shaped wrong answer.
> **Tomorrow (Day 3):** derivatives from the definition, and a scalar autograd engine you write
> yourself (MATH-04, MATH-05).

---

## §1 Where we are

Open a book and you will find a picture of a tensor: a cube of numbers, drawn as a stack of grids.
It is a good picture for arithmetic and a bad picture for everything else, because it is not what is
in the machine.

What is in the machine is a straight line. Memory is one long row of numbered slots, and there is no
second dimension in it. When a program says it holds a 2×3×4 block, the numbers are lying end to end
exactly as they always were, and what makes them a block is a small note carried alongside: how many
along each axis, and how far to walk in the line when you take one step along each. Finding "block 1,
row 2, seat 3" is not a search. It is one line of arithmetic.

That sounds like a detail and it decides how you read code for the next hundred and fifty-nine days.
If a tensor is a cube, then swapping two of its axes must rebuild the cube, and you will write your
transformer defensively around an operation you think is expensive. If a tensor is a line plus a note,
you know that swapping axes rewrites the note and costs nothing — and you also know exactly where the
bill turns up instead, which is in the operation *after* it.

Then there are two rules for combining tensors, and they are the two rules the whole field runs on.
The first says that when two shapes nearly match, the library will quietly stretch the mismatched
part rather than complain. The second says that a matrix multiply pairs up one shared axis, consumes
it, and keeps the rest. Both rules are generous. Both were designed to let you write what you mean
without ceremony, and both will accept, without a murmur, an operation that is not what you meant.

So the day has a shape: five documents on what a tensor is, three on how tensors combine, four on the
one operation that dominates everything you will ever run, and one at the end on what happens when the
two rules meet and the sizes coincide. Four of those thirteen are failures reproduced on purpose,
because the failures here do not raise. They return a finite array of the right shape and the wrong
numbers, and the only thing standing between you and a model that is quietly worse than the one you
designed is knowing, today, which checks see through that and which do not.

Everything runs on the laptop. Nothing today needs a GPU, and every number in every part was measured
on this machine on the day it was written.

---

## §2 The map

Thirteen parts, four sections. Sections 1–3 are one per curriculum ID; section 4 is the synthesis,
where two of them meet and the day's hardest failure lives. The day climbs
`foundation → working → production` and every section ends with something breaking.

### Section 1 — `01-what-a-tensor-is`: MATH-01, the four independent properties

A tensor is a flat buffer plus a description. This section separates the description into its four
parts — shape, dtype, strides, device — and shows that each one is a knob you can turn without
touching the others.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [The array that is actually flat](parts/01-what-a-tensor-is/1.1-the-array-that-is-flat.md) | If memory is one straight line, what makes it a grid? | `foundation` |
| 1.2 | [dtype — the width of a number](parts/01-what-a-tensor-is/1.2-dtype-the-width-of-a-number.md) | What does choosing a dtype silently fix, besides how much memory it takes? | `working` |
| 1.3 | [Strides and the free transpose](parts/01-what-a-tensor-is/1.3-strides-and-the-free-transpose.md) | A transpose costs nothing — so where does the cost actually appear? | `working` |
| 1.4 | [Device — where the bytes live](parts/01-what-a-tensor-is/1.4-device-where-the-bytes-live.md) | Why is a device mismatch an error rather than an automatic conversion? | `production` |
| 1.5 | [💥 The view that changed the original](parts/01-what-a-tensor-is/1.5-the-view-that-changed-the-original.md) | How does a function with a harmless name destroy its caller's data with no error? | `production` |

### Section 2 — `02-broadcasting-and-indexing`: MATH-02, the rules that stretch and select

Two conveniences that are load-bearing in every transformer — and the shape confusion that costs more
debugging hours than any other in the field.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Broadcasting — the rule in three lines](parts/02-broadcasting-and-indexing/2.1-broadcasting-the-rule.md) | How do two different shapes combine without copying anything? | `foundation` |
| 2.2 | [Indexing — view or copy](parts/02-broadcasting-and-indexing/2.2-indexing-view-or-copy.md) | Which selections re-label the buffer and which allocate a new one? | `working` |
| 2.3 | [💥 The (N, 1) that should have been (N,)](parts/02-broadcasting-and-indexing/2.3-the-n1-versus-n-bug.md) | Why does this bug hide at the start of training and only appear once the model is good? | `production` |

### Section 3 — `03-matmul`: MATH-03, the operation that is 90% of everything you will run

The definition by hand, then the library, then the batched form every model is written in, then the
ratio that explains why this operation and not another one.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Matmul is the primitive](parts/03-matmul/3.1-matmul-is-the-primitive.md) | What shape comes out, and how many operations did it cost? | `foundation` |
| 3.2 | [🔍 Three loops, then one call](parts/03-matmul/3.2-three-loops-then-one-call.md) | What exactly is the library buying you, and why do two correct versions disagree in the last bits? | `working` |
| 3.3 | [Batched matmul](parts/03-matmul/3.3-batched-matmul.md) | How does one call do a whole batch of matrix multiplies, and when does that stretch silently? | `working` |
| 3.4 | [Why hardware loves matmul](parts/03-matmul/3.4-why-hardware-loves-matmul.md) | Why is a matmul fast and an elementwise add slow, when the add does far less work? | `production` |

### Section 4 — `04-where-they-meet`: the synthesis, and the day's hardest failure

Sections 2 and 3 gave two permissive rules. One line of model code — `y = x @ W + b` — uses both. This
is what happens when two axis sizes coincide.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [💥 The shape was right and the answer was wrong](parts/04-where-they-meet/4.1-the-shape-was-right-the-answer-was-wrong.md) | What kind of check still works when a shape assertion cannot? | `production` |

---

## §3 Setup — run this

One package today, and it arrives **after** you have written the arithmetic by hand (Principle 3):
part [1.1](parts/01-what-a-tensor-is/1.1-the-array-that-is-flat.md) builds a strided tensor in plain
Python before numpy appears, and part
[3.1](parts/03-matmul/3.1-matmul-is-the-primitive.md) writes the matmul as three loops before `@`
appears.

```bash
# 1 - look the version up live. Never write a version from memory (Principle 6).
curl -s https://pypi.org/pypi/numpy/json \
  | python -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"

# 2 - pin exactly what your lookup printed
uv add numpy==<what your lookup printed>

# 3 - confirm what actually got installed, and record THAT in docs/PACKAGES.md
uv run python -c "import numpy; print(numpy.__version__)"

# 4 - the day's scratch space
./m scaffold 2
```

Everything in the parts was written and measured against **numpy 2.5.2**, resolved live from
`https://pypi.org/pypi/numpy/json` on 2026-08-26. If your lookup prints something else, pin what you
observed and note the difference — the shape rules will not have changed, but a printed repr or a
`GFLOP/s` figure may have.

Nothing else is installed today. `torch` arrives when the point becomes scale (plan §5), not before.

---

## §4 Build brief

The learner writes every line. Nothing here is solved for you.

| File | From | Contains |
| --- | --- | --- |
| `days/day-002-tensors-shape-stride/lab/flat_tensor.py` | [1.1](parts/01-what-a-tensor-is/1.1-the-array-that-is-flat.md) | `strides_for()` and `FlatTensor` with `offset` — plain Python, no numpy |
| `days/day-002-tensors-shape-stride/lab/naive_matmul.py` | [3.1](parts/03-matmul/3.1-matmul-is-the-primitive.md), [3.2](parts/03-matmul/3.2-three-loops-then-one-call.md) | the triple loop, plus the timing harness that compares it to `@` |
| `days/day-002-tensors-shape-stride/lab/shapes.md` | all parts | your own table: every `## Shapes` row you had to think about, in your words |

```text
TODO(me): extend FlatTensor with a `transpose()` that reverses shape and strides and
          shares `data`. Then write to the transposed view and show that the original
          changed. Part 1.5 is the argument; the demonstration is yours.

TODO(me): add a `contiguous()` to FlatTensor that returns a NEW FlatTensor whose data
          is in row-major order. Then time your `transpose().contiguous()` against
          numpy's `ascontiguousarray` at a size where the difference is visible, and
          write both numbers down with your hardware line.

TODO(me): write `assert_shape(x, expected, name)` — one helper, used everywhere from
          Day 3 onward. It must print BOTH the expected and the actual shape, and the
          name of the tensor. Part 4.1 explains why the message matters more than the
          assertion.

TODO(me): work out, on paper, the arithmetic intensity of `(1, C) @ (C, V)` and of
          `(B*T, C) @ (C, V)` for C=768, V=32000, B=8, T=1024, in float32. Two numbers.
          They are the reason Day 69 is slow and Day 154 is not.
```

---

## §5 The eval that must be able to fail

Three checks, and **every one must be observed red before it is green** (Principle 11).

```bash
# 1 - your hand-rolled offset must agree with numpy's strides
uv run python -c "
import numpy as np
a = np.arange(24, dtype=np.int32).reshape(2, 3, 4)
mine  = 1*(3*4) + 2*4 + 3*1
theirs = (1*a.strides[0] + 2*a.strides[1] + 3*a.strides[2]) // a.itemsize
print('mine', mine, 'theirs', theirs, 'agree', mine == theirs)
"

# 2 - your triple loop must match @ to a stated tolerance, and NOT exactly
#     (run your lab/naive_matmul.py; it must print allclose True and array_equal False)

# 3 - the shape trap must be reproducible on demand
uv run python -c "
import numpy as np
rng = np.random.default_rng(1337)
x = rng.standard_normal((2, 8, 8)); W = rng.standard_normal((8, 8))
print('same shape :', (x @ W).shape == (x * W).shape)
print('same values:', np.allclose(x @ W, x * W))
"
```

Check 1 goes red if you divide by `itemsize` in the wrong place — do that on purpose once and read the
number it prints. Check 2 goes red if you demand exact equality instead of `allclose`; try it, and
that failure *is* part [3.2](parts/03-matmul/3.2-three-loops-then-one-call.md)'s point. Check 3 must
print `True` then `False` — if it prints `True` twice, your numpy is doing something this day did not
predict and that is worth stopping for.

---

## §6 Compute budget

**Tier: T0.** Everything today is a laptop CPU.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Not "few" — zero. Nothing today can use a GPU and nothing today needs one. |
| Free notebook sessions | 0 |
| Network | one version lookup, one `uv add` |
| Disk | numpy's wheel; negligible otherwise |

The heaviest thing you will run is a 1024×1024 `float64` matmul, which measured 33.5 ms on the
reference machine. The pure-Python triple loop at N=128 measured 193 ms. If you raise N on the
pure-Python version, remember the cost is `2N³` — N=512 is 64 times the work of N=128, and that is a
demonstration worth doing once deliberately rather than by accident.

What T0 proves today: every **rule** — offsets, strides, dtype ranges, broadcasting alignment, matmul
shapes, arithmetic intensity as a ratio. All of those are exact and hardware-independent. What T0 does
**not** prove: any absolute speed. The `GFLOP/s`, `GB/s` and `×` figures in parts 1.3, 3.2 and 3.4 are
this machine's and belong to it alone (plan §4).

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Reading numpy's byte strides as element strides | your hand-computed offset is 4× off and the formula looks wrong | [1.1](parts/01-what-a-tensor-is/1.1-the-array-that-is-flat.md) |
| An integer counter that overflows | corpus statistics that go negative, with no warning at all | [1.2](parts/01-what-a-tensor-is/1.2-dtype-the-width-of-a-number.md) |
| `int32 + float32` | a `float64` result — twice as wide as either input, silently | [1.2](parts/01-what-a-tensor-is/1.2-dtype-the-width-of-a-number.md) |
| Assuming "non-contiguous is always slower" | measured here: a reduction over the *strided* axis was 3.6× **faster** | [1.3](parts/01-what-a-tensor-is/1.3-strides-and-the-free-transpose.md) |
| `reshape` on a transposed tensor | a silent copy, and your peak memory just doubled at that line | [1.3](parts/01-what-a-tensor-is/1.3-strides-and-the-free-transpose.md) |
| `.item()` inside the training step | a synchronisation every step; a correct loss curve at a fraction of the speed | [1.4](parts/01-what-a-tensor-is/1.4-device-where-the-bytes-live.md) |
| `x -= x.mean()` in a helper | the caller's raw data is gone; its mean prints as exactly `0.0` | [1.5](parts/01-what-a-tensor-is/1.5-the-view-that-changed-the-original.md) |
| A small slice kept from a big array | `nbytes` reports 80, the buffer pinned is 80,000,000 | [1.5](parts/01-what-a-tensor-is/1.5-the-view-that-changed-the-original.md) |
| `sum(axis=1)` without `keepdims` on a **square** tensor | no error; rows sum to 1.45, 0.76, 0.91 instead of 1 | [2.1](parts/02-broadcasting-and-indexing/2.1-broadcasting-the-rule.md) |
| A pairwise `x[:, None] - x[None, :]` | 762.9 MiB of output from two 80 KB inputs | [2.1](parts/02-broadcasting-and-indexing/2.1-broadcasting-the-rule.md) |
| A boolean mask on a rank-2 tensor | rank 1 out, structure silently gone | [2.2](parts/02-broadcasting-and-indexing/2.2-indexing-view-or-copy.md) |
| `(N,)` against `(N, 1)` | `(N, N)`, a loss 95× too large, and a plateau nothing moves | [2.3](parts/02-broadcasting-and-indexing/2.3-the-n1-versus-n-bug.md) |
| `==` between two float tensors | a test that fails for a reason that is not a bug | [3.2](parts/03-matmul/3.2-three-loops-then-one-call.md) |
| A batch axis that is accidentally `1` | it stretches instead of raising; every item processed against the first | [3.3](parts/03-matmul/3.3-batched-matmul.md) |
| Optimising the arithmetic of a memory-bound kernel | you make it cleverer and the runtime does not move | [3.4](parts/03-matmul/3.4-why-hardware-loves-matmul.md) |
| Test shapes that are all the same number | your test cannot detect an axis swap, and never will | [4.1](parts/04-where-they-meet/4.1-the-shape-was-right-the-answer-was-wrong.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement.** Today it arrives through
*shape* rather than through a seed, and it does so twice. Part
[2.3](parts/02-broadcasting-and-indexing/2.3-the-n1-versus-n-bug.md) inflates the loss by a constant
that does not depend on the model, so real improvements are compressed into a fraction of the reported
number and become indistinguishable from run-to-run variation. Part
[4.1](parts/04-where-they-meet/4.1-the-shape-was-right-the-answer-was-wrong.md) leaves the model a
constant, silent handicap of roughly the size you will later be trying to measure between real
changes. Neither is fixed by running more seeds — running more seeds is precisely what does **not**
work, because neither is noise. The check that finds them is a value comparison on a tiny input with
mutually distinct axis sizes, and Day 119 is where the statistical half becomes formal.

---

## §8 Verify before you code

Fetched and run on `2026-08-26`, not recalled (Principles 6, 7, 8):

| Source | Checked for |
| --- | --- |
| `https://pypi.org/pypi/numpy/json` | the current version (**2.5.2**) and its `requires_python` (`>=3.12`) — the pin in `pyproject.toml` |
| `numpy` doc `reference/generated/numpy.ndarray.strides.html` | that strides are counted in **bytes**, not elements |
| `numpy` doc `reference/generated/numpy.ndarray.itemsize.html` | the dtype width that converts between the two conventions |
| `numpy` doc `reference/generated/numpy.ndarray.device.html` and `numpy.ndarray.to_device.html` | that the array-API device interface exists in 2.x and accepts only `'cpu'` |
| `numpy` doc `reference/generated/numpy.broadcast_shapes.html` | the right-alignment rule, checked without allocating |
| `numpy` doc `reference/generated/numpy.broadcast_to.html` | that a stretched axis gets stride `0` and the view is read-only |
| `numpy` doc `reference/generated/numpy.shares_memory.html` | the exact overlap test, versus `may_share_memory`'s conservative one |
| `numpy` doc `reference/arrays.indexing.html` | the basic-versus-advanced indexing boundary, and the result-shape rule for index arrays |
| `numpy` doc `reference/generated/numpy.matmul.html` | the gufunc signature `(n?,k),(k,m?)->(n?,m?)` and the stacked-matrix Notes |
| `numpy` doc `reference/generated/numpy.iinfo.html`, `numpy.finfo.html` | the integer ranges and float `eps`/`max`/`tiny` printed in part 1.2 |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.10, numpy 2.5.2**,
seed **1337** where randomness is involved, on **2026-08-26**. No benchmark figure in this day was
recalled, and none was taken from any other machine.

---

## §9 Say it in an interview

"The thing that changed how I read model code was realising a tensor is a flat buffer plus a note —
shape, strides, dtype and device — and that those four are independent. Once that clicked, a
transpose stopped looking like a copy and started looking like a strides edit, and the interesting
question moved to the *next* line, which is where the layout bill actually arrives. I measured that on
my laptop: an elementwise add against a transposed operand cost 6.1× more than against a contiguous
one — but a reduction over the strided axis was 3.6× *faster* than over the contiguous one, which
taught me not to trust the rule without the measurement. The other thing I took from that week is
that the dangerous shape bugs don't raise. A `(N,)` minus a `(N, 1)` gives you `N²` differences and a
mean-squared error 95 times too large, and it puts a floor under the loss that no learning rate will
move. I write my tests with mutually distinct axis sizes now — 2, 3 and 5, never three 8s — because a
test with square shapes cannot see an axis swap, and I'd rather find that out on a laptop in a
millisecond than on a free GPU session two hours in."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 2` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 2 | 2026-08-26 | MATH-01, MATH-02, MATH-03 | 13 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — one row. Use **your** observed version, not this one, if the lookup differs:

```text
| numpy | 2.5.2 | 2026-08-26 | 2 | The numerics floor. Arrives after the hand-rolled strided tensor (part 1.1) and the hand-rolled matmul (part 3.1) exist, per Principle 3. Version resolved live from https://pypi.org/pypi/numpy/json; requires_python >=3.12, which matches the project pin. |
```

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The timings in parts 1.3, 3.2 and 3.4 are microbenchmarks, not runs; they belong
in the parts that measured them, next to the hardware line, and not in the run ledger.

Commit:

```text
day 002: Tensors — shape, stride, dtype, device — closes MATH-01, MATH-02, MATH-03
```
