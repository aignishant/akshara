---
day: 1
phase: 1
phase_name: "The ground: tensors, gradients, information"
title: "Bootstrap and the map"
ids: ["OPS-01", "OPS-02", "OPS-03", "OPS-04"]
principles: [1, 2, 6, 8, 9, 10, 13, 15, 16, 17, 18, 19]
kind: setup
plan_version: "v1.2.0"
parts: 14
compute_tier: T0
generated: "2026-08-26"
status: written
lab_scaffolded: false
commit: ""
---

# Day 1 — Bootstrap and the map

> **Yesterday (Day 0):** the machine. One tool owning the environment, a repository shaped like the
> work, a `.gitignore` written before there was anything to protect, a driver that refuses — and four
> guards broken on purpose to prove they were alive.
> **Today:** that generic Python repository becomes **Akshara's memory**. The layout acquires rules
> about what it refuses to hold, a Hugging Face token gets exactly one home, nine ledgers start
> recording what cannot be recovered later, and the free-compute accounts are set up with their real
> costs measured rather than assumed.
> **Tomorrow (Day 2):** the first actual mathematics — tensors, shapes, broadcasting, and the matmul
> that is ninety per cent of everything you will run (MATH-01..03).

---

## §1 Where we are

Yesterday you built a repository that any Python project could have. Today it becomes this one.

Think about what actually survives a project. Not the conversation where the hard decision got made —
that is gone the moment the window closes. Not your memory of why a constant is 8 rather than 16;
that lasts a few weeks at best. What survives is exactly what somebody wrote into a file and
committed, and nothing else. A project's real memory is not the sum of what its authors know. It is
the much smaller set of things they bothered to write down.

That gap matters more here than in ordinary software, for a reason specific to what you are about to
build. A piece of code can be re-read to work out what it does. **A trained model cannot.** It is a
file of numbers that does not record the corpus it saw, the seed it used, the schedule it followed or
the machine it ran on — and none of that is recoverable afterwards from the model itself. On Day 67
you will spend an entire free GPU session producing one, and six weeks later the only difference
between a result you can build on and a story you half-remember is a row of text somebody typed at
the time.

So today is about deciding, deliberately, what gets written down — and where. The layout stops being
folders and becomes a set of refusals: each directory says what would be *wrong* to put in it, which
is the only kind of rule that carries information. The token gets one home and a read-only scope,
because a credential's danger scales with the number of copies of it. Nine ledgers appear, six
written by hand and three computed, and the difference between those two kinds is a genuine skill:
anything derivable should be derived, because a fact stored twice will eventually disagree with
itself.

And the last section is about the machine you do not own. Free compute is not free of cost — it is
free of *money*, and paid for in revocability, opacity and exposure. A session can be reclaimed
mid-run with no warning and no traceback. Rather than discover that on Day 67, you rehearse it today:
kill a job on purpose, resume it, and check that the resumed answer is the *same* answer. A resume
path that has never been run is a resume path that does not work.

---

## §2 The map

Fourteen parts, four sections — one per curriculum ID. The day climbs
`foundation → working → production` and each section ends with something breaking.

### Section 1 — `01-repo-as-memory`: OPS-01, the repository as the thing that survives

Why the repo is the memory, what each directory refuses to hold, and where a new file goes.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 1.1 | [The repo is the memory](parts/01-repo-as-memory/1.1-the-repo-is-the-memory.md) | What is the one question that decides whether a project's knowledge will survive? | `foundation` |
| 1.2 | [The layout as an argument](parts/01-repo-as-memory/1.2-the-layout-as-argument.md) | Why does a directory carry information in proportion to what it **excludes**? | `working` |
| 1.3 | [Where a new file goes](parts/01-repo-as-memory/1.3-where-a-new-file-goes.md) | What do you do with the file that fits nowhere — and what is lost if you place it silently? | `production` |

### Section 2 — `02-secrets-and-tokens`: OPS-02, one home for a credential

The token, the loader you write rather than install, and the leak route `.gitignore` cannot see.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 2.1 | [The token in one place](parts/02-secrets-and-tokens/2.1-the-token-in-one-place.md) | Why must `.gitignore` contain `.env` *before* `.env` exists? | `foundation` |
| 2.2 | [Reading .env without a dependency](parts/02-secrets-and-tokens/2.2-reading-env-without-a-dependency.md) | Why does an existing environment variable win over the file? | `working` |
| 2.3 | [💥 The token that leaked](parts/02-secrets-and-tokens/2.3-the-token-that-leaked.md) | How does a credential reach a committed file without appearing in any line of code? | `production` |

### Section 3 — `03-the-ledgers`: OPS-03, ten records and the difference between them

What a ledger is, the one that matters most, the three that are computed, and what happens when you
edit one of those.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 3.1 | [What a ledger is for](parts/03-the-ledgers/3.1-what-a-ledger-is-for.md) | Why is a correction appended rather than applied? | `foundation` |
| 3.2 | [RUNS.md turns anecdote into result](parts/03-the-ledgers/3.2-runs-md-turns-anecdote-into-result.md) | What changes a training result that is recoverable from **neither** the checkpoint nor the code? | `production` |
| 3.3 | [The generated three](parts/03-the-ledgers/3.3-the-generated-three.md) | Which facts should never be stored — and what new failure do you accept by computing them? | `working` |
| 3.4 | [💥 Editing a generated ledger](parts/03-the-ledgers/3.4-editing-a-generated-ledger.md) | Why is correcting a generated file worse than leaving the wrong number visible? | `production` |

### Section 4 — `04-free-compute`: OPS-04, the machine you do not own

The three tiers, what the accounts really cost, the notebook discipline, and pre-emption rehearsed.

| # | Part | What it answers | Level |
| --- | --- | --- | --- |
| 4.1 | [Three tiers and what CPU proves](parts/04-free-compute/4.1-three-tiers-and-what-cpu-proves.md) | What does a laptop run prove — and what does it prove nothing about? | `foundation` |
| 4.2 | [The accounts and what they cost](parts/04-free-compute/4.2-the-accounts-and-what-they-cost.md) | Free of money — but paid for in what? | `working` |
| 4.3 | [The notebook ↔ module discipline](parts/04-free-compute/4.3-notebook-module-discipline.md) | Why is "it ran in my session" not evidence that a notebook works? | `production` |
| 4.4 | [💥 The session that vanished](parts/04-free-compute/4.4-the-session-that-vanished.md) | Why is "the resume ran successfully" not evidence that the resume is correct? | `production` |

---

## §3 Setup — run this

No packages are installed today except one dev tool. Everything else arrives on the day it is first
used, after its hand-rolled version exists (Principle 3).

```bash
# 1 — the secret rule, BEFORE the file it protects (part 2.1)
printf '\n# Secrets (OPS-02)\n.env\n.env.*\n!.env.example\n*.key\n*.pem\n' >> .gitignore
git check-ignore -v .env; echo "ignored? exit=$?"

# 2 — the template, then your real file
#    create a READ token first at https://huggingface.co/settings/tokens
cp .env.example .env     # then edit .env and paste the token into HF_TOKEN=

# 3 — notebook output stripping (part 2.3). Look the version up live first.
curl -s https://pypi.org/pypi/nbstripout/json | python -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"
uv add --dev nbstripout==<what your lookup printed>
uv run nbstripout --install --attributes .gitattributes

# 4 — the directory refusals (part 1.2)
#    write akshara/README.md and scripts/README.md as the part shows

# 5 — regenerate the computed ledgers and read them
./m trace
./m tracker
head -12 docs/TRACEABILITY.md
```

Accounts to create, all free, none requiring payment details (part 4.2): **Hugging Face** (read
token), **Google Colab**, **Kaggle**. Then run the measurement cell from part 4.2 in a GPU notebook
and record what it printed — Day 66 sizes Akshara against those numbers.

---

## §4 Build brief

| File | From | Contains |
| --- | --- | --- |
| `.env` | [2.1](parts/02-secrets-and-tokens/2.1-the-token-in-one-place.md) | `HF_TOKEN`, the two `AKSHARA_*_DIR` paths. **Never committed.** |
| `akshara/config.py` | [2.2](parts/02-secrets-and-tokens/2.2-reading-env-without-a-dependency.md), [4.1](parts/04-free-compute/4.1-three-tiers-and-what-cpu-proves.md) | `load_env()` and `device()` |
| `akshara/README.md` | [1.2](parts/01-repo-as-memory/1.2-the-layout-as-argument.md) | what this package refuses to hold |
| `scripts/README.md` | [1.2](parts/01-repo-as-memory/1.2-the-layout-as-argument.md) | the dependency arrow, and why it points one way |
| `.gitattributes` | [2.3](parts/02-secrets-and-tokens/2.3-the-token-that-leaked.md) | the `nbstripout` filter, committed so it follows the repo |

```text
TODO(me): wire the credential scan from part 2.1 into `./m check`, so a token-shaped
          string in a tracked file fails the gate rather than waiting to be noticed.

TODO(me): wire the "generated ledgers are not stale" check from part 3.4 into `./m check`
          — regenerate, then fail if the committed copies differ.

TODO(me): add the `scripts/ must not import akshara` grep from part 1.2 to `./m check`.
          One line, and it is the arrow every other rule rests on.
```

---

## §5 The eval that must be able to fail

Two checks today, and both must be observed **red** before they are green.

```bash
# 1 — the notebook filter must actually strip (part 2.3)
#     build the leak demo from that part, then:
git add notebooks/leak_demo.ipynb
echo "on disk:  $(grep -c 'hf_ABCDEF' notebooks/leak_demo.ipynb)"   # expect 1
echo "in index: $(git show :notebooks/leak_demo.ipynb | grep -c 'hf_ABCDEF')"  # expect 0
git reset -q HEAD notebooks/leak_demo.ipynb; rm -f notebooks/leak_demo.ipynb

# 2 — the resume must produce the SAME answer, not just run (part 4.4)
#     both runs must print `done 465`
```

If `in index` is `1`, the filter is not installed and every notebook you commit carries whatever it
printed. If the two resume runs disagree, the resume path is losing or duplicating work.

---

## §6 Compute budget

**Tier: T0** for everything on the laptop. One optional **T1** excursion to measure the hardware.

| Resource | Today |
| --- | --- |
| GPU-minutes | **0 required.** ~2 optional, to run part 4.2's measurement cell |
| Free notebook sessions | 0 required; 1 partial if you measure |
| Network | account signup, one `nbstripout` install, the version lookup |
| Disk | negligible |

The measurement excursion is optional today and its output is **required by Day 66**, which sizes the
model against a T4's actual VRAM. Doing it now costs two GPU-minutes; doing it on Day 66 costs a
context switch in the middle of arithmetic.

---

## §7 Traps

| Trap | What you see | Where |
| --- | --- | --- |
| `.env` created before `.gitignore` covers it | one commit where it is trackable — and ignore rules never apply to tracked files | [2.1](parts/02-secrets-and-tokens/2.1-the-token-in-one-place.md) |
| `os.environ.get()` instead of `os.environ[]` | a `401` three layers away instead of a named `KeyError` | [2.2](parts/02-secrets-and-tokens/2.2-reading-env-without-a-dependency.md) |
| A `.env` loader that overwrites existing variables | the notebook's real token silently replaced by a stale file value | [2.2](parts/02-secrets-and-tokens/2.2-reading-env-without-a-dependency.md) |
| Printing a token prefix "just to check" | it is in the notebook's `outputs`, in the committed JSON | [2.3](parts/02-secrets-and-tokens/2.3-the-token-that-leaked.md) |
| Editing `TRACEABILITY.md` to fix a wrong row | the edit vanishes on the next `./m check`, and the real defect is hidden | [3.4](parts/03-the-ledgers/3.4-editing-a-generated-ledger.md) |
| Writing the `RUNS.md` row at the end of a run | pre-empted runs leave no record at all | [3.2](parts/03-the-ledgers/3.2-runs-md-turns-anecdote-into-result.md) |
| Reading a green CPU smoke run as "it will work" | proves logic; proves nothing about memory, throughput or precision | [4.1](parts/04-free-compute/4.1-three-tiers-and-what-cpu-proves.md) |
| Defining a function in a notebook cell | it shadows the imported one; the checkpoint was trained by code not in git | [4.3](parts/04-free-compute/4.3-notebook-module-discipline.md) |
| A checkpoint holding only weights | resume restarts the schedule and the data — a different model, silently | [4.4](parts/04-free-compute/4.4-the-session-that-vanished.md) |

**Named silent failure (plan §6): #4 — noise mistaken for improvement.** Today it arrives through
*record-keeping* rather than through a seed. A run with no `RUNS.md` row, or a row with one seed and
no noise band, produces a number that cannot be compared to anything — and a comparison made anyway
is a coin flip with a table behind it. Part
[3.2](parts/03-the-ledgers/3.2-runs-md-turns-anecdote-into-result.md) is the antidote and Day 119
makes it formal.

---

## §8 Verify before you code

Fetched on `2026-08-26`, not recalled (Principles 6, 7, 8):

| Source | Checked for |
| --- | --- |
| `https://huggingface.co/settings/tokens` | token scopes — that a **read** token exists and is the default choice |
| `https://pypi.org/pypi/nbstripout/json` | the current version, pinned into `pyproject.toml` and `docs/PACKAGES.md` |
| `https://git-scm.com/docs/gitattributes` | the `filter` attribute mechanism `nbstripout --install` uses |
| `https://git-scm.com/docs/gitignore` | negation with `!`, and that order matters for `!.env.example` |
| `https://docs.python.org/3/library/os.html#os.environ` | `os.environ` is a mapping; `[]` raises `KeyError`, `.get()` returns `None` |
| `nbformat` schema (v4) | that `outputs` is a per-cell array stored in the file — the basis of part 2.3 |
| `nvidia-smi --help-query-gpu` | the `--query-gpu` field names used in part 4.2's measurement cell |

---

## §9 Say it in an interview

"The thing I'd point at from that first week is the run ledger. A trained model doesn't record the
corpus, the seed, the schedule or the hardware — none of that is recoverable from the checkpoint —
so if it isn't written down at launch it's gone. I write the row before the run starts, not after,
because the runs that get pre-empted are the ones that would otherwise leave no trace, and on free
compute pre-emption is the expected case rather than an incident. The row has a column for which of
the known silent failures I ruled out and how. And I rehearsed the interruption on day one, on a
laptop, with a toy job — killed it, resumed it, and checked the resumed answer was the *same* answer,
not just that it ran. A resume path that's never been exercised is the least-tested code you have,
and it runs at the worst possible moment."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` exits `0`.

`./m done 1` will refuse while any box is unticked, an artifact is staged, or the gate is red.
Defined by understanding and green checks, **never by elapsed time** (Principle 17).

---

## §11 Ledger & commit

`docs/PROGRESS.md` — paste this row:

```text
| 1 | 2026-08-26 | OPS-01, OPS-02, OPS-03, OPS-04 | 14 | T0 | <commit sha> | ✅ |
```

`docs/PACKAGES.md` — one required row, plus two if you ran the T1 measurement. Use **your** observed
values:

```text
| nbstripout | <your lookup> | 2026-08-26 | 1 | Strips notebook outputs on the way into git. A credential or a data sample can reach a committed file through `outputs` without appearing in any cell's source (part 2.3). |
| colab-gpu (observed) | <name, memory.total, driver> | 2026-08-26 | 1 | The T1 device, measured with `nvidia-smi` rather than read from a docs page. Day 66 sizes Akshara against this number. |
| colab-host (observed) | <RAM GB, disk free GB> | 2026-08-26 | 1 | Host limits — the binding constraint on Day 64's corpus tokenization, which is CPU and disk bound. |
```

`docs/DATASETS.md`, `docs/MODELS.md`, `docs/RUNS.md` — **no rows today.** Nothing was downloaded
and nothing was trained.

Commit:

```text
day 001: Bootstrap and the map — closes OPS-01, OPS-02, OPS-03, OPS-04
```
