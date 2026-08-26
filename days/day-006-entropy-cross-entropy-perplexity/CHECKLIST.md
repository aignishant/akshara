# Day 6 — CHECKLIST

**IDs closed:** MATH-10, MATH-11, MATH-12
**Principles served:** 1, 2, 3, 8, 10, 11, 16, 17, 18, 20
**Parts:** 12 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 6` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 7 days complete, then one commit reading
`day 006: Entropy, cross-entropy and perplexity — closes MATH-10, MATH-11, MATH-12`.

---

## Setup

- [ ] Day 5's checklist is fully ticked and `./m done 5` committed
- [ ] `./m scaffold 6` run; the lab directory exists
- [ ] **No packages installed today** — confirmed
- [ ] You can say why the `nan` demonstrations need `np.errstate`, and why that must never appear in
      real code

## MATH-10 — entropy (section 1)

- [ ] Read 1.1; ran its check-yourself — six surprises, the additivity pair, and the `ln(2)` ratio
- [ ] Noticed that the additivity check prints **`False`** and can say why that is not a failure
- [ ] Can state the three requirements that force `I(p) = −log(p)`
- [ ] Can say which requirement is the reason a sequence loss is a sum rather than a product
- [ ] Read 1.2; ran its check-yourself — three uniforms hitting their ceilings **exactly**
- [ ] **Wrote down `ln(V)` for the vocabulary sizes you expect to use** — Day 25 checks against it
- [ ] Replaced the `np.where` guards with the naive formula and watched the `certain` row break
- [ ] Can define entropy in one sentence using the word *expected*, and state both bounds
- [ ] Read 1.3; ran its check-yourself — one `nan`, one biased value, one **9%** clipping error
- [ ] Can say why `0 · log(0)` is zero in mathematics and `nan` in arithmetic
- [ ] Can name the two kinds of zero and say which one masking is the right answer for
- [ ] Can say why `+ eps` and `clip` are both wrong, with a distinct reason for each

## MATH-11 — cross-entropy (section 2)

- [ ] Read 2.1; ran its check-yourself — `H(p, q) > H(p)`, `H(p, p) = H(p)`, and the asymmetry
- [ ] **Wrote down the excess** `0.257262` — part 3.1 names it
- [ ] Can say which argument supplies the weighting and which supplies the logarithm
- [ ] Can state the floor of cross-entropy and when it is reached
- [ ] Read 2.2; ran its check-yourself — two identical numbers and three shapes
- [ ] Dropped the `[..., None]` and read the error
- [ ] Can explain why `V − 1` terms vanish for a one-hot target
- [ ] Can say what shape **and dtype** the target has in every real implementation
- [ ] Wrote the target-shift assertion and can say what an unshifted target does to the loss
- [ ] Read 2.3; ran its check-yourself — two identical values, one `-inf`, one `-800`
- [ ] Can give the chain from "maximise the likelihood" to "minimise cross-entropy" in three steps
- [ ] Can say what `log(softmax(z))` simplifies to and why that form cannot underflow
- [ ] Read 2.4; ran its check-yourself — three numbers, and a fourth row where two are **identical**
- [ ] Can name the three reductions and say which question each answers
- [ ] Can say what changing `sum` to `mean` does to the gradient, **with the factor**
- [ ] Can say why the difference is invisible in a fixed-length test batch
- [ ] Read 2.5; ran its check-yourself and **watched the two columns move in opposite directions**
- [ ] The `-100` count equals the padded-position count — **the plan's §6 check, run**
- [ ] Can explain why the reported loss falls while the real loss rises
- [ ] Can name both standard fixes and say which one also covers prompt masking

## MATH-12 — KL and perplexity (section 3)

- [ ] Read 3.1; ran its check-yourself — the identity holds **exactly**, and one direction is `inf`
- [ ] Can state the identity linking entropy, cross-entropy and KL
- [ ] Can say what it tells you about how low a loss curve can go
- [ ] Can say which direction cross-entropy training uses, and what mode-covering means
- [ ] Read 3.2; ran its check-yourself — four perplexities equal to their vocabulary sizes exactly
- [ ] Saw the deliberately wrong unit give `36.845651` instead of `12.182494`
- [ ] Can state what perplexity means in one sentence with the word *choices*
- [ ] Can name the two things a perplexity number is meaningless without
- [ ] **Wrote down `ln(V)` and `V` for your planned vocabulary** as the step-0 expectation
- [ ] Read 3.3; ran its check-yourself — a **42×** perplexity spread and three identical bits/byte
- [ ] Saw the padding model report `37.29` where its real perplexity is `197.41`
- [ ] Can explain why a finer tokenizer gives a lower perplexity for the same model
- [ ] Can name the unit to report instead when tokenizers differ
- [ ] Read 3.4; ran its check-yourself — four numbers and an identity that holds
- [ ] Changed **one** function to `np.log2` and watched the identity fail by `1.4427`
- [ ] Can state both identities linking today's four quantities
- [ ] Can name three different bugs a single identity failure would distinguish between

## Build brief

- [ ] `lab/information.py` written — every function masked, every unit in the name
- [ ] `lab/loss.py` written — `log_softmax`, `nll_from_logits`, `reduce_loss` with an explicit `how`
- [ ] `lab/report.py` written — the five-line step-0 report with both warnings
- [ ] `tests/test_information.py` written — identity, padding, `log(0)`, unit
- [ ] The entropy of a **real file** measured, in bits/char **and** bits/byte, with the difference
      explained
- [ ] Cross-entropy implemented **three ways** and asserted equal, then timed
- [ ] The padding demonstration written as a test that **goes red** without the mask
- [ ] Step-0 loss and perplexity computed on paper for `V = 256` and `V = 32000`
- [ ] Part 3.3's three tokenizations converted: what a 10% quality gain looks like in each unit

## The evals that must be able to fail

- [ ] `uv run python -m pytest tests/test_information.py -q` green
- [ ] Mask removed from `entropy` → **`nan`** on a distribution with a zero
- [ ] One identity term switched to `np.log2` → identity fails, off by `1.4427`
- [ ] KL arguments swapped → a different finite number, and the non-negativity assertion fires
- [ ] Mask dropped from the loss → **the two losses move in opposite directions**
- [ ] `exp` applied to bits → `36.85` where it should be `12.18`
- [ ] Everything put back; the suite is green
- [ ] `./m depth 6` passes without argument
- [ ] `./m check` exits `0`

## Provenance (Principles 8, 10)

- [ ] Every number you wrote down is **measured on your machine**, with hardware, seed and date — or
      cited. None was recalled.
- [ ] **Every information number you recorded states its unit** (bits or nats)
- [ ] **Every perplexity you recorded states its tokenizer and its reduction**
- [ ] You did **not** copy this day's `1190/2000`, `42×`, `5.366416` or `0.838776` figures into your
      notes as if they were yours
- [ ] Where your machine disagreed with this document, you **recorded the disagreement**

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can say why **every** result in this day reproduces identically on any hardware — and what
      that says about the difference between this day and Day 2's timings

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **confirmed no rows**
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows MATH-10, MATH-11 and MATH-12
      closed on day 6
- [ ] `./m done 6` committed with the message from §11
