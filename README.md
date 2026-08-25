# 🔤 Project Akshara

**Generative AI from the byte up.** A 162-day curriculum that builds a language model end to end —
the tokenizer, the transformer, the training loop, the alignment, the quantization, the server —
and then the rest of the field around it: diffusion, multimodal, retrieval, evaluation, safety.

> **Akshara** (Sanskrit अक्षर) means two things at once: *the syllable* — the smallest indivisible
> unit of language — and *the imperishable*. Both are the point. This starts at the byte and does
> not stop until the thing you built is trained, aligned, quantized, served and evaluated.

Everything runs at **$0**, on a laptop CPU or one free Colab/Kaggle session.

---

## What this actually is

Not a reading list, and not a wrapper around somebody else's model. You write:

- a **byte-level BPE tokenizer**, trained on your own corpus — then compare it against `tiktoken`
- **attention**, multi-head, RoPE, RMSNorm, SwiGLU, the residual stream — then compare against
  `transformers`
- a **training loop** with mixed precision, gradient accumulation, checkpoint-and-resume
- a **pretrained base model**, sized by arithmetic from one free T4's VRAM
- **SFT and DPO**, with the chat-template masking bug demonstrated before it is fixed
- a **KV cache**, the sampler zoo, and constrained JSON decoding — then compare against `vLLM`
- **LoRA and 4-bit quantization**, with the accuracy damage measured rather than assumed
- a **tiny diffusion model** with classifier-free guidance
- a **vision–language projector**, a **RAG pipeline**, an **eval suite**, and a **served endpoint**

Every mechanism is hand-rolled first and the library opened second, so that `transformers`,
`peft` and `diffusers` end up as conveniences you can read rather than mysteries you import.

---

## Start here

| You want | Read |
| --- | --- |
| The contract — what gets taught, in what order, and why | [`docs/00_MASTER_PLAN.md`](docs/00_MASTER_PLAN.md) |
| How to read a day | [`days/README.md`](days/README.md) |
| Where the project is right now | [`docs/PROGRESS.md`](docs/PROGRESS.md) — the last row |
| What's written, and how deeply | [`docs/TRACKER.md`](docs/TRACKER.md) |
| "Where do I learn `ARCH-28`?" | [`docs/CURRICULUM_INDEX.md`](docs/CURRICULUM_INDEX.md) |

```bash
uv sync            # set up the environment
./m status         # where am I?
./m start 0        # open Day 0's hub and list its parts
```

---

## The shape of it

**17 curricula · 309 concept IDs · 162 days · 22 phases.**

| Book | Curricula |
| --- | --- |
| **I — Ground** | Foundations (`MATH`) · Tokenization (`TOK`) · Representation (`EMB`) |
| **II — The Machine** | Architecture (`ARCH`) · Training (`TRAIN`) · Scaling (`SCALE`) |
| **III — The Runtime** | Inference (`INFER`) · Efficiency (`EFF`) · Serving (`SERVE`) · Operations (`OPS`) |
| **IV — The Behaviour** | Post-training (`POST`) · Reasoning (`REASON`) · Retrieval (`RAG`) · Evaluation (`EVAL`) · Safety (`SAFE`) |
| **V — Beyond text** | Multimodal (`MM`) · Generative families (`GEN`) |

**Nobody chose 162.** It is what came out of splitting 309 concepts at idea boundaries until each
day held one coherent unit of subject. A round number would have been a warning sign: a plan that
commits to "100 days" has to compress attention into two of them, and the compression always lands
on the same victim — the explanation.

**A day is a unit of subject, not a unit of time.** There is no time estimate anywhere in this
repo, on purpose. Day 93 might take one evening or four; both are the day being done properly.

---

## The rules that shape every document

The full set is [plan §2](docs/00_MASTER_PLAN.md) (twenty-one principles). The ones you will feel:

- **Build first, compare after.** A library you have re-implemented is a convenience. One you have
  only imported is a mystery with a nice API.
- **Never invent a number.** Every empirical claim is either *measured here* — with hardware, seed
  and date — or *cited* with an arXiv id and section. "LoRA rank is typically 8–64" is a rumour with
  a hedge in front of it.
- **Seeds, configs and code are committed. Weights and data never are.** `./m done` refuses to
  commit a staged checkpoint. The repo holds what *reproduces* a model, never the model.
- **Overfit one batch before you train anything.** A model that cannot memorise sixteen examples has
  a bug, not a hyperparameter problem.
- **Shapes are stated, never inferred.** More transformer bugs are shape bugs than algorithm bugs.
- **Fail honestly.** A run that diverged is recorded as diverged, in `docs/RUNS.md`, with its seed.

### 📄 Papers are taught, not cited

**130 papers across 88 of the 162 days**, each getting its **own part** — not a footnote. You get the
world before the paper, its equation read symbol by symbol, what its evidence does *and does not*
support, and what later work corrected.

And each paper part contains **the smallest end-to-end runnable project that implements that paper
and nothing else** — one command, on your CPU, printing a result, with the **A/B** that switches the
paper's idea off. Being able to strip an idea down to the smallest thing that still demonstrates it
is the proof you understood what the paper actually added. It is *build first, compare after*
applied to the literature instead of to libraries.

This is the antidote to how this field actually misleads itself: half-remembered claims detached
from their conditions. *"Temperature 0.7 is best." "Twenty tokens per parameter." "LoRA rank 16 is
standard."* Every one is a real result, from a real paper, measured under conditions nobody
restates.

### 💥 The five silent failures

Ordinary software fails loudly. Generative systems fail *quietly* — they train, they run, they emit
fluent plausible output, and they are wrong. The whole curriculum is arranged around catching these:

| # | Trap | What you see |
| --- | --- | --- |
| 1 | **Contamination** | Brilliant benchmark scores — from a test set that was in your training corpus |
| 2 | **Tokenizer / template mismatch** | A fine-tune that is subtly worse, with nothing in the logs |
| 3 | **The loss counted padding** | Loss goes down, generations are garbage |
| 4 | **Noise mistaken for improvement** | Version B beats A by 1.5 points — inside the seed noise |
| 5 | **Evaluating on the format you trained on** | A huge win that measured format compliance, not capability |

Every day that touches one names it, and says how you would detect it.

---

## The driver

`make` is not used. `./m` is the driver.

```bash
./m status         # one line: how many days written / complete
./m start N        # point at day N's hub and list its parts
./m parts N        # list day N's sub-topic documents
./m depth [N]      # check against plan §25, the depth contract
./m trace          # regenerate TRACEABILITY.md + CURRICULUM_INDEX.md from the hubs vs plan §24
./m tracker        # regenerate TRACKER.md
./m scaffold N     # create days/day-NNN-<slug>/lab/
./m check          # ruff + format + CPU-only pytest + depth contract + traceability
./m done N         # refuses on an unticked checklist or a staged checkpoint, then commits
```

`./m check` is the whole-project gate and must be green before any day is finished. The depth check
is not advisory: it fails a day for a missing `Shapes` table, an unexplained code block, a numbering
gap, a paper part with no runnable project, a hub that carries teaching, or a smuggled-in time
estimate.

---

## Layout

```
akshara/        the model package — you write every line, from the day documents
configs/        every run's config, committed. Weights are not.
days/           the teaching: one folder per day, hub + parts/ (+ papers/ demos)
docs/           the plan, the six ledgers, the generated ledgers, the ADRs
scripts/        depth_check.py · trace.py · tracker.py
tests/          CPU-only, deterministic, offline
notebooks/      Colab/Kaggle notebooks, output stripped before commit
```

Nothing under `akshara/` or `tests/` is pre-written. Every line of it is printed in a day document
and typed by you — because you cannot debug an attention mask on Day 88 that you never typed on
Day 31.

---

## Ledgers

Seven are written by hand and append-only; three are generated. Do not confuse them — editing a
generated one just means the next `./m check` overwrites you.

| Hand-written | What it records |
| --- | --- |
| `PROGRESS.md` | one row per completed day — the last row is where we are |
| `PACKAGES.md` | every install: package, version, date, day, why |
| `DATASETS.md` | every dataset **before** download: revision SHA, licence, decontamination status |
| `MODELS.md` | every checkpoint **before** loading: revision SHA, licence, safetensors-only |
| `RUNS.md` | every training run: seed, config hash, hardware, losses, outcome — **including failures** |
| `PAPERS.md` | every paper taught: identifier resolved live, the part that teaches it, its demo path |
| `CHANGELOG_PLAN.md` | every amendment to the plan |

`RUNS.md` is the one an ordinary project does not have, and the one that will save you. Six weeks
after a training run, the only difference between a result and an anecdote is a row containing a
seed, a config hash and a hardware line.
