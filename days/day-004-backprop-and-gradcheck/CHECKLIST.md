# Day 4 — CHECKLIST

**IDs closed:** MATH-06, MATH-07
**Principles served:** 1, 2, 3, 8, 10, 11, 16, 17, 18, 20
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 4` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green` — including, for the first time, a real test file — a status line showing 5
days complete, then one commit reading
`day 004: Backprop through a layer and gradient checking — closes MATH-06, MATH-07`.

---

## Setup

- [ ] Day 3's checklist is fully ticked and `./m done 3` committed
- [ ] `./m scaffold 4` run; the lab directory exists
- [ ] `tests/` exists and `uv run python -m pytest --version` prints a version
- [ ] **No packages installed today** — confirmed, and you can say why

## MATH-06 — the linear layer (section 1)

- [ ] Read 1.1; ran its check-yourself — shape `(4, 3)`, parameters `18`, boolean `True`
- [ ] Predicted the shape and the parameter count **before** running
- [ ] Can state the shape rule for `Y = X @ W + b` naming every axis
- [ ] Can say how many routes a single weight `W[k, j]` has to the loss, and why that number is `B`
- [ ] Can demonstrate — not just assert — that two linear layers with no nonlinearity are one layer
- [ ] Read 1.2; derived all three gradients from the index formula **before** reading the matrix form
- [ ] Ran 1.2's check-yourself; all three relative errors below `1e-8`
- [ ] Deleted the `A[i] = old` restore line, predicted the effect, and confirmed it
- [ ] Can name, for each gradient, the axis that is summed over and why
- [ ] Can state the invariant every gradient's shape must satisfy
- [ ] Can say which of the three gradients needs `X`, which needs `W`, and what that implies for memory
- [ ] Read 1.3; ran its check-yourself and **predicted all six results before looking**
- [ ] Exactly three raised; `dY.T @ X` gave `(3, 5)` and you can say what it computes
- [ ] Re-ran with `B = C = C_out = 4` and watched **all six** succeed
- [ ] Can state the rule for finding the contracted axis in one sentence
- [ ] Read 1.4; ran its check-yourself — `(4,)`, `(3, 4)`, `(3, 4)`, and one error below `1e-8`
- [ ] **Understood the third line**: a `(4,)` bias minus a `(3, 4)` gradient gives a `(3, 4)` bias
- [ ] Wrote `unbroadcast` and confirmed it reproduces the axis list without your typing one
- [ ] Can state the rule for backpropagating through a broadcast in one sentence
- [ ] Read 1.5; ran its check-yourself — cosine `0.0868`, and **both** runs decreased
- [ ] Re-ran with distinct shapes and watched the wrong version raise
- [ ] Can explain why a gradient 85° from the truth still reduces the loss
- [ ] Can name the two defences, and say which one costs nothing

## MATH-07 — gradient checking (section 2)

- [ ] Read 2.1; wrote `numerical_gradient` and ran its check-yourself — three errors below `1e-8`
- [ ] Ran the disconnected-loss case and got **exactly `0.0`**
- [ ] Can say what makes a numerical gradient worth using as a check
- [ ] Can say why it is useless as a way of training
- [ ] Read 2.2; ran its check-yourself — two absolute errors five orders apart, two relative errors not
- [ ] Ran the same check in `float32` and recorded what the relative error became
- [ ] **Swept `h` on your machine, in both dtypes**, and wrote down the best value for each
- [ ] Can say why the denominator is `|a| + |n|` and not `|a|`
- [ ] Can give a defensible threshold for `float64` and for `float32`, with the reason for each
- [ ] Read 2.3; wrote `tests/test_linear.py` with the three parametrised cases
- [ ] First run is `3 passed`
- [ ] **Broke `dW` on purpose and watched `[dW]` fail while the other two passed**
- [ ] Ran the broken version at **both** distinct and square shapes, and saw the two different messages
- [ ] Put it back and confirmed `3 passed`
- [ ] Can name the four properties this repository requires of a test and how a gradient check meets each
- [ ] Can say why the fixture uses 2, 3 and 5
- [ ] Read 2.4; ran its check-yourself — a pass at `8.135e-11` on a **bias-free** layer
- [ ] The all-ones case printed **exactly `0.0`**
- [ ] Wrote `test_forward_matches_hand_arithmetic` and confirmed it **fails** on the bias-free forward
- [ ] Can state exactly what a passing gradient check proves, using the word *consistent*
- [ ] Can name the two complementary checks that cover what it does not
- [ ] Read 2.5; ran its check-yourself — `judged 1` at `w = 1.0`, `judged 0` at `w = 25.0`
- [ ] Saw the relative error of **`0.000e+00`** awarded to an all-zeros gradient
- [ ] Added the `judged` guard and **watched the same case turn red**
- [ ] Can explain how a check awards a perfect score to a backward pass that computes nothing
- [ ] Can name the single assertion that turns that pass into a failure

## Together (section 3)

- [ ] Read 3.1; ran its check-yourself — three errors, one value test, one loss decrease
- [ ] Applied **all five** breakages, one at a time, and wrote down which check caught each
- [ ] No breakage passed all four; if one did, you noted the gap in your lab
- [ ] Can name the four checks and, for each, one bug it catches that none of the others does

## Build brief

- [ ] `lab/linear.py` written, with the three shape assertions **inside** `linear_backward`
- [ ] `lab/gradcheck.py` written, with `numerical_gradient`, `relative_error` and the `judged` guard
- [ ] `lab/sweep.py` written; **your** `h` for `float64` and `float32`, with hardware line and date
- [ ] `RTOL` derived from **your** sweep, not copied from this document
- [ ] The `(B, T, C)` extension written **both** with `einsum` and with a reshape, and asserted equal
- [ ] `unbroadcast` used in place of the hand-written axis list, and the tests still pass
- [ ] The gradient check parametrised over at least three shape triples, one with a size-1 axis
- [ ] A judged-fraction test written and **watched red** by moving into `tanh` saturation
- [ ] The backward-costs-2×-forward argument written on paper: one sentence, two flop counts

## The evals that must be able to fail

- [ ] `uv run python -m pytest tests/test_linear.py -q` green
- [ ] Bias deleted from the forward pass → **check 2 red**, and you read the actual/desired values
- [ ] `dW = dY.T @ X` → **check 1 red**, naming both shapes
- [ ] `dW = X @ dY` at square shapes → **check 3 red** at order `1e0`
- [ ] `W + lr * dW` → **check 4 red**, loss increases
- [ ] Gradcheck at `tanh(25.0)` → **check 3′ red**, `0% of entries judged`
- [ ] Everything put back; the suite is green again
- [ ] `./m depth 4` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 8, 10)

- [ ] Every number you wrote down is **measured on your machine**, with hardware, seed and date — or
      cited. None was recalled.
- [ ] You did **not** copy this day's `0.0868`, `8.135e-11`, `3.69×` or `52,523×` figures into your own
      notes as if they were yours
- [ ] Where your machine disagreed with this document, you **recorded the disagreement** rather than
      assuming you were wrong

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say why a gradient check is deliberately run at shapes of 2, 3 and 5 and never at
      realistic ones

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**, and you can say why
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**, and you can say why
      the forty-step loop in part 1.5 is not a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-06 and MATH-07 closed on
      day 4
- [ ] `./m done 4` committed with the message from §11
