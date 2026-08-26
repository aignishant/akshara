# Day 8 — CHECKLIST

**IDs closed:** MATH-15, MATH-16
**Principles served:** 1, 2, 3, 8, 10, 11, 12, 16, 17, 18, 20
**Parts:** 12 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 8` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 9 days complete, then one commit reading
`day 008: Gradient descent and Adam — closes MATH-15, MATH-16`.

---

## Setup

- [ ] Day 7's checklist is fully ticked and `./m done 7` committed
- [ ] `./m scaffold 8` run; the lab directory exists
- [ ] **No packages installed today** — confirmed
- [ ] Day 4's `gradcheck` re-run against the gradients you will use in part 3.1 — **before** trusting
      that test
- [ ] You can say why today's test surface has curvatures `[1, 100]` and not `[1, 1]`

## MATH-15 — gradient descent and momentum (section 1)

- [ ] Read 1.1; ran its check-yourself — a gradient whose components differ by 100×
- [ ] Can say what an optimizer can and cannot observe
- [ ] Can define the condition number and say why it, not the parameter count, makes optimization hard
- [ ] Noticed that the steep coordinate hit **exactly** `0.0` on step 0 and can say why
- [ ] Can say why a flattening loss curve does not mean convergence
- [ ] Read 1.2; ran its check-yourself — one descending and one ascending sequence
- [ ] Can write the update rule and say why the sign is a minus
- [ ] Worked out why `w` shrinks by exactly `0.8` per step at `lr = 0.1`
- [ ] Can name the one-batch experiment that tells a wrong sign from a too-large step
- [ ] Can say why `-=` and `= ... -` differ for a 124M-parameter model
- [ ] Read 1.3; ran its check-yourself — one `lr` converging in a single step and one going nowhere
- [ ] **Wrote down `2/L` for two surfaces you derived yourself**, then verified each by sweeping
- [ ] Saw `lr = 1.0` give a **perfectly flat** loss curve for 1000 steps and can say what it hides
- [ ] Can say why `lr = 0.5` gave exactly `0.0` for `f(w) = w²`
- [ ] Can say what the update-to-weight ratio shows that the loss does not
- [ ] Read 1.4; ran its check-yourself — nine ordinary-looking steps of a doomed run
- [ ] **Recorded the step at which each `lr` overflowed** — and that `lr = 1.01` never did
- [ ] Can describe the shape of divergence and say why `nan` is a bad detector
- [ ] Can name the two quantities to log from step 1
- [ ] Saw `lr = 5000` **converge** on a convex saturating loss and can say why that proves nothing
- [ ] Read 1.5; ran its check-yourself — 138 steps against 653
- [ ] Can say why momentum speeds the flat direction and damps the steep one by the **same** mechanism
- [ ] Can give the memory length in terms of `β`
- [ ] Can state momentum's stability bound and say why it is **not** `2/L`
- [ ] Can say what raising `β` does to the effective learning rate, and in which convention

## MATH-16 — Adam and AdamW (section 2)

- [ ] Read 2.1; ran its check-yourself — two coordinates converging at identical rates
- [ ] Can say what `√v` is estimating and why it is computed elementwise
- [ ] Replaced `g**2` with `np.sum(g**2)` and watched per-parameter scaling switch off
- [ ] Can say what happens to the meaning of `lr` once you divide by `√v`
- [ ] Saw the `ε`-inside-vs-outside difference and **recorded the factor**
- [ ] Read 2.2; ran its check-yourself — the same step for gradients 12 orders of magnitude apart
- [ ] **Wrote Adam's four lines from memory** and checked them against the part
- [ ] Can say what each moment estimates and why `β₁ ≠ β₂`
- [ ] Can say why Adam's `lr` is ~1000× smaller than SGD's for the same model
- [ ] Can say why the `1e-6` gradient row was 1% short, and what that says about `ε`
- [ ] Noticed that Adam was **worse than RMSProp** on this surface and can say why
- [ ] Read 2.3; ran its check-yourself — a first step of exactly `lr`, and one 3.16× too large
- [ ] Can say whether the uncorrected first step is too large or too small — **with the factor**
- [ ] Can say which moment is biased harder and why the square root matters
- [ ] **Wrote down how many steps the `β₂` correction takes to reach within 1% of 1**
- [ ] Can state the difference between bias correction and warmup
- [ ] Read 2.4; ran its check-yourself — a model 4× bigger to train than to store
- [ ] **Wrote down bytes/parameter for SGD, momentum and Adam**
- [ ] Can say what mixed precision does to that table — and it is not what most people say
- [ ] Can name the one term the table leaves out
- [ ] Computed the training memory for a 7B model and said whether it fits on 80 GB
- [ ] Read 2.5; ran its check-yourself — a **91×** decay disparity from one `λ`
- [ ] Can say where the `λw` term goes in each scheme and why SGD does not care
- [ ] Saw the coupled form land **exactly** on the SGD+L2 analytic equilibrium
- [ ] Can give the shrink factor AdamW applies to a parameter with zero gradient
- [ ] Can say which parameter groups are normally excluded from weight decay, and why
- [ ] Read 2.6; ran its check-yourself — three different answers from the same 100 steps
- [ ] **Noticed that the buggy resume had the lowest loss** and can say why that is the danger
- [ ] Can list everything Adam's state consists of
- [ ] Can say which piece is not shaped like a parameter and why that makes it easy to lose
- [ ] Can say what a correct resume looks like in a loss curve

## Section 3 — Principle 12

- [ ] Read 3.1; ran its check-yourself — step-0 loss near `ln(V)`, final loss 3 orders below
- [ ] Can state what overfitting one batch proves and what it does **not**
- [ ] Can name four bugs that make it fail
- [ ] Can say what the step-zero loss should be and what each direction of deviation means
- [ ] Can say why the labels in this test are **random** on purpose
- [ ] Can say why no weight decay appears anywhere in this test

## Build brief

- [ ] `lab/surface.py` written — `quadratic`, `condition_number`
- [ ] `lab/optim.py` written — four optimizers, **one signature**, state per parameter tensor
- [ ] `lab/diagnose.py` written — range test, step health, divergence trend
- [ ] `lab/memory.py` written — the report for **your** planned model
- [ ] `tests/test_optim.py` written — descent, first step, resume, overfit-one-batch
- [ ] `2/L` derived on paper for two surfaces and **verified by sweeping**, with the grid resolution
      reported
- [ ] Momentum written **both** ways, with the learning-rate relationship stated as a formula
- [ ] Adam's first step asserted `== lr` at three gradient magnitudes; the `v̂` line deleted and the new
      first step **predicted before measuring**
- [ ] Part 2.5's comparison re-run on **your own** surface, with the disparity ratio explained
- [ ] Training memory computed for your Day 39 model, with and without mixed precision, arithmetic shown
- [ ] The overfit test **broken five ways**, each failure message recorded, and the one that still
      passes identified and explained

## The evals that must be able to fail

- [ ] `uv run python -m pytest tests/test_optim.py -q` green
- [ ] Update sign flipped → the loss rises **smoothly**, looking like training
- [ ] `lr` set 1% above `2/L` → 4000 steps, no `nan`, no convergence
- [ ] `v̂` correction deleted → first step `31.6×` `lr`
- [ ] `t` reset on resume → parameters move `4.2e-03`, loss changes 31×
- [ ] One parameter tensor frozen → **the loss plateaus on 16 examples**
- [ ] Everything put back; the suite is green
- [ ] `./m depth 8` passes without argument
- [ ] `./m check` exits `0`

## Overfit one batch (Principle 12)

- [ ] **Overfit one batch first** — loss reached ~0 on 16 examples before any other claim
- [ ] Step-zero loss checked against `ln(V)` and the gap explained
- [ ] Which of the five silent failures (plan §6) this test rules out, and which it **cannot** —
      written down

## Provenance (Principles 8, 10)

- [ ] Every number you wrote down is **measured on your machine**, with hardware, seed and date — or
      cited. None was recalled.
- [ ] **Every learning rate you recorded names its optimizer** (`3e-4` alone is a rumour)
- [ ] **Every momentum coefficient you recorded names its convention**
- [ ] Every value that is a **convention** rather than a measurement is labelled as one —
      `β₁`, `β₂`, `ε`, `lr` defaults included
- [ ] You did **not** copy this day's `91×`, `3.162`, `1940`, `138/653` or `16 bytes/param` figures into
      your notes as if they were yours
- [ ] Where your machine disagreed with this document, you **recorded the disagreement**

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can name the two things about real optimization this day **cannot** demonstrate, and which
      day measures each

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md`, `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can say why part 3.1 is a test rather than a run
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-15 and MATH-16 closed on
      day 8
- [ ] `./m done 8` committed with the message from §11
