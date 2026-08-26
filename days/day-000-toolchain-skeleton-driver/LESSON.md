---
day: 0
phase: 0
phase_name: "Foundry: the machine, the skeleton, the driver"
title: "Toolchain, skeleton and the ./m driver"
ids: []
principles: [1, 2, 6, 9, 10, 11, 13, 16, 17, 18, 19, 20]
kind: setup
plan_version: "v1.2.0"
parts: 13
compute_tier: T0
generated: "2026-08-25"
status: written
lab_scaffolded: false
commit: ""
---

# Day 0 — Toolchain, skeleton and the `./m` driver

> **Yesterday:** nothing. This is the first day, and the repository does not exist yet.
> **Today:** you build the machine that everything else assumes — one tool that owns the environment,
> a repository shaped like the work, a `.gitignore` written before there is anything to protect, a
> driver that gives every operation one name, and a gate that **refuses** to finish a day that is not
> finished. Then you break all four guards on purpose and watch each one catch you.
> **Tomorrow (Day 1):** the repository stops being a generic Python project and becomes Akshara's
> memory — the six ledgers, `scripts/trace.py`, the Hugging Face token, and the free-compute
> accounts (OPS-01..04).

---

## §1 Where we are

Nothing about today is about generative AI. That is the point, and it is worth being honest about
before you start.

Imagine a workshop where four different rulers hang on the wall, each marked in slightly different
units, and nobody remembers which one the last measurement used. Every individual cut is careful.
Every measurement is taken honestly. And the pieces do not fit, because "one metre" was never a
single thing in that room. The problem is not skill. It is that a question everybody assumed had one
answer had four, and nothing in the room ever said so.

That is what a computer is like before somebody decides who owns the environment. There are several
Pythons, several copies of the same library, and several tools each resolving "which one?" by its own
rule. Nothing warns you, because from each tool's point of view nothing is wrong.

In ordinary software that costs you an afternoon. Here it costs you something worse. The code you are
about to spend a hundred and sixty-one days writing does not crash when the environment is wrong — it
**runs**, and returns a slightly different number. A changed default, a changed rounding mode, a
changed seed: the loss still goes down, the model still trains, and you have quietly run a different
experiment than the one you think you ran. There is no traceback for that. The only defence is that
the environment was pinned in a file you committed, so "the same environment" is something you can
check rather than something you assume.

So today is about turning assumptions into artifacts. One tool owns the interpreter and the packages,
and the versions live in a lockfile. The layout is decided once, so "where does this go?" has an
answer instead of a hundred local answers. The rule that weights never enter git is written while the
repository is empty and the rule costs nothing — because the moment it starts costing something is
the moment nobody follows it. Every operation gets one name, in one file, so that the answer to "how
do I run the checks here?" lives in the repository rather than in your memory of this week.

And then the last section does the thing that makes any of it trustworthy: it breaks all four guards
deliberately. A guard that has never fired and a guard that is broken emit exactly the same signal,
which is silence. Today is the cheapest day in the entire plan to learn which one you have.

---

## §2 The map

Thirteen parts, six sections. The day climbs `foundation → working → production` and ends with a
deliberate failure. It closes **no curriculum IDs** by design — everything here is a precondition for
the curriculum rather than part of it.

### Section 1 — `01-the-toolchain`: one owner for the environment

What goes wrong when several tools each answer "which Python?", and the single tool that ends it.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [The four Pythons](parts/01-the-toolchain/1.1-the-four-pythons.md) | Why does the same command install something and then fail to find it? | `foundation` |
| 1.2 | [uv owns the environment](parts/01-the-toolchain/1.2-uv-owns-the-environment.md) | What does a lockfile record that a dependency list does not? | `working` |
| 1.3 | [Observed is not available](parts/01-the-toolchain/1.3-observed-is-not-available.md) | Why is the version a tool *lists* not the version you may write down? | `working` |

### Section 2 — `02-the-skeleton`: a repository shaped like the work

The layout as a set of decisions, and the one file that holds every tool's settings.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [Directories as argument](parts/02-the-skeleton/2.1-directories-as-argument.md) | What would be *wrong* to put in each directory — and why is that the useful question? | `foundation` |
| 2.2 | [One file owns the config](parts/02-the-skeleton/2.2-one-file-owns-the-config.md) | How does a test suite pass by running nothing, and what stops it? | `working` |

### Section 3 — `03-gitignore-first`: the file written before the thing it protects

Two different reasons to exclude a file, and why one of them is permanent.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [Ignore it before it exists](parts/03-gitignore-first/3.1-ignore-before-it-exists.md) | Why does adding a pattern do nothing for a file that is already tracked? | `working` |
| 3.2 | [💥 The checkpoint that cannot be removed](parts/03-gitignore-first/3.2-the-checkpoint-that-cannot-be-removed.md) | You deleted the 400MB file — so why is the repository still 400MB bigger? | `production` |

### Section 4 — `04-the-driver`: one name for every operation

Why a repository needs a driver, how it resolves a day, and the property that makes it worth having.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Why a driver](parts/04-the-driver/4.1-why-a-driver.md) | What does `set -e` prevent, and why is refusing more valuable than running? | `foundation` |
| 4.2 | [Building the driver](parts/04-the-driver/4.2-building-the-driver.md) | Why glob `day-043-*` instead of building the folder name — and what would `\|\| true` have broken? | `working` |
| 4.3 | [`./m done` — the gate that refuses](parts/04-the-driver/4.3-the-gate-that-refuses.md) | Why is the staged-artifact check ordered before everything else? | `production` |

### Section 5 — `05-the-depth-check`: the contract made mechanical

Which half of a standard a script can enforce, and the half it must never try to.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 5.1 | [A contract nobody checks](parts/05-the-depth-check/5.1-a-contract-nobody-checks.md) | How does a good standard lose to a hundred reasonable exceptions? | `foundation` |
| 5.2 | [What the depth check cannot catch](parts/05-the-depth-check/5.2-what-depth-check-cannot-catch.md) | Why is a false positive more dangerous to a check's survival than a false negative? | `production` |

### Section 6 — `06-the-failure-lab`: the deliberate failure

Today's failure, run on purpose (plan §25.7).

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 6.1 | [💥 Four ways to break the gate](parts/06-the-failure-lab/6.1-four-ways-to-break-the-gate.md) | Why is a guard that has never fired indistinguishable from a broken one? | `production` |

---

## §3 Setup — run this

Nothing is installed today except the toolchain itself. No `numpy`, no `torch` — packages arrive on
the day they are first used, and only after the hand-rolled version exists (Principle 3).

```bash
# 1 — install uv (PowerShell on Windows; read the script at that URL first)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2 — observe what you actually got, and pin the interpreter
uv --version
uv python pin 3.12

# 3 — the skeleton
mkdir -p akshara/{tokenizer,model,train,infer,eval,serve} \
         configs scripts tests notebooks days docs/adr
touch akshara/__init__.py akshara/{tokenizer,model,train,infer,eval,serve}/__init__.py
touch tests/__init__.py

# 4 — create the environment and prove which interpreter answers
uv sync
uv run python -c "import sys; print(sys.executable); print(sys.version.split()[0])"

# 5 — make the driver executable, in git as well as locally
chmod +x m
git update-index --chmod=+x m
```

Versions this document **observed** on `2026-08-25` [measured here: Windows 11]. Use what your own
lookup prints, not these — Principle 6, and part
[1.3](parts/01-the-toolchain/1.3-observed-is-not-available.md) explains why the distinction matters:

| Tool | Observed | How |
| --- | --- | --- |
| git | 2.54.0.windows.1 | `git --version` |
| uv | 0.12.3 | `uv --version` |
| python | 3.12.12 | `sys.version` — **not** the top of `uv python list`, which offers 3.12.13 but has not installed it |
| ruff | 0.16.4 | `uv pip compile` against PyPI |
| pytest | 9.1.1 | `uv pip compile` against PyPI |

---

## §4 Build brief

Five files. Every line of them is printed in the parts; you type them.

| File | From | Contains |
| --- | --- | --- |
| `.python-version` | [1.2](parts/01-the-toolchain/1.2-uv-owns-the-environment.md) | `3.12` — written by `uv python pin` |
| `pyproject.toml` | [2.2](parts/02-the-skeleton/2.2-one-file-owns-the-config.md) | project metadata, empty `dependencies`, ruff + pytest settings with `--strict-markers` |
| `.gitignore` | [3.1](parts/03-gitignore-first/3.1-ignore-before-it-exists.md) | the artifact patterns, written on an empty repository |
| `m` | [4.2](parts/04-the-driver/4.2-building-the-driver.md) | `status` · `start` · `parts` · `depth` · `trace` · `tracker` · `scaffold` · `check` · `done` |
| `Makefile` | [4.1](parts/04-the-driver/4.1-why-a-driver.md) | a two-line shim so `make check` reaches `./m check` |

```text
TODO(me): in `m`, the `done` case currently commits after `./m check`.
          Add the staged-artifact refusal described in part 4.3 — before the
          checklist test, because it guards the irreversible mistake.

TODO(me): `./m status` is listed in the usage text. Wire it to
          `scripts/tracker.py --summary` and confirm the printed count matches
          what you see in docs/TRACKER.md.
```

---

## §5 The eval that must be able to fail

Today's red check is **four red checks**, and they are the whole of part
[6.1](parts/06-the-failure-lab/6.1-four-ways-to-break-the-gate.md). Each guard must be observed
refusing:

```bash
# 1 — stage an artifact past .gitignore; ./m done must refuse
mkdir -p checkpoints && uv run python -c "open('checkpoints/probe.pt','wb').write(b'0'*2048)"
git add -f checkpoints/probe.pt
./m done 0; echo "must be 1 → exit=$?"
git reset -q HEAD checkpoints/probe.pt; rm -rf checkpoints
```

The other three — the unticked checklist, the smuggled clock, the missing `In production` section —
are run in part 6.1 with their cleanup. **A guard that does not refuse is a guard you do not have**,
and today is the cheapest day in the plan to find that out.

---

## §6 Compute budget

**Tier: T0** — laptop CPU, throughout. No GPU is used, none is required, and nothing is deferred to
bigger hardware.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0** |
| Free notebook sessions | **0** |
| Network | one `uv` download, plus the interpreter if 3.12 is not present |
| Disk | under 200 MB (`.venv` plus the toolchain) |

The `-m "not gpu"` filter in `./m check` and the CPU-only test rule in `CLAUDE.md` are what make T0 a
guarantee rather than a hope — see part
[4.2](parts/04-the-driver/4.2-building-the-driver.md).

---

## §7 Traps

| Trap | What you see | Where it is explained |
| --- | --- | --- |
| `pip install` outside `uv` | package installs, import still fails | [1.1](parts/01-the-toolchain/1.1-the-four-pythons.md) |
| Copying a version from `uv python list` | a ledger row naming an interpreter that never ran | [1.3](parts/01-the-toolchain/1.3-observed-is-not-available.md) |
| `\|\| true` instead of `\|\| [ $? -eq 5 ]` | `./m check` prints "OK all green" over a failing test | [4.2](parts/04-the-driver/4.2-building-the-driver.md) |
| Omitting `set -euo pipefail` | a failed step scrolls past and the day commits anyway | [4.1](parts/04-the-driver/4.1-why-a-driver.md) |
| `.gitignore` added *after* a file is tracked | the pattern is ignored entirely; nothing warns | [3.1](parts/03-gitignore-first/3.1-ignore-before-it-exists.md) |
| `git rm` to shrink a repository | the object stays in history forever | [3.2](parts/03-gitignore-first/3.2-the-checkpoint-that-cannot-be-removed.md) |
| CRLF line endings in `m` | `cannot execute: required file not found` | [4.1](parts/04-the-driver/4.1-why-a-driver.md) |
| Missing `--strict-markers` | a typo'd marker runs a GPU test inside a CPU-only gate | [2.2](parts/02-the-skeleton/2.2-one-file-owns-the-config.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement.** It arrives today through the
environment rather than through a seed: two runs under "the same" setup that were not the same, with
nothing red anywhere. The detection is that the environment is pinned in a committed lockfile, so
"same environment" is checkable. Every part of section 1 is about making that true.

---

## §8 Verify before you code

Fetched on `2026-08-25`, not recalled (Principles 6, 7, 8):

| Source | Checked for |
| --- | --- |
| `https://docs.astral.sh/uv/` | the install command, `uv python pin`, `uv sync`, `uv run` semantics |
| `https://astral.sh/uv/install.ps1` | read before piping to a shell (Principle 13) |
| `uv --version`, `git --version`, `uv python list` | the observed versions in §3, on this machine |
| `uv pip compile` against PyPI | ruff and pytest resolved versions |
| `https://docs.astral.sh/ruff/settings/` | `line-length`, `extend-exclude`, `per-file-ignores` |
| `https://docs.pytest.org/en/stable/reference/exit-codes.html` | exit code `5` = no tests collected — the basis of the `\|\| [ $? -eq 5 ]` clause |
| `https://git-scm.com/docs/gitignore` | tracked files are unaffected by later patterns |

---

## §9 Say it in an interview

"Before I wrote any model code I spent a day on the machine, and the reason is specific to this kind
of work: numerical code with the wrong library version doesn't crash, it returns a slightly different
number. So the environment is owned by one tool and pinned in a committed lockfile, which makes 'the
same environment' something I can check rather than assume. The part I'd actually defend hardest is
the failure lab at the end — I broke all four guards on purpose and watched each one refuse, because a
guard that has never fired and a guard that's broken send exactly the same signal, which is silence. I
found out on an empty repository, with a 40MB file of zeros, that `git rm` doesn't shrink anything —
rather than finding out on the day I had a real checkpoint and no way to un-commit it."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 0` will refuse while any box is unticked, an artifact is staged, or the gate is red. It
cannot tell whether you were honest — that part is yours. Defined by understanding and green checks,
**never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 0 | 2026-08-25 | — (no IDs; toolchain) | 13 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — paste these, **with the versions your own lookups printed**, not the ones here:

```text
| git | 2.54.0.windows.1 | 2026-08-25 | 0 | Version control + Git Bash, the shell every day document is written for. Observed with `git --version`. |
| uv | 0.12.3 | 2026-08-25 | 0 | One binary owns interpreter, packages, lock and run. Observed with `uv --version`. |
| python | 3.12.12 | 2026-08-25 | 0 | Runtime, per plan §5. Observed with `sys.version` — `uv python list` offers 3.12.13 but has not installed it. |
| ruff | 0.16.4 | 2026-08-25 | 0 | Lint + format, one tool. Resolved with `uv pip compile`. Dev dependency. |
| pytest | 9.1.1 | 2026-08-25 | 0 | Test runner behind `./m check`. Resolved with `uv pip compile`. Dev dependency. |
```

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded
and nothing was trained.

Commit:

```text
day 000: Toolchain, skeleton and the ./m driver — closes no IDs
```
