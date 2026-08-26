# Day 2 — CHECKLIST

**IDs closed:** MATH-01, MATH-02, MATH-03
**Principles served:** 1, 2, 3, 6, 7, 8, 10, 11, 15, 16, 17, 18, 20
**Parts:** 13 across 4 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 2` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 3 days complete, then one commit reading
`day 002: Tensors — shape, stride, dtype, device — closes MATH-01, MATH-02, MATH-03`.

---

## Setup

- [ ] Day 1's checklist is fully ticked and `./m done 1` committed
- [ ] numpy's version looked up **live** with the `curl` in §3, and you can say what it printed
- [ ] `uv add numpy==<observed>` run with an exact `==` pin, and `uv.lock` updated
- [ ] `uv run python -c "import numpy; print(numpy.__version__)"` prints the version you pinned
- [ ] The `docs/PACKAGES.md` row is written with **your** version and **your** date
- [ ] `./m scaffold 2` run; `days/day-002-tensors-shape-stride/lab/` exists

## MATH-01 — what a tensor is (section 1)

- [ ] Read 1.1; wrote `FlatTensor` and `strides_for` **before** importing numpy (Principle 3)
- [ ] Ran 1.1's check-yourself; the last two numbers **agree**, and you know why the first two changed
      when you switched dtype
- [ ] Can answer out loud: why does a transpose not have to move any numbers, and what would have to
      be true for it to become expensive?
- [ ] Read 1.2; ran its check-yourself and **watched a count go negative** with no exception
- [ ] Can name the two independent things a dtype fixes, and give one failure caused by each — one
      that raises and one that does not
- [ ] Saw `int32 + float32` produce `float64` and can say why that line matters in a training loop
- [ ] Read 1.3; ran its check-yourself and **wrote down both ratios with your own hardware line**
- [ ] Your two ratios point in **opposite directions**, and you can explain the one that contradicts
      the naive rule
- [ ] Ran `np.shares_memory(A, A.T.reshape(-1))` and saw `False` — you can say what that `False` cost
- [ ] Read 1.4; ran its check-yourself and saw the `to_device("cuda")` refusal text
- [ ] Wrote down the byte count for a `(32000, 768)` fp32 table — Day 66 needs it
- [ ] Can answer out loud: name the failure that produces a completely correct loss curve at a
      fraction of the expected speed
- [ ] Read 1.5; ran its check-yourself **both ways** and watched the caller's mean become `0.0`
- [ ] Can say why the in-place form — the bug here — is the *correct* choice inside an optimizer step

## MATH-02 — broadcasting and indexing (section 2)

- [ ] Read 2.1; **predicted** all three `broadcast_shapes` results before running them
- [ ] Ran the pairwise line and saw the MiB figure your machine produced
- [ ] Can state the three-line rule with the words **right-aligned** in it
- [ ] Can say why `(5,)` combined with `(5, 1)` gives twenty-five numbers rather than five
- [ ] Reproduced the square-matrix `keepdims` failure and saw rows that do **not** sum to 1
- [ ] Read 2.2; ran its check-yourself — first boolean `True`, second `False`
- [ ] Can state the one property of a selection that decides view versus copy
- [ ] Can explain why `z[[0, 2]] = -1` changes `z` even though `z[[0, 2]]` is a copy
- [ ] Predicted `emb[ids].shape` before running it, and can state the gather shape rule in words
- [ ] Read 2.3; **predicted the shape wrong or right, and wrote down which**
- [ ] Ran its check-yourself and saw the factor of 95
- [ ] Added the `reshape(pred.shape)` assertion, watched it pass, then **broke it on purpose** and
      watched it raise
- [ ] Can say why this bug hides at the start of training and appears only once the model is good

## MATH-03 — matrix multiplication (section 3)

- [ ] Read 3.1; wrote the triple loop **before** using `@` (Principle 3)
- [ ] Ran 3.1's check-yourself; predicted all three shapes first, including the rank-0 one
- [ ] Broke the shapes on purpose and can say which operand and which axis the error names
- [ ] Can state the shape rule for `@` in one sentence using the words *inner* and *outer*
- [ ] Can give the flop count of `(B, T, C) @ (C, V)` without looking
- [ ] Read 3.2; ran its check-yourself and **wrote your speedup down with your hardware line**
- [ ] `allclose` printed `True` and `array_equal` printed `False`, and you can say why
- [ ] Can name the four things the library's matmul does that your loop does not
- [ ] Read 3.3; predicted all four shapes in its check-yourself before running
- [ ] Can say why `(1, 4, 5) @ (8, 5, 3)` producing `(8, 4, 3)` is dangerous rather than convenient
- [ ] Read 3.4; ran its check-yourself and **recorded your machine's two ceilings** (GB/s and GFLOP/s)
- [ ] Your achieved ratio is **smaller** than your intensity ratio, and you can say why
- [ ] Re-ran it in `float32` and can say which rate improved more, and roughly by how much
- [ ] Can define arithmetic intensity in one sentence and explain why single-token decoding is slow

## Synthesis (section 4)

- [ ] Read 4.1; ran its check-yourself and saw **two `True`s** where you wanted a failure
- [ ] Changed `T` from 8 to 5, re-ran, and can name which of the four lines **still** does not raise
- [ ] Wrote the `test_linear_bias_is_per_channel` test, watched it pass, then substituted the broken
      bias and **watched it go red**
- [ ] Can name the one condition that turns both of today's rules from safe into dangerous
- [ ] Can name the kind of check that still works when a shape assertion does not

## Build brief

- [ ] `lab/flat_tensor.py` written; `FlatTensor.transpose()` added and the aliasing demonstrated
- [ ] `FlatTensor.contiguous()` written; timed against `np.ascontiguousarray` and **both numbers
      recorded with your hardware line**
- [ ] `lab/naive_matmul.py` written, with its timing harness
- [ ] `assert_shape(x, expected, name)` written, and its message prints **both** shapes and the name
- [ ] The arithmetic-intensity arithmetic for `(1, C) @ (C, V)` and `(B*T, C) @ (C, V)` done **on
      paper**, both numbers written down
- [ ] `lab/shapes.md` written — every `## Shapes` row you had to think about, in your own words

## The evals that must be able to fail

- [ ] Check 1 (hand offset vs numpy strides) run and **green**
- [ ] Check 1 broken on purpose — divided by `itemsize` in the wrong place — and **watched it go red**
- [ ] Check 2 (triple loop vs `@`) run: `allclose` `True`, `array_equal` `False`
- [ ] Check 2 broken on purpose — demanded exact equality — and **watched it go red**
- [ ] Check 3 (the `@` versus `*` trap) run and printed `True` then `False`
- [ ] `./m depth 2` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 6, 7, 8)

- [ ] Every number you wrote down today is either **measured on your machine** — with the hardware
      line, the seed and the date next to it — or **cited**. None was recalled.
- [ ] You did **not** copy this day's `GFLOP/s`, `GB/s` or `×` figures into your own notes as if they
      were yours. They are the reference machine's.
- [ ] Your `docs/PACKAGES.md` row records the version `uv` actually installed, not the one this
      document names

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say what today's CPU measurements prove, and what they prove nothing about

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` row pasted from §11, with your observed version
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**, and you can say why
      a microbenchmark is not a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-01..03 closed on day 2
- [ ] `./m done 2` committed with the message from §11
