---
day: 6
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Entropy, cross-entropy and perplexity"
ids: ["MATH-10", "MATH-11", "MATH-12"]
principles: [1, 2, 3, 8, 10, 11, 16, 17, 18, 20]
kind: math
plan_version: "v1.3.0"
parts: 12
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 6 — Entropy, cross-entropy and perplexity: why the loss is the loss

> **Yesterday (Day 5):** what a model actually outputs — logits, the softmax that turns them into a
> distribution, temperature, and the machinery for drawing a token — with six measured ways each of
> those goes silently wrong.
> **Today:** the number the whole curriculum optimises. What surprise is, what a distribution's average
> surprise is, what it costs to believe the wrong thing, and why *that* quantity and not another one is
> the loss — plus the padding failure that makes it go down while the model gets worse.
> **Tomorrow (Day 7):** 💥 numerical reality — fp32, fp16 and bf16, the softmax that returns `NaN`, and
> the log-sum-exp trick this day kept pointing at (MATH-13, MATH-14).

---

## §1 Where we are

Everything so far has been machinery. Today is the number.

Start from a question with no mathematics in it: what does it mean for a message to be *informative*?
Three requirements settle it. Being told what you already knew tells you nothing. Something unlikely
tells you more than something likely. And two unrelated pieces of news, together, should be worth the
sum of what each is worth separately — not some other combination. That third requirement is the one
that does all the work, because there is exactly one function that turns multiplication into addition,
and once you insist on it the definition of information is forced.

From there everything follows almost mechanically. The average surprise of a distribution is its
*entropy*, and it runs from zero for a certainty up to a ceiling set by how many outcomes there are.
The average surprise you *actually experience* when the world does one thing and you expected another
is *cross-entropy* — and it can never be below the entropy, with the gap being exactly how wrong you
were. That gap has a name too.

And then the sentence this day exists for: minimising cross-entropy is the same operation as making
the observed data as likely as possible under your model. Not similar to it, not a good proxy for it —
the same thing, with a logarithm applied so a computer can hold the numbers. Every loss in this
curriculum, from Day 25's first tiny model to Day 161's finished system, is that.

Which raises the question everybody eventually asks and few can answer: **how low should the loss go?**
Not to zero. The identity says the loss splits into the data's own irreducible uncertainty plus your
model's error, and only the second half can be reduced. A curve flattening near that floor is a model
that has learned what there was to learn; a curve flattening far above it has not; and telling those
two apart requires knowing the floor exists.

Then the failures, and today's are the worst kind so far because they make the number *improve*. A
third of every batch is padding, and `<pad>` following `<pad>` is the easiest prediction in the whole
problem — so a model that learns it reports a falling loss while its real loss rises. Measured today:
`4.5970` on the dashboard, `6.2059` on the tokens anybody cares about, moving in opposite directions.
That is the plan's Silent Failure #3, and it is joined by a second: the same text under a finer
tokenizer gives a perplexity 42 times lower, with no change to the model at all.

Twelve parts. Everything on the laptop, and every one of today's failures reproduces in milliseconds
because they are properties of arithmetic rather than of hardware.

---

## §2 The map

Twelve parts, three sections — one per curriculum ID. Section 1 defines the unit of surprise, section 2
turns it into the loss, and section 3 is the family of numbers you actually report. The day climbs
`foundation → working → production` and every section ends with something breaking.

### Section 1 — `01-entropy`: MATH-10, the unit of surprise

From "what makes a message informative" to a number with a floor and a ceiling — and the term in the
formula that is zero in mathematics and `nan` in arithmetic.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [Surprise, measured](parts/01-entropy/1.1-surprise-measured.md) | Why is information `−log(p)` and not something simpler? | `foundation` |
| 1.2 | [Entropy in bits and nats](parts/01-entropy/1.2-entropy-in-bits-and-nats.md) | How uncertain is a distribution, on a scale with both ends known? | `working` |
| 1.3 | [💥 The zero-probability event and log(0)](parts/01-entropy/1.3-the-zero-probability-event.md) | Why are the two popular fixes for `log(0)` both wrong? | `production` |

### Section 2 — `02-cross-entropy`: MATH-11, why the loss is the loss

The cost of believing the wrong thing, its collapse to a single lookup, the argument that it is the
*only* sensible loss — and the reduction choice that hides Silent Failure #3.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Coding with the wrong distribution](parts/02-cross-entropy/2.1-coding-with-the-wrong-distribution.md) | What does it cost to hold beliefs that do not match the world? | `foundation` |
| 2.2 | [NLL is cross-entropy with a one-hot](parts/02-cross-entropy/2.2-nll-is-cross-entropy-with-a-one-hot.md) | Why does the implementation look nothing like the formula? | `working` |
| 2.3 | [Why this is the loss](parts/02-cross-entropy/2.3-why-this-is-the-loss.md) | Why this quantity, and why computed from logits? | `working` |
| 2.4 | [The mean over what?](parts/02-cross-entropy/2.4-the-mean-over-what.md) | Three ways to turn `(B, T)` into a scalar — which, and why does it matter? | `production` |
| 2.5 | [💥 The loss that counted padding](parts/02-cross-entropy/2.5-the-loss-that-counted-padding.md) | How does the reported loss fall while the real loss rises? | `production` |

### Section 3 — `03-kl-and-perplexity`: MATH-12, the same quantity wearing three hats

The gap between cross-entropy and its floor, the exponential that makes it readable, the trap that
makes it incomparable, and the identity that checks all four at once.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [KL divergence — the extra bits](parts/03-kl-and-perplexity/3.1-kl-the-extra-bits.md) | How low can a loss curve go, and why not to zero? | `foundation` |
| 3.2 | [Perplexity](parts/03-kl-and-perplexity/3.2-perplexity.md) | What does "perplexity 20" actually mean? | `working` |
| 3.3 | [💥 The perplexity that improved](parts/03-kl-and-perplexity/3.3-the-perplexity-that-improved.md) | How does a metric improve 42× with no change to the model? | `production` |
| 3.4 | [One batch, four numbers, one identity](parts/03-kl-and-perplexity/3.4-one-batch-four-numbers.md) | Which single check catches a unit error, an argument swap and a reduction mismatch? | `production` |

---

## §3 Setup — run this

**No new packages today.** Everything uses the numpy pinned on Day 2.

```bash
uv run python -c "import numpy; print('numpy', numpy.__version__)"
./m scaffold 6
```

One thing to have in mind throughout: this repository sets
`filterwarnings = ["error::RuntimeWarning"]` in `pyproject.toml`, from Day 0. Today that setting earns
its keep — `log(0)`, `0 × inf` and `exp` overflow are all `RuntimeWarning`s, so they stop the run
instead of quietly producing `nan`. The demonstrations that need to *print* a `nan` wrap themselves in
`np.errstate(...)`; **never write that in real code.**

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `days/day-006-entropy-cross-entropy-perplexity/lab/information.py` | [1.2](parts/01-entropy/1.2-entropy-in-bits-and-nats.md), [2.1](parts/02-cross-entropy/2.1-coding-with-the-wrong-distribution.md), [3.1](parts/03-kl-and-perplexity/3.1-kl-the-extra-bits.md) | `entropy_nats`, `entropy_bits`, `cross_entropy`, `kl_divergence` — all masked, all with the unit in the name |
| `days/day-006-entropy-cross-entropy-perplexity/lab/loss.py` | [2.2](parts/02-cross-entropy/2.2-nll-is-cross-entropy-with-a-one-hot.md), [2.3](parts/02-cross-entropy/2.3-why-this-is-the-loss.md), [2.4](parts/02-cross-entropy/2.4-the-mean-over-what.md) | `log_softmax`, `nll_from_logits`, `reduce_loss(nll, mask, how=...)` |
| `days/day-006-entropy-cross-entropy-perplexity/lab/report.py` | [3.2](parts/03-kl-and-perplexity/3.2-perplexity.md), [3.4](parts/03-kl-and-perplexity/3.4-one-batch-four-numbers.md) | `report_step_zero` — token count, loss, perplexity, `ln(V)` ratio, and the two warnings |
| `tests/test_information.py` | [1.3](parts/01-entropy/1.3-the-zero-probability-event.md), [2.5](parts/02-cross-entropy/2.5-the-loss-that-counted-padding.md), [3.4](parts/03-kl-and-perplexity/3.4-one-batch-four-numbers.md) | the identity test, the padding test, the `log(0)` test, the unit test |

```text
TODO(me): measure the entropy of a real text file you have on disk — a character-level
          histogram is enough. Report it in bits per character AND bits per byte, and say
          why the two differ for a file containing any non-ASCII text. Day 10 is the
          mechanism; this is the number.

TODO(me): implement cross-entropy THREE ways — from two probability distributions, from
          logits and a one-hot, and from logits and integer targets — and assert all three
          agree to 1e-12 on a case where all three are computable. Then time them and say
          which you would ship.

TODO(me): write the padding demonstration from part 2.5 as a TEST that goes red. Construct
          a model that is good at <pad> and assert that the masked loss is HIGHER than the
          unmasked one. Watch it fail if you remove the mask.

TODO(me): work out on paper what your step-0 loss should be for V = 256 (Day 10's
          byte-level vocabulary) and for V = 32000. Two numbers, in nats, and the
          perplexity of each. You will check against these on Day 25.

TODO(me): take part 3.3's three tokenizations and compute what a 10% real improvement in
          model quality would look like in each — in perplexity and in bits per byte. Say
          which of the two you would put in a results table and why.
```

---

## §5 The eval that must be able to fail

Four checks, and **every one must be observed red before it is green** (Principle 11).

```bash
uv run python -m pytest tests/test_information.py -q
```

| Break this | Expect | Which check catches it |
| --- | --- | --- |
| remove the `np.where` mask from `entropy` | `nan` on any distribution containing a zero | the `log(0)` test |
| use `np.log2` in one of the three identity terms | `H(p) + KL ≠ H(p, q)`, off by `1.4427` | the identity test |
| swap the KL arguments | a **different** finite number; sometimes negative | the identity test + the non-negativity assertion |
| drop the mask from the loss | reported loss falls while masked loss rises | the padding test |
| `exp` a bits figure | perplexity `36.85` where it should be `12.18` | the unit test |

The fourth row is the day's centrepiece and it is worth doing by hand once: build the model that is
good at `<pad>`, print the two losses side by side, and watch them move in opposite directions as you
raise the `<pad>` logit. **A loss that falls is not evidence of anything** until you know what it was
averaged over.

The second and third rows are both caught by **one** check — the identity `H(p) + KL = H(p, q)` — which
is why part [3.4](parts/03-kl-and-perplexity/3.4-one-batch-four-numbers.md) exists as its own document.

---

## §6 Compute budget

**Tier: T0.** numpy on a laptop CPU, at vocabularies of 4, 50 and 256.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0.** Nothing today can use a GPU or needs one. |
| Free notebook sessions | 0 |
| Network | none — no packages installed today |
| Disk | negligible |

The heaviest thing today is a `(4, 10, 50)` batch. Everything else is arrays of four to 256 elements.

What T0 proves: **every result in this day.** The definition of information, both entropy bounds, the
`H(p) + KL = H(p, q)` identity, `exp(ln(k)) = k`, the `nan` from `0 × log(0)`, the `−inf` from
`log(softmax(z))` at scale 800, the padding divergence and the 42× perplexity spread are all
mathematics or IEEE-754 arithmetic. **They reproduce identically on any hardware**, which is unusual
for this curriculum and worth noticing. What T0 does not show is estimating `H(p)` for a real corpus,
which is Day 68's genuinely hard problem.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| `np.log` mistaken for base 10 | every information number wrong by `2.3026` | [1.1](parts/01-entropy/1.1-surprise-measured.md) |
| A loss reported without its unit | bits and nats differ by `1.4427` — enough to look like a real gain | [1.1](parts/01-entropy/1.1-surprise-measured.md) |
| Multiplying probabilities over a sequence | underflows to exactly `0.0` at ~700 tokens in `float64` | [1.1](parts/01-entropy/1.1-surprise-measured.md), [2.3](parts/02-cross-entropy/2.3-why-this-is-the-loss.md) |
| `-(p * np.log2(p)).sum()` on any distribution with a zero | `nan`, from `0 × −inf` | [1.3](parts/01-entropy/1.3-the-zero-probability-event.md) |
| `log(p + 1e-10)` as the fix | biases **every** term; measured `0.9999999997` where the answer is `1.0` | [1.3](parts/01-entropy/1.3-the-zero-probability-event.md) |
| `np.clip(p, 1e-10, 1)` as the fix | **9% wrong** on a distribution containing no zeros at all | [1.3](parts/01-entropy/1.3-the-zero-probability-event.md) |
| Swapping the cross-entropy arguments | `2.000000` becomes `2.264723` — finite, plausible, a different objective | [2.1](parts/02-cross-entropy/2.1-coding-with-the-wrong-distribution.md) |
| A model that assigns exactly zero to something that happens | cross-entropy `inf`, then `nan` one step later | [2.1](parts/02-cross-entropy/2.1-coding-with-the-wrong-distribution.md) |
| Building a one-hot target tensor | `(B, T, V)` where `(B, T)` was needed — **16,000×** the memory | [2.2](parts/02-cross-entropy/2.2-nll-is-cross-entropy-with-a-one-hot.md) |
| Targets not shifted by one | the model learns to copy; loss collapses towards zero and looks superb | [2.2](parts/02-cross-entropy/2.2-nll-is-cross-entropy-with-a-one-hot.md) |
| `log(softmax(z))` instead of `log_softmax(z)` | `−inf` at logits spanning 800, where the fused form gives `−800` | [2.3](parts/02-cross-entropy/2.3-why-this-is-the-loss.md) |
| Changing `sum` to `mean` in a refactor | every gradient scaled by `1/27` — a stealth learning-rate change | [2.4](parts/02-cross-entropy/2.4-the-mean-over-what.md) |
| Comparing losses computed with different reductions | `5.366416` vs `5.413519` on **one batch** | [2.4](parts/02-cross-entropy/2.4-the-mean-over-what.md) |
| `nll.mean()` without the mask | reported `4.5970` while real is `6.2059` — **opposite directions** | [2.5](parts/02-cross-entropy/2.5-the-loss-that-counted-padding.md) |
| Comparing perplexity across tokenizers | `148.413` vs `3.490` for identical models — a factor of 42 | [3.3](parts/03-kl-and-perplexity/3.3-the-perplexity-that-improved.md) |
| `exp` applied to a bits figure | `36.85` instead of `12.18`, and both look like perplexities | [3.2](parts/03-kl-and-perplexity/3.2-perplexity.md) |
| Logging only the loss | one number, nothing to compare it to, and three of today's bugs invisible | [3.4](parts/03-kl-and-perplexity/3.4-one-batch-four-numbers.md) |

**Named silent failure (plan §6): #3 — the loss counted padding or the prompt.** This is the day it is
built. Part [2.5](parts/02-cross-entropy/2.5-the-loss-that-counted-padding.md) measures the reported
loss falling from `5.3434` to `4.5970` — a 14% improvement — while the real loss over the same model
rises from `5.3664` to `6.2059`. **The two curves point in opposite directions and only one is on the
dashboard.** The plan's §6 gives the detection by name — *print the label tensor for one batch and count
the `-100`s by hand* — and part 2.5 turns it into an assertion. Day 88's instruction tuning is the same
mechanism on a much larger fraction of the tokens, and part
[3.3](parts/03-kl-and-perplexity/3.3-the-perplexity-that-improved.md) shows the contamination reaching
perplexity, where the exponential amplifies a 14% loss difference into a fivefold metric difference.

**Silent Failure #4 also appears**, through part
[3.3](parts/03-kl-and-perplexity/3.3-the-perplexity-that-improved.md)'s tokenizer trap: a metric that
moves by a factor of 42 for reasons unrelated to model quality makes any improvement below that
magnitude uninterpretable. The fix is a tokenizer-independent unit — bits per byte — and it is one
division.

---

## §8 Verify before you code

Everything today is numpy 2.5.2 (pinned Day 2) and the standard library. Checked and run on
`2026-08-26`:

| Source | Checked for |
| --- | --- |
| `numpy` doc `reference/generated/numpy.log.html`, `numpy.log2.html` | that `np.log` is base **e** and `np.log2` is base 2 — the unit trap in part 1.1 |
| `numpy` doc `reference/generated/numpy.where.html` | elementwise selection, used for the zero-masking pattern throughout |
| `numpy` doc `reference/generated/numpy.take_along_axis.html` | the gather that collapses cross-entropy to one lookup — part 2.2 |
| `numpy` doc `reference/generated/numpy.finfo.html` | `float64` `tiny = 2.2250738585072014e-308` and `max`, for the underflow and overflow arguments |
| `numpy` doc `reference/generated/numpy.isclose.html` | `rtol`/`atol` semantics, used for the identity check in part 3.4 |
| `python` doc `library/math.html#math.log` | that `math.log(0.0)` raises `ValueError` where numpy returns `-inf` — the asymmetry in part 1.3 |
| Day 2 part 1.2's own output | `float32` eps `1.1920928955078125e-07`, `float64` eps `2.220446049250313e-16`, `float32 tiny 1.1754944e-38` |
| Day 5 part 1.3's own output | `exp(-800) = 0.0`, the numerical zero that part 1.3 distinguishes from a structural one |

Every empirical number in this day was produced by running the code in the part that quotes it, on
**Intel Core i3-1115G4 (2 cores / 4 threads), 11.7 GB RAM, Windows 11, CPython 3.12.10, numpy 2.5.2**,
seed **1337** where randomness is involved, on **2026-08-26**. No figure was recalled and none came from
another machine.

---

## §9 Say it in an interview

"The thing that reframed training for me was realising cross-entropy isn't a design choice — it *is*
maximum likelihood, with a log applied because the product of a thousand probabilities underflows to
zero. I checked that: a four-token sequence already has a likelihood of `4e-07`, and at seven hundred
tokens it's exactly zero in float64 while the sum of logs is a perfectly ordinary number. That's also
why the loss takes logits rather than probabilities — `log(softmax(z))` is a subtraction that can't
underflow, and I measured the naive route returning `-inf` on logits spanning 800 where the fused one
returns `-800`. But the thing I'd actually bring up is the padding failure. A third of a real batch is
padding, and `<pad>` after `<pad>` is the easiest prediction in the problem — so if you average over
the padded positions, the reported loss *falls* as the model learns that trick while the real loss on
actual tokens *rises*. I measured `4.60` on the dashboard against `6.21` on the tokens anyone cares
about, moving in opposite directions. Now I log the counted-token count at step zero alongside the
loss and `ln(V)`, because an untrained model should start at `ln(V)` and anything much below that means
you're leaking the answer."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 6` will refuse while any box is unticked, an artifact is staged, or the gate is red. Defined
by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 6 | 2026-08-26 | MATH-10, MATH-11, MATH-12 | 12 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — **no rows today.** Nothing was installed; numpy was pinned on Day 2.

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded and
nothing was trained. The `(4, 10, 50)` batches in this day are constructed from a seeded generator, not
from a corpus, and the padding demonstration is a simulation rather than a run.

Commit:

```text
day 006: Entropy, cross-entropy and perplexity — closes MATH-10, MATH-11, MATH-12
```
