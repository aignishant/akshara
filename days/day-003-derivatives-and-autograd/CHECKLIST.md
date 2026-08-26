# Day 3 — CHECKLIST

**IDs closed:** MATH-04, MATH-05
**Principles served:** 1, 2, 3, 8, 10, 11, 12, 16, 17, 18
**Parts:** 12 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 3` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 4 days complete, then one commit reading
`day 003: Derivatives by hand and a scalar autograd engine — closes MATH-04, MATH-05`.

---

## Setup

- [ ] Day 2's checklist is fully ticked and `./m done 2` committed
- [ ] `./m scaffold 3` run; `days/day-003-derivatives-and-autograd/lab/` exists
- [ ] **No packages installed today** — confirmed, and you can say why nothing new was needed

## MATH-04 — the derivative (section 1)

- [ ] Read 1.1; ran its check-yourself and the error column is **exactly `h`** at every step
- [ ] Can state what a derivative answers in one sentence with the word *nudge* in it
- [ ] Can say what the **sign** of a gradient tells you and what its **size** tells you
- [ ] Reproduced the `abs(x)` corner at zero and got `+1.0` and `-1.0` from the two sides
- [ ] Read 1.2; ran its check-yourself — the two methods agreed and `0.5 ** 50` printed
      `8.881784197001252e-16`
- [ ] Compared that to `float32` eps from Day 2 part 1.2 and can say what it means for the update
- [ ] Can state the chain rule in one sentence using the word *local*
- [ ] Can explain, with the arithmetic, why depth 50 at 0.9 trains and depth 50 at 0.5 does not
- [ ] Can name the architectural feature whose local derivative is exactly 1, and say why that matters
- [ ] Read 1.3; ran its check-yourself — the third number is the **sum** of the first two
- [ ] Printed one route alone and asked yourself what in a training log would have told you
- [ ] Can state the two rules: what happens *along* a path, and what happens *across* paths
- [ ] Read 1.4; worked out `a.grad` **on paper** before running the seven-node check
- [ ] All seven values and all seven gradients match the table in the part
- [ ] Changed `d = e + c` to `d = e + c + c` and **predicted** `c`'s new gradient before running
- [ ] Can explain, with one pond and ten thousand houses, why backward is the cheap direction
- [ ] Can say what would have to be true about a problem for **forward** mode to be cheaper
- [ ] Read 1.5; ran the `h` sweep **on your machine** and found your own minimum
- [ ] **Wrote your best `h` down** — Day 4's gradient check uses it, not this document's
- [ ] Saw the numerator go to exactly `0.0` at `h = 1e-16` and can explain it via `float64` eps
- [ ] Can name the two errors that fight as `h` shrinks and say which direction each moves
- [ ] Can say what happens to the best `h` in `float32`, and by roughly how many orders of magnitude

## MATH-05 — the engine (section 2)

- [ ] Read 2.1; wrote `Value` with `data`, `grad`, `_prev`, `_backward` and `_op`
- [ ] Ran 2.1's check-yourself; `d._op` is `+`, the labels are `['*', 'leaf']`, `a._prev` is `set()`
- [ ] **Measured bytes per node with `tracemalloc` on your machine** and wrote the number down
- [ ] Can say why `tracemalloc` was used instead of `sys.getsizeof` here
- [ ] Ran `len((a * a)._prev)` and can say why `1` is correct
- [ ] Can name the four things a node carries and what each is for
- [ ] Can explain why the arrows point at operands rather than at consumers
- [ ] Read 2.2; implemented `+`, `*`, `**`, `tanh`, `exp` and **all four** reflected operators
- [ ] Confirmed `2 * Value(3.0)` works, not just `Value(3.0) * 2`
- [ ] `__pow__` **asserts** a constant exponent, and you can say what silently guessing would cost
- [ ] Ran 2.2's check-yourself; all three pairs agree to at least eight significant figures
- [ ] Can state the one line every backward pass contains, and name what the `*` and the `+=` are
- [ ] Can say why `a - b` and `a / b` need no derivative rule of their own
- [ ] Read 2.3; implemented `backward()` with a post-order traversal and a `visited` set
- [ ] Ran 2.3's check-yourself; `dL/da` is exactly `8.0`
- [ ] **Moved `order.append` above the child loop, watched the number change, and put it back**
- [ ] Can state the single ordering constraint the backward pass must satisfy
- [ ] Can name the **two separate** things that go wrong when you recurse from the loss
- [ ] Read 2.4; ran its check-yourself — `6.0` for `x*x` and `12.0` for the chain
- [ ] **Changed one `+=` to `=`, watched `6.0` become `3.0`, and confirmed the chain still gave `12.0`**
- [ ] Confirmed two `backward()` calls on the same leaf give `4.0`, not `2.0`
- [ ] Can explain why `=` gives exactly half for `x·x`
- [ ] Can name the architectural feature that appears once per block and is corrupted on every one
- [ ] Read 2.5; ran its check-yourself — `6, 12, 18, 24` without zeroing and `6, 6, 6, 6` with
- [ ] Moved `w.grad = 0.0` to the **end** of the loop and can say what that tells you about placement
- [ ] Can explain why the engine cannot zero gradients for you, naming the legitimate use of
      cross-call accumulation
- [ ] Can describe the shape of a run with this bug, **including why lowering the LR does not fix it**

## Scaling up (section 3)

- [ ] Read 3.1; ran the scalar-vs-numpy benchmark **at two sizes** and recorded the ratio
- [ ] Your ratio is above `8`, and you can say which second effect accounts for the excess
- [ ] Ran it at `N = 32` and **watched it raise `RecursionError`**
- [ ] Can say which line of part 2.3 the traceback points at, and where the depth actually came from
- [ ] Computed the `(8, 512, 768)` activation memory both ways and wrote both figures down
- [ ] Can name the three separate costs and the **single** design change that fixes all three
- [ ] Can state what backpropagating through a **broadcast** turns into, and why
- [ ] Read 3.2; ran the memory experiment at two step counts, **with `gc.collect()`**
- [ ] The detached column is flat and the attached column is proportional to the step count
- [ ] Rebuilt the running-average variant and can say which column it resembled
- [ ] Can explain why keeping one node alive keeps a whole graph alive
- [ ] Can name the three places in an ordinary training loop where a node outlives its step

## Build brief

- [ ] `lab/engine.py` written — every line typed, none pasted
- [ ] `lab/sweep.py` written; **your** `h` recorded, with your hardware line and the date
- [ ] `lab/cost.py` written; scalar-vs-numpy at two sizes, and the memory slope, both recorded
- [ ] `lab/test_engine.py` written with the fan-out, accumulation and leak tests
- [ ] The iterative topological sort `TODO(me)` attempted, and the `N = 32` result recorded **either
      way** — it working and it still raising are both findings (Principle 10)
- [ ] `log()` added, with its gradient check **and** its `x = 0` edge case answered in writing
- [ ] `draw()` added and used at least once on a graph that surprised you
- [ ] `numeric_grad(f, args, i)` written, using **your** measured `h`
- [ ] The `x * x` set-versus-contributions question answered on paper — two numbers, and why they
      differ

## The evals that must be able to fail

- [ ] Check 1 (fan-out) green at `8.0`
- [ ] Check 1 **watched red** by moving `order.append`
- [ ] Check 2 (accumulation) green at `6.0`
- [ ] Check 2 **watched red** at `3.0` by changing one `+=` — and check 1 still passed, and you noticed
- [ ] Check 3 (no leak) green at `[6.0, 6.0, 6.0]`
- [ ] Check 3 **watched red** at `[6.0, 12.0, 18.0]`
- [ ] Check 4 (agrees with the numerical method) green with **your** `h`
- [ ] Check 4 run with `h = 1e-16` once, to see a check that cannot fail
- [ ] `./m depth 3` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 8, 10)

- [ ] Every number you wrote down today is **measured on your machine**, with hardware, seed and date —
      or cited. None was recalled.
- [ ] You did **not** copy this day's `µs/node`, `52,523×`, `512 bytes` or `KiB` figures into your notes
      as if they were yours
- [ ] Where your machine disagreed with this document, you **recorded the disagreement** rather than
      assuming you were wrong

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say what today's CPU measurements prove, and what they prove nothing about

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**, and you can say why
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-04 and MATH-05 closed on
      day 3
- [ ] `./m done 3` committed with the message from §11
