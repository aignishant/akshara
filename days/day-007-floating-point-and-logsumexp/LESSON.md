---
day: 7
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Numerical reality — floating point and log-sum-exp"
ids: ["MATH-13", "MATH-14"]
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

# Day 7 — 💥 Numerical reality: fp32, fp16, bf16, and the softmax that returns NaN

> **Yesterday (Day 6):** the number the curriculum optimises — entropy, cross-entropy, KL and
> perplexity — and why minimising cross-entropy *is* maximum likelihood, with the padding failure that
> makes the reported loss fall while the real loss rises.
> **Today:** the machine that has to hold those numbers. What a float actually is, why the gaps between
> floats grow, what `fp16` and `bf16` each throw away, and the two operations — `exp` and `log` — that
> turn a correct formula into `inf`, `nan` or a silent bag of zeros. Then log-sum-exp, which fixes all
> of it.
> **Tomorrow (Day 8):** optimization — gradient descent, momentum, Adam and AdamW, and the learning
> rate as *the* hyperparameter (MATH-15, MATH-16).

---

## §1 Where we are

Six days of mathematics have assumed a machine that can hold a number. Today that assumption is
withdrawn.

Start with something everybody has met and almost nobody has been told the reason for: `0.1 + 0.2` is
not `0.3`. The usual explanation — "computers are imprecise" — is not an explanation, and it is the
reason the rest of this subject stays mysterious. The real answer is a formula. A number is stored as a
sign, a scale, and a handful of digits, and its value is the digits multiplied by two raised to the
scale. Everything surprising follows from that one line, mechanically, with no further mysteries: one
tenth is not a finite binary fraction, so it is stored as the nearest thing that is.

The consequence that matters is not the rounding. It is that **the spacing between the numbers a
machine can hold grows with the numbers themselves.** Near one, the gap is about a ten-millionth. Near
a million, it is a sixteenth. Near ten thousand, in a sixteen-bit format, it is eight. So a running
total eventually grows large enough that the thing you are adding falls into the gap between two
representable values and disappears — and the total simply stops. Measured today: ten thousand
additions of `0.1` in `float16` gives `256.0`, and so does a hundred thousand. Not an error. Not a
warning. A plausible number, frozen.

Then the two operations this field cannot avoid. `exp` grows so fast that it runs out of number: above
about `88.7` in `float32` there is no answer, and above **`11.09`** in `float16` there is no answer —
and an attention score of eleven is not unusual, it is Tuesday. When `exp` overflows, one entry of a
probability vector becomes `nan` and the rest become zero, and one step later every weight in the model
is `nan`. `log` fails at the other end, turning a probability that underflowed to zero into `−inf`,
which is worse than a very negative number because it is contagious.

And then today's real lesson, which is the quiet one. A `float16` softmax over a thousand tokens can
set 980 of its probabilities to exactly zero **and still sum to `1.0000000000`**. The check everybody
runs — *do the probabilities add to one?* — cannot see this failure, because the failure is invisible
to it by construction. The model can now never produce those 980 tokens, at any temperature, and the
loss barely moves.

The fix for all of it is one function. `log-sum-exp` has a shift identity that lets you subtract the
largest value before exponentiating and add it back afterwards, exactly — so `exp` never sees a
positive argument and cannot overflow. Written out, the loss becomes `z − lse(z)`: a subtraction, with
no exponential anywhere, returning `−800` where the naive route returns `−inf`.

Eleven parts. Everything runs on the laptop, and — unusually for this curriculum — **every number
today is fixed by the IEEE-754 standard and reproduces bit-for-bit on any machine you will ever use.**

---

## §2 The map

Eleven parts, three sections. Section 1 is MATH-13: what a number is and what each format throws away.
Section 2 is MATH-14: the two operations that break, and the function that fixes them. Section 3
assembles both into the battery you run before a training run. The day climbs
`foundation → working → production`, and each of the first two sections ends with something breaking.

### Section 1 — `01-floating-point`: MATH-13, what a number actually is

From the three fields inside a float to the reason mixed-precision training keeps a `float32` copy of
every weight — and the thousand training steps that changed nothing at all.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [A float is sign, exponent and mantissa](parts/01-floating-point/1.1-sign-exponent-mantissa.md) | What is actually stored, and why is `0.1 + 0.2 != 0.3`? | `foundation` |
| 1.2 | [Range versus precision — fp32, fp16, bf16](parts/01-floating-point/1.2-range-versus-precision.md) | Two 16-bit formats, same width — what does each one buy? | `working` |
| 1.3 | [The gap between representable numbers](parts/01-floating-point/1.3-the-gap-between-representable-numbers.md) | At what magnitude does `x + 1 == x` become true? | `working` |
| 1.4 | [💥 The sum that was wrong by fourteen hundred](parts/01-floating-point/1.4-accumulation-error.md) | Why does a long sum drift — and why does `fp16` stop entirely? | `production` |
| 1.5 | [Mixed precision — what is kept in fp32](parts/01-floating-point/1.5-mixed-precision.md) | Why does 16-bit training need a 32-bit copy of the weights? | `production` |

### Section 2 — `02-stable-softmax`: MATH-14, the two operations that break

Where `exp` overflows to the decimal place, the function that makes the threshold irrelevant, and the
failure that passes every check you would think to run.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [💥 The softmax that returns NaN](parts/02-stable-softmax/2.1-the-softmax-that-returns-nan.md) | At exactly what logit does each dtype's softmax die? | `foundation` |
| 2.2 | [log-sum-exp — the function the trick is named after](parts/02-stable-softmax/2.2-log-sum-exp.md) | What is `lse`, and why is shifting it free? | `working` |
| 2.3 | [`log_softmax` is a subtraction](parts/02-stable-softmax/2.3-log-softmax-is-a-subtraction.md) | Why does every loss function take logits rather than probabilities? | `working` |
| 2.4 | [💥 The softmax that summed to one and was still wrong](parts/02-stable-softmax/2.4-the-softmax-that-returned-all-zeros.md) | How does a distribution lose 98% of its tokens and pass every check? | `production` |
| 2.5 | [log-sum-exp everywhere else](parts/02-stable-softmax/2.5-log-sum-exp-everywhere-else.md) | Where else is this the same function — and how does it stream? | `production` |

### Section 3 — `03-together`: the battery

Both ideas in one script, on one batch, in three dtypes.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [One batch, three dtypes, one stable path](parts/03-together/3.1-one-batch-three-dtypes.md) | Which four numbers and three invariants prove a numerical path is sound? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything uses the numpy pinned on Day 2 and the standard library's
`struct`.

```bash
uv run python -c "import numpy; print('numpy', numpy.__version__)"
./m scaffold 7
```

Two things to hold onto for the whole day.

**First**, this repository sets `filterwarnings = ["error::RuntimeWarning"]` in `pyproject.toml`, from
Day 0. Today that setting is the day's subject rather than a background detail: `exp` overflow, `log(0)`
and `0 × inf` are all `RuntimeWarning`s, so here they stop the run instead of quietly producing `inf`
and `nan`. Every demonstration that needs to *print* an `inf` wraps itself in `np.errstate(...)`.
**Never write that in real code** — it is precisely how a `nan` reaches production unannounced.

**Second**, and it will trip you at least once: numpy promotes narrow scalars to `float64` in ordinary
Python arithmetic. To reproduce a `float16` failure you must force the result back into `float16` after
every operation — `s = np.float16(s + v)`, not `s += v`. Several of today's parts look fussier than
necessary for exactly this reason, and the fussiness is what makes them reproduce.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-007-floating-point-and-logsumexp/lab/floats.py` | [1.1](parts/01-floating-point/1.1-sign-exponent-mantissa.md), [1.2](parts/01-floating-point/1.2-range-versus-precision.md), [1.3](parts/01-floating-point/1.3-the-gap-between-representable-numbers.md) | `unpack_float32`, `to_bf16`, `gap_at`, `format_table` — the three formats side by side |
| `days/day-007-floating-point-and-logsumexp/lab/summation.py` | [1.4](parts/01-floating-point/1.4-accumulation-error.md) | `naive_sum`, `kahan_sum`, `check_sum_is_stable` — and a comparison against `np.sum` |
| `days/day-007-floating-point-and-logsumexp/lab/stable.py` | [2.2](parts/02-stable-softmax/2.2-log-sum-exp.md), [2.3](parts/02-stable-softmax/2.3-log-softmax-is-a-subtraction.md), [2.5](parts/02-stable-softmax/2.5-log-sum-exp-everywhere-else.md) | `logsumexp`, `log_softmax`, `softplus`, `log_sigmoid`, `online_lse` |
| `days/day-007-floating-point-and-logsumexp/lab/battery.py` | [3.1](parts/03-together/3.1-one-batch-three-dtypes.md) | `check_numerics` — four numbers, three invariants, one dict returned |
| `tests/test_numerics.py` | [1.4](parts/01-floating-point/1.4-accumulation-error.md), [2.1](parts/02-stable-softmax/2.1-the-softmax-that-returns-nan.md), [2.4](parts/02-stable-softmax/2.4-the-softmax-that-returned-all-zeros.md), [3.1](parts/03-together/3.1-one-batch-three-dtypes.md) | the overflow test, the accumulation test, the zero-tail test, the three invariants |

```text
TODO(me): compute ln(finfo.max) for float16, float32 and float64 yourself, then find the
          largest attention score your Day 30 configuration could produce for hs = 64 with
          unit-variance q and k. Say whether the 1/sqrt(hs) scaling alone keeps you under
          the fp16 threshold, and show the arithmetic.

TODO(me): implement to_bf16 and verify it against the three properties bf16 must have:
          same max as float32, eps of 2^-7, and exact for every float32 whose low 16
          mantissa bits are already zero. Three assertions, no library needed.

TODO(me): write the accumulation demonstration as a TEST that goes red. Assert that a
          float16 sum of 10,000 copies of 0.1 is NOT within 1% of 1000.0 — then make it
          green by widening the accumulator, and say which line you changed.

TODO(me): take the 980/1000 zeroed-tokens result from part 2.4 and repeat it at V = 32000
          with your own seed. Report the zero count, the row sum, and the true lost mass.
          Then answer in writing: the lost mass is negligible — why does it still matter?

TODO(me): implement online_lse and assert it is BIT-IDENTICAL to the one-pass version on a
          (4096,) vector split into blocks of 512, 1024 and 4096. If any of the three is
          not bit-identical, your rescale is wrong — find it before reading part 2.5 again.

TODO(me): run the part 3.1 battery on a SQUARE batch (B, T, V) = (4, 50, 50) with keepdims
          removed from one logsumexp call. Record which of the three invariants catches it
          and which two do not.
```

---

## §5 The eval that must be able to fail

Five checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_numerics.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| remove the max subtraction from `logsumexp` | `inf` at logits of 1000, then `nan` | the overflow test |
| sum `0.1` ten thousand times in `float16` | `256.0` where `1000.0` was expected | the accumulation test |
| compute `log(softmax(z))` instead of `z - lse(z)` | `-inf` for the third entry of `[0, -400, -800]` | the log-space test |
| run the softmax in `float16` on a peaked distribution | 980/1000 exact zeros, **row sum still `1.0`** | the zero-tail test |
| drop `keepdims=True` on a square batch | plausible numbers, `lse - max` outside `[0, ln V]` | the `lse - max` bound |

The fourth row is the day's centrepiece and it is worth running by hand once, because **the sum-to-one
check passes while it fails**. Print the zero count next to the row sum and watch the two numbers
disagree about whether anything is wrong.

The fifth row is the reason a test batch should never be square: on `(4, 10, 50)` the missing
`keepdims` raises immediately; on `(4, 50, 50)` it broadcasts silently and only the bound catches it.

---

## §6 Compute budget

**Tier: T0.** numpy and `struct` on a laptop CPU, at array sizes from 3 to 1,000,000 elements.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed today |
| Disk | negligible |

The heaviest thing today is a `(1000000,)` array of `float32` — four megabytes — and a Python loop over
a hundred thousand elements, which is slow only by the standards of the vectorized alternative it
exists to be compared against.

What T0 proves: **every result in this day.** The bit layouts, both 16-bit formats, all three `exp`
thresholds, the accumulation stall at `256.0`, the 980 zeroed tokens, the shift identity, the streaming
`lse`'s bit-exact agreement — all of it is IEEE-754 arithmetic or a seeded generator, and **all of it
reproduces identically on any conforming machine.** That is unusual for this curriculum and worth
noticing: today, "measured on this machine" and "true everywhere" coincide.

What T0 does **not** show is the reason anyone accepts these trade-offs: on hardware with 16-bit matmul
units, narrow arithmetic is several times faster than wide. **The correctness argument is complete
here; the speed argument needs a GPU and is Day 66's measurement**, not an assertion made today.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| Comparing computed floats with `==` | `0.1 + 0.2 == 0.3` is `False`; two correct matmuls differ at `1e-14` | [1.1](parts/01-floating-point/1.1-sign-exponent-mantissa.md) |
| Assuming `bf16` is "the precise one" | `bf16` cannot tell `1.0` from `1.005`; its eps is `0.0078` | [1.2](parts/01-floating-point/1.2-range-versus-precision.md) |
| `fp16` on a value above 65504 | `RuntimeWarning: overflow encountered in cast`, then `inf` | [1.2](parts/01-floating-point/1.2-range-versus-precision.md) |
| `fp16` on a value below `6e-08` | **exactly `0.0`, with no warning at all** | [1.2](parts/01-floating-point/1.2-range-versus-precision.md) |
| An absolute tolerance across a range of magnitudes | meaningless at one end or the other; use `rtol` | [1.3](parts/01-floating-point/1.3-the-gap-between-representable-numbers.md) |
| A `float16` counter or accumulator | stops at `2048`; `x + 1 == x` from there on | [1.3](parts/01-floating-point/1.3-the-gap-between-representable-numbers.md) |
| A hand-written summation loop | `9998.557` where `np.sum` gives `10000.001` on the same terms | [1.4](parts/01-floating-point/1.4-accumulation-error.md) |
| A `float16` running total | freezes at `256.0` — the same answer for 10k and 100k terms | [1.4](parts/01-floating-point/1.4-accumulation-error.md) |
| Applying the optimizer update to 16-bit weights | **1000 steps, weight bit-identical, no error** | [1.5](parts/01-floating-point/1.5-mixed-precision.md) |
| Believing mixed precision halves weight memory | it *adds* — `4 + 2` bytes per parameter, not `2` | [1.5](parts/01-floating-point/1.5-mixed-precision.md) |
| `exp` of a raw logit in `fp16` | `inf` above `11.09` — reachable by an ordinary attention score | [2.1](parts/02-stable-softmax/2.1-the-softmax-that-returns-nan.md) |
| One overflowing entry in a softmax row | `[nan, 0, 0, …]` — and only *some* rows of the batch break | [2.1](parts/02-stable-softmax/2.1-the-softmax-that-returns-nan.md) |
| `np.max` without `keepdims=True` | a broadcast error — or, on a square batch, silently wrong numbers | [2.2](parts/02-stable-softmax/2.2-log-sum-exp.md) |
| A fully masked row (`all -inf`) | `-inf − (-inf)` = `nan`, poisoning the row | [2.2](parts/02-stable-softmax/2.2-log-sum-exp.md) |
| `log(softmax(z))` instead of `z - lse(z)` | `-inf` where the fused form gives `-800` | [2.3](parts/02-stable-softmax/2.3-log-softmax-is-a-subtraction.md) |
| A softmax layer *and* `cross_entropy` | the softmax applied twice; loss plateaus far above `ln(V)` | [2.3](parts/02-stable-softmax/2.3-log-softmax-is-a-subtraction.md) |
| Trusting "the probabilities sum to 1" | `1.0000000000` with **980 of 1000 entries exactly zero** | [2.4](parts/02-stable-softmax/2.4-the-softmax-that-returned-all-zeros.md) |
| Casting to `fp32` *after* the softmax | too late — the zeros are already there | [2.4](parts/02-stable-softmax/2.4-the-softmax-that-returned-all-zeros.md) |
| `log(1 + exp(x))` written literally | `inf` at `x = 800`, where the answer is `800.0` | [2.5](parts/02-stable-softmax/2.5-log-sum-exp-everywhere-else.md) |
| Ranking beams in probability space | all `0.0` after ~800 nats; `argmax` returns index `0` forever | [2.5](parts/02-stable-softmax/2.5-log-sum-exp-everywhere-else.md) |
| A square test batch | hides every missing-`keepdims` bug in the file | [3.1](parts/03-together/3.1-one-batch-three-dtypes.md) |
| Logging only the loss | the magnitude that predicted the `nan` was never recorded | [3.1](parts/03-together/3.1-one-batch-three-dtypes.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement**, in its numerical form. Today's
centrepiece, part [2.4](parts/02-stable-softmax/2.4-the-softmax-that-returned-all-zeros.md), measures a
`float16` softmax zeroing **980 of 1000 tokens while the row still sums to `1.0000000000`** — and the
lost probability mass is `5.15e-07`, far too small to move any aggregate metric. So the loss, the
perplexity and the accuracy are all *unchanged*, the sanity check passes, and the model has
nevertheless been made incapable of producing 98% of its vocabulary. **A metric that cannot move is not
evidence that nothing changed.** The detection is not the sum: it is counting the exact zeros, and
better still not leaving log space at all.

**Silent Failure #3 also appears in a new disguise.** Day 6 showed a mean that counted padding; part
[1.4](parts/01-floating-point/1.4-accumulation-error.md) shows a mean that stopped counting altogether
— a `float16` accumulator frozen at `256.0`, reporting a converged-looking number forever. Both are
"the reduction was not what you thought it was", and both are caught by printing the count alongside
the value.

---

## §8 Verify before you code

Everything today is numpy 2.5.2 (pinned Day 2) and the standard library. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| `numpy` doc `reference/generated/numpy.finfo.html` | `bits`, `eps`, `max`, `tiny`, `precision` for `float16`/`float32`/`float64` — the whole of part 1.2's table |
| `numpy` doc `reference/generated/numpy.spacing.html` | that it returns the distance to the next representable value away from zero — part 1.3 |
| `numpy` doc `reference/generated/numpy.nextafter.html` | that the second argument supplies direction only, and `nextafter(0, 1)` is the smallest subnormal |
| `numpy` doc `reference/generated/numpy.ndarray.view.html` | reinterpreting `float32` bits as `uint32` without conversion — part 1.2's `to_bf16` |
| `numpy` doc `reference/generated/numpy.sum.html` | the `dtype=` accumulator argument, and that the default accumulates in the input dtype |
| `numpy` doc `reference/generated/numpy.take_along_axis.html` | rank-matching requirements for the gather in parts 2.3 and 3.1 |
| `numpy` doc `reference/generated/numpy.log1p.html` | accurate `log(1 + x)` for tiny `x` — the softplus idiom in part 2.5 |
| `numpy` doc `reference/generated/numpy.errstate.html` | which of `over`/`under`/`divide`/`invalid` each demonstration must suppress |
| Python doc `library/struct.html#format-characters` | `>f` as big-endian `float32`, for part 1.1's bit unpacking |
| **arXiv:2205.14135** — *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* | abstract opened at `https://arxiv.org/abs/2205.14135` on **2026-08-26**; confirmed the claim of an "IO-aware **exact** attention algorithm that uses tiling", which is the streaming `lse` of part 2.5 |
| Day 2 part 1.2's own output | `float32` eps `1.1920928955078125e-07`, `float32 tiny 1.1754944e-38` — carried forward, not re-derived |
| Day 5 part 1.3's own output | the stable softmax and the proof that the max subtraction is exact; today supplies the threshold, not the fix |
| Day 6 part 2.3's own output | `log(softmax(z))` returning `-inf` at logits spanning 800; part 2.3 is the mechanism behind it |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.12, numpy 2.5.2**,
seed **1337** where randomness is involved, on **2026-08-26**. No figure was recalled and none came
from another machine.

> **A note on the CPython version.** Days 2–6 record `CPython 3.12.10`; this day records `3.12.12`,
> which is what `uv run python -V` reports in this environment today. Nothing in either day depends on
> the patch version — every figure here is IEEE-754 arithmetic or numpy — but the ledger records what
> was actually run rather than what the earlier days said, per Principle 8.

---

## §9 Say it in an interview

"The thing that changed how I debug training runs was realising that `float16` has a five-bit exponent,
which means `exp` overflows above `ln(65504)` — about eleven. An unscaled attention score clears eleven
easily, so a softmax in `fp16` doesn't degrade, it returns `nan`, and one step later every weight is
`nan`. That's the loud failure and it's the easy one. The one I actually watch for now is the quiet
version: I measured a `fp16` softmax over a thousand tokens setting 980 of them to exactly zero while
the row still summed to `1.0000000000` — so the standard sanity check passes, the loss barely moves
because the lost mass was five parts in ten million, and the model can now never produce 98% of its
vocabulary at any temperature. You can't detect that by summing; you have to count the exact zeros, or
better, stay in log space until the sampler, because `z − lse(z)` keeps all thousand of them finite in
the same dtype. The same reasoning is why mixed precision keeps `fp32` master weights — I ran a
thousand optimizer steps on a `fp16` weight with an ordinary gradient and an ordinary learning rate and
the weight came out bit-identical, because the update was `1e-05` and the `fp16` gap at `1.0` is
`0.000977`. So now the first thing I add to a run is `max|logits|` in the log line next to the loss,
because that's the number that was drifting upward before the `nan` arrived."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 7` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 7 | 2026-08-26 | MATH-13, MATH-14 | 11 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; numpy was pinned on Day 2.

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The `(4, 10, 50)` batch in part 3.1 comes from a seeded generator, and the
thousand-step loop in part 1.5 is a single scalar being updated — a demonstration of an optimizer step,
not a run.

Commit:

```text
day 007: Numerical reality — floating point and log-sum-exp — closes MATH-13, MATH-14
```
