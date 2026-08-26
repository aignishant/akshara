# Day 1 — CHECKLIST

**IDs closed:** OPS-01, OPS-02, OPS-03, OPS-04
**Principles served:** 1, 2, 6, 8, 9, 10, 13, 15, 16, 17, 18, 19
**Parts:** 14 across 4 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0 required, ~2 optional

> `./m done 1` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line showing 2 days complete, then one commit reading
`day 001: Bootstrap and the map — closes OPS-01, OPS-02, OPS-03, OPS-04`.

---

## Setup

- [ ] Day 0's checklist is fully ticked and `./m done 0` committed
- [ ] `.gitignore` extended with the **secret** patterns, and `git check-ignore -v .env` names the
      rule **before** `.env` was created
- [ ] Hugging Face account created and a **read** token issued — not write, and you can say why
- [ ] `.env.example` committed; `.env` created from it and **not** committed
- [ ] `nbstripout` version looked up live, pinned with `==`, and recorded in `docs/PACKAGES.md`
- [ ] `uv run nbstripout --install --attributes .gitattributes` run, and `.gitattributes` is committed

## OPS-01 — the repo as memory (section 1)

- [ ] Read 1.1; ran its check-yourself and **wrote down the three baseline numbers**
- [ ] Can answer out loud: what is the one question that decides whether the repo is genuinely the
      memory — and why is a ledger with no failed runs a warning sign?
- [ ] Read 1.2; `akshara/README.md` and `scripts/README.md` written, each leading with a **refusal**
- [ ] Ran 1.2's check-yourself; the `scripts/` → `akshara` import count is **0**
- [ ] Can answer out loud: why does a directory carry information in proportion to what it excludes,
      and what breaks if `scripts/` imports `akshara/`?
- [ ] Read 1.3; can state the placement procedure's first question without looking
- [ ] Can answer out loud: why is the procedure ordered most-constrained first, and what is lost when
      a close call is placed without a note?

## OPS-02 — secrets and tokens (section 2)

- [ ] Read 2.1; ran its check-yourself and **all three numbers are 0**
- [ ] Can answer out loud: why must `.gitignore` cover `.env` *before* it exists, and why is "remove
      it from history" the wrong first response to a leaked credential?
- [ ] Read 2.2; `akshara/config.py` written with `load_env()` — typed, not installed
- [ ] `load_env` skips empty values, and you can say what `HF_TOKEN=""` would have broken later
- [ ] `load_env` lets an **existing** environment variable win, and you can say which day depends on
      that
- [ ] Ran 2.2's check-yourself and know your `token_source`
- [ ] Can answer out loud: why `os.environ["X"]` rather than `os.environ.get("X")`?
- [ ] Read 2.3; **built the leak demo** and saw the token present in the file and absent from the
      cell source
- [ ] Ran the `git show :` check — **`on disk: 1`, `in index: 0`**
- [ ] Deleted the demo notebook afterwards
- [ ] Can answer out loud: name two ways a credential reaches a notebook's output without appearing
      in any cell's source

## OPS-03 — the ledgers (section 3)

- [ ] Read 3.1; ran its check-yourself — **6 hand-written ledgers exist**, and the newest date is today
- [ ] Can answer out loud: why is a correction appended rather than applied, and why is a partially
      maintained ledger worse than an empty one?
- [ ] Read 3.2; can name the columns of a `RUNS.md` row **from memory**
- [ ] Can answer out loud: name three things that change a training result and are recoverable from
      neither the checkpoint nor the code
- [ ] Can say why a ledger where every config has exactly one seed cannot support a claim of
      improvement
- [ ] Read 3.3; ran its check-yourself — the parser reports **162 days and 309 IDs**, matching the
      plan's own frontmatter
- [ ] Can answer out loud: what is a primary fact versus a derived fact, and what new failure mode do
      you accept by generating a ledger?
- [ ] Read 3.4; **edited `TRACEABILITY.md` on purpose**, ran `./m check`, and watched the edit vanish
      with no warning
- [ ] Ran 3.4's check-yourself — **differing lines: 0**
- [ ] Can answer out loud: why is correcting a generated file worse than leaving the wrong number
      visible?

## OPS-04 — free compute (section 4)

- [ ] Read 4.1; `device()` written in `akshara/config.py`, with `AKSHARA_FORCE_CPU` checked **first**
- [ ] Ran 4.1's check-yourself and know what your machine actually reports
- [ ] Can answer out loud: name two things a T0 smoke run proves and two it proves nothing about
- [ ] Read 4.2; Colab **and** Kaggle accounts created, and you can say why two rather than one
- [ ] Can answer out loud: name the three currencies free compute is paid for in
- [ ] Can say why the `RUNS.md` row is written at launch rather than at exit
- [ ] Read 4.3; can list the five cells of a T1 notebook and say what each may **not** contain
- [ ] Can answer out loud: why is "it ran in my session" not evidence that a notebook works?
- [ ] Read 4.4; **built both toy scripts**, killed the fragile one, and confirmed `result.txt` does
      not exist
- [ ] Ran the durable one, killed it, resumed it, and confirmed **both runs print `done 465`**
- [ ] Ran the clean-versus-resumed `diff` and saw `IDENTICAL`
- [ ] Cleaned up `/tmp/preempt`
- [ ] Can answer out loud: name three things besides the weights a checkpoint must contain, and say
      why "the resume ran successfully" is not evidence that the resume is correct

## 💥 The evals that must be able to fail

- [ ] **Notebook filter** — observed `on disk: 1` and `in index: 0`. A `1` in the index means the
      filter is not installed and the guard does not exist
- [ ] **Resume correctness** — observed the clean run and the resumed run print the **same number**.
      A difference means the resume path loses or duplicates work
- [ ] **Generated-ledger edit** — observed an edit to `TRACEABILITY.md` silently disappear

## Optional T1 excursion

- [ ] Ran part 4.2's measurement cell on a free GPU notebook
- [ ] Recorded `colab-gpu (observed)` and `colab-host (observed)` rows in `docs/PACKAGES.md`, **with
      today's date**
- [ ] Understand that Day 66 sizes Akshara against those numbers, and that skipping this now means
      doing it then

## Build brief — the `TODO(me)` items

- [ ] `TODO(me)` #1: credential scan wired into `./m check`
- [ ] `TODO(me)` #2: stale-generated-ledger check wired into `./m check`
- [ ] `TODO(me)` #3: the `scripts/` must-not-import-`akshara` grep wired into `./m check`
- [ ] All three verified by **breaking each one on purpose** and watching the gate go red

## Verification

- [ ] `uv run ruff check .` clean
- [ ] `uv run ruff format --check .` clean
- [ ] `uv run python scripts/depth_check.py 1` green — and you did not argue with it
- [ ] `./m trace` shows Day 1 closing **exactly** OPS-01..04, no more and no fewer
- [ ] `./m check` exits `0`
- [ ] `git ls-files | grep -c '^\.env$'` prints **0**
- [ ] `git ls-files -z | xargs -0 grep -lE 'hf_[A-Za-z0-9]{20,}'` finds **nothing**
- [ ] No artifact staged: `git diff --cached --name-only | grep -E '\.(safetensors|pt|bin)$'` empty

## Ledger

- [ ] `docs/PROGRESS.md` row pasted from hub §11, with your real commit sha
- [ ] `docs/PACKAGES.md` row for `nbstripout` with the version **your** lookup printed
- [ ] Any T1 measurement rows added, dated today
- [ ] Confirmed **no** `DATASETS.md`, `MODELS.md` or `RUNS.md` rows are needed today, and
      can say why for each
- [ ] `./m tracker` regenerated, and `docs/TRACKER.md` shows Day 1 with 14 parts

## Commit

- [ ] `./m done 1` — and it committed only after refusing everything it should have refused
