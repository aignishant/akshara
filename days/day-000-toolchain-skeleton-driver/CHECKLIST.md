# Day 0 — CHECKLIST

**IDs closed:** none (toolchain — plan §24.2, Phase 0)
**Principles served:** 1, 2, 6, 9, 10, 11, 13, 16, 17, 18, 19, 20
**Parts:** 13 across 6 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0

> `./m done 0` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && git log --oneline -1
```

Expected: `OK all green`, then one commit reading
`day 000: Toolchain, skeleton and the ./m driver — closes no IDs`.

---

## Setup — the toolchain (section 1)

- [ ] `uv` installed, and you **read the install script** at its URL before piping it to a shell
- [ ] `uv --version` run, and the number written into `docs/PACKAGES.md` is the one it printed
- [ ] `uv python pin 3.12` run; `.python-version` exists and contains `3.12`
- [ ] `uv sync` succeeds and `.venv/` exists
- [ ] `uv run python -c "import sys; print(sys.executable)"` prints a path **inside this project**
- [ ] Can say why every Python command from here on begins with `uv run`

## Section 1 — one owner for the environment

- [ ] Read 1.1; ran its check-yourself and **wrote down the number** of Pythons on your machine
- [ ] Can answer out loud: why does `ModuleNotFoundError` almost never mean the package is missing
      from the computer — and why is the silent version worse than the traceback?
- [ ] Read 1.2; ran its check-yourself and noted both numbers (installed distributions vs `==` pins)
- [ ] Can answer out loud: what does `uv.lock` record that `pyproject.toml` does not?
- [ ] Read 1.3; ran its check-yourself and compared **offered** against **observed**
- [ ] Can answer out loud: why does a ledger row need a date next to the version to mean anything?
- [ ] **Checked whether your `uv python list` offers a Python it has not installed** — and recorded
      the one that actually ran

## Section 2 — the skeleton

- [ ] Read 2.1; the six `akshara/` subpackages exist and each has an `__init__.py`
- [ ] Ran 2.1's check-yourself; `pkgutil.iter_modules` reports **6**
- [ ] Can answer out loud: pick two directories and say what would be **wrong** to put in each
- [ ] Read 2.2; `pyproject.toml` written with `dependencies = []` and you can say why empty is a
      decision rather than an omission
- [ ] `[tool.pytest.ini_options]` includes `--strict-markers` and the three markers are declared
- [ ] Ran 2.2's check-yourself; **the collected-test count is 0 and you know it is 0**
- [ ] Can answer out loud: why is a passing test suite that selected zero tests worse than a failing
      one?

## Section 3 — gitignore first

- [ ] Read 3.1; `.gitignore` written **before** any artifact existed
- [ ] Ran `git check-ignore -v` on a fake weight file and saw **the rule and line number** that
      matched — not just silence
- [ ] Ran 3.1's check-yourself; tracked-artifact count is **0**
- [ ] Can answer out loud: why does adding a pattern do nothing for an already-tracked file, and what
      is the difference between the *secret* reason and the *artifact* reason for excluding a file?
- [ ] Read 3.2; **committed a 40MB file on purpose**, then ran `git rm --cached`, and watched
      `size-pack` **not go down**
- [ ] Ran `git reset --hard` and then `git gc --prune=now`, and watched the size finally drop
- [ ] Can answer out loud: why does `git rm` not shrink a repository, and name the three mechanisms
      this project uses to keep a checkpoint out of git — in order of how much each relies on you
      remembering anything

## Section 4 — the driver

- [ ] Read 4.1; `m` created, `chmod +x m` **and** `git update-index --chmod=+x m` both run
- [ ] Ran 4.1's check-yourself; the advertised command count matches the `case` clauses
- [ ] Can answer out loud: what does `set -e` prevent, and why is a driver that can *refuse* worth
      more than one that only runs things?
- [ ] Read 4.2; `./m start 0` lists this day's parts in order
- [ ] The gate contains `|| [ $? -eq 5 ]` and **not** `|| true`, and you can say what `|| true` would
      have broken
- [ ] Ran `./m check; echo $?` and read the **exit code**, not the printed word
- [ ] Read 4.3; the staged-artifact refusal is implemented **before** the checklist test
- [ ] Ran 4.3's check-yourself; the gate **refused with exit=1**
- [ ] Can answer out loud: what is the one thing `./m done` fundamentally cannot verify about your day?

## Section 5 — the depth check

- [ ] Read 5.1; ran `uv run python scripts/depth_check.py` and read its exit code
- [ ] Ran 5.1's check-yourself; noted **how many distinct rules** the script enforces
- [ ] Can answer out loud: which half of the depth contract can a script enforce, and why would a
      rule that counted words be worse than no rule?
- [ ] Read 5.2; ran its check-yourself and noted the exempt-language and clock-pattern counts
- [ ] Can answer out loud: why is a false positive more dangerous to a check's survival than a false
      negative, and what will `depth_check.py` never be able to tell you?

## 💥 Section 6 — the failure lab (the eval that must be able to fail)

**Every one of these must be observed refusing. A guard that does not refuse is a guard you do not
have.**

- [ ] **Break 1** — staged an artifact past `.gitignore` with `git add -f`; `./m done 0` printed
      `FAIL a weight/dataset file is staged` and **exit=1**
- [ ] **Break 2** — left an unticked box; `./m done 0` refused and printed the **line number**
- [ ] **Break 3** — added a reader-directed time estimate to a part; `depth_check.py` failed citing
      **Principle 17**
- [ ] **Break 4** — deleted an `In production` section; `depth_check.py` failed naming the **missing
      section**
- [ ] Ran the tally from 6.1's check-yourself: **4 guards refused**
- [ ] **Restored everything you broke** — the section, the clock sentence, the checklist — and
      `uv run python scripts/depth_check.py 0` is green again
- [ ] Read each refusal message *as a user* and can say whether it would be enough in nine weeks
- [ ] Can answer out loud: why do guards 1 and 2 protect against the same mistake, and why is a guard
      that has never fired indistinguishable from a broken one?

## Build brief — the `TODO(me)` items

- [ ] `TODO(me)` #1 solved: the staged-artifact refusal added to `./m done`, ordered **before** the
      checklist test, and verified by Break 1
- [ ] `TODO(me)` #2 solved: `./m status` wired to `scripts/tracker.py --summary`, and its printed
      count matches `docs/TRACKER.md`

## Verification

- [ ] `uv run ruff check .` clean
- [ ] `uv run ruff format --check .` clean
- [ ] `uv run python scripts/depth_check.py 0` green — **and you did not argue with it**
- [ ] `uv run python scripts/trace.py` runs; Day 0 claims **no IDs**, matching plan §24.2
- [ ] `./m check` exits `0`
- [ ] `git ls-files | grep -E '\.(safetensors|gguf|bin|pt|pth|ckpt|npy)$'` prints **nothing**
- [ ] No secret is in `git ls-files` (there is no `.env` yet — that arrives tomorrow, OPS-02)

## Ledger

- [ ] `docs/PROGRESS.md` row pasted from hub §11, with your real commit sha
- [ ] `docs/PACKAGES.md` rows pasted — **five rows, with the versions your machine printed**, not the
      ones in the document
- [ ] Confirmed **no** `DATASETS.md`, `MODELS.md`, `RUNS.md` or `PAPERS.md` rows are needed today, and
      can say why for each
- [ ] `docs/TRACKER.md` regenerated (`./m tracker`)

## Commit

- [ ] `./m done 0` — and it committed only after refusing everything it should have refused
