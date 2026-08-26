# 📅 days/ — the 162 written days

**Never done this before?** Start at Day 0.
**Already set up?** Run `./m status`; it tells you where you are.
**Want the map?** [`../docs/CURRICULUM_INDEX.md`](../docs/CURRICULUM_INDEX.md).
**Want progress?** [`../docs/TRACKER.md`](../docs/TRACKER.md).

---

## The eight rules these documents follow

1. **All the code lives in the documents. None of it is pre-written in the repo.**
   You type it, you own it. There is no `akshara/*.py` waiting for you — every line you will ever
   run is written out in a lesson, and you create the file yourself. You cannot debug an attention
   mask on Day 88 that you never typed on Day 31.

2. **Every code block is followed by a line-by-line walkthrough.**
   Not a summary — an explanation of what each line does and *why it is that line and not another*.
   If a line is unexplained anywhere in these documents, that is a bug in the document.

3. **Every tensor has a shape, twice.**
   Once as a trailing comment on the line that changes it (`# (B, T, C)`), and once in the part's
   `## Shapes` table with what each axis *means*. More transformer bugs are shape bugs than
   algorithm bugs, and a document that leaves you to infer an axis has taught you something you
   cannot debug.

4. **Every command is given in full.**
   `mkdir -p`, `uv add package==1.2.3`, the run command, the check command. You should never have to
   infer "and now presumably I create a folder".

5. **One idea per document.** *(Principle 16)*
   A day is not one long page. It is a short hub plus one document per subtopic, in `parts/`. If a
   document needs the word "also" to introduce its second half, it should have been two documents.

6. **There are no clocks here.** *(Principle 17)*
   You will not find "this takes 90 minutes" or an "estimated hours" field anywhere, because it
   would be a lie and because it invites trimming. **A day is a unit of subject, not a unit of
   time.** Day 93 might take you one evening or four; both are the day being done properly. If a
   subject needs twenty-four documents, it gets twenty-four. `./m done N` is gated on a ticked
   checklist and green checks, never on hours elapsed.
   *(A measured duration — "the run took 43 minutes on a T4" — is data, not a clock. That stays.)*

7. **Zero prior knowledge in, production knowledge out.** *(Principle 18)*
   Every document starts where someone who has never heard of the idea can stand — the jargon is
   defined the first time it appears, including jargon from earlier days, with a link back. And no
   document stops at the toy example: each ends with **In production** — what a research engineer
   writes instead of the teaching version, what breaks at scale, the comment a senior reviewer
   leaves, and the question an interviewer asks to find out whether you have really used it.

---

## What's in a day folder

```
days/day-NNN-<slug>/   # the number is the identity; the slug says what the day teaches
├── LESSON.md      # the hub — the story, the map of parts, setup, build brief, eval, budget
├── CHECKLIST.md   # the definition of done. `./m done NNN` refuses to commit until it's ticked.
├── parts/         # THE TEACHING — one document per subtopic
│   ├── 01-<slug>/ # section 1 — its own folder, named for what the section is about
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   └── 02-<slug>/ # section 2
│       └── 2.1-<slug>.md
└── lab/           # your own scratch code; `./m scaffold NNN` makes it
```

**Read the hub first, then the parts in numerical order.** The hub's §2 map is the table of
contents and tells you what each section number means for that day.

### What `1.1`, `1.2`, `2.1` mean

The number is `<section>.<subtopic>`, both scoped to that day.

- The **section** (before the dot) groups subtopics that share one mental model — usually one
  curriculum ID, one forward-pass stage, or one phase of a mechanism.
- The **subtopic** (after the dot) is the reading order inside that section.

So on a two-ID day, `1.x` is the first ID, `2.x` is the second, and a `3.x` is usually the synthesis
— the trap you can only see once both ideas are true at the same time. Whatever the grouping is,
the hub says so explicitly.

**Each section gets its own folder**, numbered with two digits and then named for what it covers:
`parts/01-soft-lookup/`, `parts/03-causal-mask/`. So the third subtopic of section 2 is
`parts/02-<slug>/2.3-<slug>.md`.

**Day numbers are three digits** — `day-007-…`, `day-143-…` — so the folders sort correctly. The
plan runs to 161.

**The number is the identity; the slug is a label on it.** `./m`, `scripts/depth_check.py`,
`scripts/tracker.py` and `scripts/trace.py` all find a day by its number and accept whatever slug
follows, so `./m start 43` works no matter what `day-043-…` is called.

### The shape of every part document

Eleven sections, always in this order. They trace one path: from a reader who has never heard of the
idea, to one who could defend it in a design review. This is the depth contract (plan §25.4), and
`./m depth NNN` fails the day if any unconditional one is missing.

| Section | What it's for |
| --- | --- |
| **frontmatter** | `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next` — machine-read. No duration field; see rule 6. |
| **One-line answer** | the whole claim in one sentence, before anything else |
| **The story** | a concrete scene — a person, a machine, a failure, a decision — with no jargon at all. The hook the definition hangs on. |
| **The idea in plain language** | the concept from zero, every term defined the first time it appears, no code |
| **Why Akshara needs it** | the concrete later day that breaks without this — never "this is important" |
| **The mechanism** | how it actually works: the code, the derivation, or the diagram |
| **Shapes** *(when there are tensors)* | one row per tensor: symbolic shape, concrete numbers, what each axis means |
| **Line by line** *(when there is code)* | every non-obvious token, and why it is that line and not another |
| **When it breaks** | the real error text, verbatim — and for this field, the *silent* failure too: what wrong-but-running looks like, and the check that catches it |
| **In production** | what changes in a real system: scale, memory, throughput, the review comment, the interview question |
| **Check yourself** | one command that prints a **number**, and one question to answer out loud |

### The `level` ladder

Every part declares one, and a day climbs:

| `level` | You, at the end of that part |
| --- | --- |
| `foundation` | Know what it *is*, and could define it without using the word itself. |
| `working` | Can implement or use it on your own problem, and recognise its error messages on sight. |
| `production` | Know what changes in a real system, and can defend the choice with arithmetic. |

---

## The symbols

Used consistently across all 162 days. A part that introduces a new one defines it.

| Symbol | Means |
| --- | --- |
| `B` | batch size |
| `T` | time / sequence length (number of tokens) |
| `C` | channels — the model dimension, `d_model` |
| `H` | number of attention heads |
| `hs` | head size, usually `C / H` |
| `V` | vocabulary size |

| Marker | Means |
| --- | --- |
| 💥 | a deliberate failure — the part where you break it on purpose |
| 🅿️ | parked: awareness-level, interview-ready, deliberately not built. **The arithmetic is still worked** — you must be able to size the thing you did not run. |
| 🔍 | compare: the hand-rolled version already exists, and today you open the library and diff your understanding against theirs |
| `TODO(me)` | yours to solve. The document never does the reps for you. |

---

## Compute: what you actually need

Every day states its tier in the hub's frontmatter (`compute_tier`) and §6 (plan §4).

| Tier | Hardware | Which days |
| --- | --- | --- |
| **T0** | Your laptop CPU. No GPU. | The overwhelming majority — every hand-rolled implementation. |
| **T1** | One free Colab or Kaggle session (T4-class). | The pretraining run, the LoRA fine-tune, the DPO run, the diffusion training, the VLM projector. |
| **T2** 🅿️ | Cannot be done at $0. | Read, with the arithmetic worked. Never a blocker. |

**No day requires a payment.** If a T1 session gets revoked mid-run, that is normal, not an
incident — every T1 day checkpoints and resumes (TRAIN-15, TRAIN-16), which is why those are taught
before the first real run rather than after the first lost one.

---

## The shell

Day documents are written for **Git Bash** on Windows. If you are in PowerShell:

| Git Bash | PowerShell |
| --- | --- |
| `mkdir -p a/b` | `New-Item -ItemType Directory -Force a/b` |
| `touch f.py` | `if (-not (Test-Path f.py)) { New-Item -ItemType File f.py }` |
| `cat f.py` | `Get-Content f.py` |
| `export VAR=x` | `$env:VAR = 'x'` |
| `./m check` | `bash ./m check` |
| `cmd1 && cmd2` | `cmd1; if ($?) { cmd2 }` |

---

## The daily ritual

```bash
./m status          # where am I?
./m start N         # open day N's hub, list its parts
./m scaffold N      # make days/day-NNN-<slug>/lab/ for your own code
# ... read the parts in order, type the code, solve the TODO(me)s ...
./m check           # ruff + format + CPU-only tests + depth contract + traceability
./m done N          # refuses on an unticked checklist or a staged checkpoint, then commits
```

`./m done N` will refuse to commit if a weight file or dataset is staged. That is Principle 9
doing its job: **the repo holds what reproduces a model, never the model.**
