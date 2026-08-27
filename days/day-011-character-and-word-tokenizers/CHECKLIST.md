# Day 11 — CHECKLIST

**IDs closed:** TOK-05, TOK-06
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 16, 17, 18
**Parts:** 11 across 3 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 11` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **written** count reads 12, then one commit reading
`day 011: Character-level and word-level tokenizers — closes TOK-05, TOK-06`.

---

## Setup

- [ ] Day 10's checklist is fully ticked and `./m done 10` committed
- [ ] `./m scaffold 11` run; the lab directory exists
- [ ] **No packages installed today** — confirmed; everything used is the standard library
- [ ] The corpus sha256 printed and **written down**, and compared against `9760f2b6d4340b97`
- [ ] You can say what it means if your hash differs, and whether that makes this day wrong
- [ ] Day 9 part 2.1 re-read — you can state the round-trip contract from memory

## TOK-05 — the character tokenizer (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] `CharTokenizer` written into `akshara/tokenizer/char.py`, by hand, every line
- [ ] Round-tripped the **whole corpus** and got `True`
- [ ] Confirmed the ids for `'Overfit one batch'` match Day 9's exactly — and can say why that matters
- [ ] Saved, reloaded, and confirmed the two hashes match
- [ ] Can name the four things the class adds over Day 9's nine lines
- [ ] Read 1.2; ran its check-yourself
- [ ] Measured `V` under five definitions of "character" on your own corpus
- [ ] Can say which transforms are allowed inside `from_text` and which are not, and state the property
      that decides it
- [ ] Saw that `NFKC` **adds** tokens, and can name the two characters responsible
- [ ] Can say why the 143 distinct bytes in this corpus is the wrong number to size a byte vocabulary
- [ ] Printed the vocabulary by Unicode category and looked at it — you can say how many entries are
      symbols rather than letters
- [ ] Read 1.3; ran its check-yourself
- [ ] Measured characters-per-word on **held-out** text yourself
- [ ] Can name the three costs of a long tokenization and say which one compute cannot fix
- [ ] Can state how many words a 1,024-token context window holds at character level
- [ ] Can say whether the `30.9×` is a measurement or a projection, and which day makes it a timing
- [ ] Read 1.4; ran its check-yourself
- [ ] Can name the three unknown-character policies and which one breaks the contract
- [ ] Saw a foreign word encoded as **newlines** with `.get(ch, 0)`, and can say why id 0 is the newline
- [ ] Rebuilt the table with a reserved `<unk>` slot and can say what changed and what did **not**
- [ ] Can say why an averaged fallback rate hides the population it is failing
- [ ] Read 1.5; ran its check-yourself
- [ ] Computed your alphabet's coverage of assigned Unicode and can state it as a percentage
- [ ] Reproduced the three stages: `KeyError` → hotfix → falling loss
- [ ] Can explain, in one sentence, why destroying a fifth of a corpus lowers the reported loss by a fifth
- [ ] Can say why coverage must be asserted **per source** rather than over the whole corpus

## TOK-06 — the word tokenizer (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Measured tokens, types and hapax for at least four splitters on your own corpus
- [ ] Confirmed that **none** of them reconstructs the corpus — and can say what was lost
- [ ] Saw `re.findall(r"[A-Za-z']+", "3.14")` return `[]`, and can say what that does to a document
- [ ] Can say why the regex patterns must be raw strings
- [ ] Read 2.2; ran its check-yourself
- [ ] `WordTokenizer` written into `akshara/tokenizer/word.py`, with `<unk>` at slot 0 by construction
- [ ] Can say why a word tokenizer must have a cap and a character one need not
- [ ] Can name the two different orders used to select and to number the vocabulary, and why they differ
- [ ] Noticed that `max_size=1000` gives `V = 1001`, and can say what that breaks if ignored
- [ ] Built the vocabulary from the **training split only** — and can say what happens to the numbers if
      you do not
- [ ] Read 2.3; ran its check-yourself
- [ ] Measured the coverage curve at five caps **plus** the uncapped row
- [ ] Can state the uncapped out-of-vocabulary rate and explain in one sentence why it is not zero
- [ ] Measured the mean length of covered against uncovered words, and can say what it implies
- [ ] Reproduced the optimistic number from measuring against the wrong split, and can say why a
      plausible-but-wrong number is more dangerous than an obviously broken one
- [ ] Read 2.4; ran its check-yourself
- [ ] Measured the share of your vocabulary that is a stem plus a suffix
- [ ] Can say whether that figure is an over- or an under-estimate, and name two forms the heuristic misses
- [ ] Looked at the `learn` family's counts and noticed that the **stem is rarer than its inflections**
- [ ] Can name the three separate costs of one slot per inflected form, and which of the three a bigger
      vocabulary would fix
- [ ] Wrote the `TODO(me)` paragraph on what you would count to discover `ing` without a suffix list —
      **before** reading Day 12
- [ ] Read 2.5; ran its check-yourself
- [ ] Reproduced `the tokenizer <unk> its vocabulary and cannot <unk> anything <unk>` on your own machine
- [ ] Confirmed that five ordinary output checks pass on it and only the round trip fails
- [ ] Confirmed that **no piece** of the lost word exists in the vocabulary
- [ ] Can say what "no id sequence produces this word" means for capability as opposed to quality

## Section 3 — together

- [ ] Read 3.1; ran its check-yourself
- [ ] Built the six-column table on your own machine, every row from **one** held-out variable
- [ ] Can sort today's findings into trades and gates without looking
- [ ] Can say why the character tokenizer's gate has a handle on it and the word tokenizer's does not
- [ ] Can name the two cells in the table that are in-distribution artefacts, and say what would move them

## The eval that can go red (Principle 11)

- [ ] `tests/test_tokenizers.py` exists and runs CPU-only, offline, with no seed needed
- [ ] **Observed red before green:** added `.casefold()` to `from_text` → the corpus round-trip test failed
- [ ] **Observed red before green:** moved `normalize` out of `encode` → passed on ASCII, failed on a
      decomposed accent
- [ ] **Observed red before green:** dropped `sort_keys=True` → the hash stopped being stable
- [ ] The pre-tokenizer losslessness test was written, run, and **could not be made to pass** — and you
      decided deliberately what to do about that rather than deleting it
- [ ] The probe list includes the empty string, a bare space, doubled spaces, a number, and a non-Latin
      string

## Silent failures ruled out (plan §6)

- [ ] **#1 contamination** — you can say why a vocabulary built on the whole corpus makes every coverage
      number meaningless, and you measured both versions
- [ ] **#2 tokenizer/template mismatch** — your tokenizer has a hash, you saved and reloaded it, and you
      can say where that hash gets checked in a real system
- [ ] **#5 evaluated on the format you trained on** — you can name two numbers in today's table that are
      in-distribution artefacts, and say what data would move them

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with the corpus hash beside it
- [ ] You did **not** copy this day's `151`, `5.56`, `30.9`, `184.2`, `19.29%`, `10.41%`, `15.57%`,
      `6.60`, `4.07` or `0.101172%` figures into your notes as if they were yours
- [ ] Every figure you recorded names **which splitter** and **which split** produced it
- [ ] Part 1.3's `30.9×` is labelled in your notes as **arithmetic over a measured ratio**, not a timing
- [ ] Part 1.5's loss table is labelled as **arithmetic over a described model**, not a training run
- [ ] Part 2.4's `15.57%` is labelled as a **lower bound from a nine-suffix heuristic**
- [ ] Where your corpus hash differed from this document's, you **recorded that** and did not reuse this
      document's numbers

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] You can name the one question about tokenization schemes this day **cannot** answer, and which day
      answers it

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **confirmed no rows**
- [ ] `docs/DATASETS.md` — **confirmed no rows**, and you can say why the master plan is not a dataset row
- [ ] `docs/MODELS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can name the two figures that are arithmetic rather
      than runs
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-05 and TOK-06 closed on day 11
- [ ] `./m done 11` committed with the message from §11
