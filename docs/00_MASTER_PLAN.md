---
plan: akshara
version: "v1.1.0"
curricula: 17
ids: 309
days: 162
phases: 22
doc_architecture: "hub + parts/ (see §25)"
paper_architecture: "one part per paper, in the day's own paper section (see §24.3, §25.10)"
day_count_is: "derived, not chosen (see §24.0)"
created: "2026-08-25"
amended: "2026-08-25"
---

# 🔤 MASTER PLAN v1.1.0 — Project **Akshara**
## Generative AI from the byte up — tokenizers · transformers · training · alignment · diffusion · serving

> **Akshara** (Sanskrit अक्षर) means two things at once: *the syllable* — the smallest indivisible
> unit of language — and *the imperishable*. Both are the point. This curriculum starts at the byte,
> builds the unit, and does not stop until the thing you built is trained, aligned, quantized,
> served and evaluated.
>
> 📌 **Purpose:** the single source of truth. Every later document points back here.
>
> **You build the model.** Not a wrapper around somebody else's model — the tokenizer, the attention,
> the block, the training loop, the sampler, the KV cache, the LoRA, the diffusion denoiser. Each one
> hand-rolled first and *then* compared against the library everyone uses, so that
> `transformers`, `tokenizers`, `peft` and `diffusers` are conveniences you can read, never
> mysteries you import.
>
> ⚠️ **Zero budget is a hard constraint, not an aspiration.** Every day in this plan runs on a
> laptop CPU or one free Colab/Kaggle T4 session. If a day cannot be done at $0 it is redesigned
> until it can, or it is explicitly parked 🅿️ as reading. See §4.

---

## 📑 Table of Contents

| §  | Section |
| --- | --- |
| 1  | 🎬 The Vision — one model, seventeen threads |
| 2  | 🧭 Core Principles — rules we never break |
| 3  | 🏗️ The Artifact — what Akshara actually is |
| 4  | 💸 Compute & Budget Policy — the $0 constraint |
| 5  | ⚙️ The Stack — versions, pins, verification |
| 6  | 💥 The Five Silent Failures — how generative work goes wrong quietly |
| 7  | 🧶 The Seventeen Curricula & the ID scheme |
| 8  | 📐 Curriculum MATH — Foundations (MATH-01..16) |
| 9  | 🔤 Curriculum TOK — Tokenization (TOK-01..20) |
| 10 | 🧮 Curriculum EMB — Representation (EMB-01..10) |
| 11 | 🏛️ Curriculum ARCH — Architecture (ARCH-01..40) |
| 12 | 🔁 Curriculum TRAIN — Training (TRAIN-01..28) |
| 13 | 📈 Curriculum SCALE — Scaling & Pretraining (SCALE-01..10) |
| 14 | 🎲 Curriculum INFER — Decoding & Inference (INFER-01..20) |
| 15 | 🗜️ Curriculum EFF — Efficiency (EFF-01..18) |
| 16 | 🎯 Curriculum POST — Post-training & Alignment (POST-01..20) |
| 17 | 🧠 Curriculum REASON — Reasoning & Prompting (REASON-01..14) |
| 18 | 📚 Curriculum RAG — Knowledge & Retrieval (RAG-01..14) |
| 19 | 📊 Curriculum EVAL — Evaluation (EVAL-01..16) |
| 20 | 🖼️ Curriculum MM — Multimodal (MM-01..16) |
| 21 | 🌫️ Curriculum GEN — Other Generative Families (GEN-01..21) |
| 22 | 🛡️ Curriculum SAFE — Safety, Security & Ethics (SAFE-01..20) |
| 23 | 🚀 Curriculum SERVE — Serving & Systems (SERVE-01..16) · OPS-01..10 |
| 24 | 🗓️ The Day Map (day → IDs closed) · **§24.3 The Paper Roster** |
| 25 | 📐 The Depth Contract — how a day is written · **§25.10 Paper parts** |
| 26 | 🚦 Phase Gates & the Freshness Check |
| 27 | 📒 Ledgers & Traceability |
| 28 | ✍️ The Style Guide |

---

## 1 · 🎬 The Vision — one model, seventeen threads

By the final day you will have **built a language model from the byte up, trained it, taught it to
follow instructions, aligned it to preferences, quantized it, served it behind an API, and
evaluated it honestly** — and you will be able to defend every number in it. Alongside it you will
have built a tiny diffusion model, a vision–language projector, and a retrieval pipeline, because
"generative AI" is not one architecture and a curriculum that pretends otherwise is lying.

Three commitments shape everything:

1. **One artifact, not toy demos.** Every concept lands as a change to Akshara. The tokenizer you
   write on Day 13 is the tokenizer that trains the model on Day 67 and the one that breaks the
   fine-tune on Day 88 if you get the chat template wrong. Nothing is learned in a vacuum.
2. **The repo is the memory, not the chat.** Ledgers plus day documents mean any capable CLI agent
   (Claude Code today, any other tomorrow) can pick up exactly where the last one stopped — and
   more importantly, **every training run is reproducible from a committed config and a seed.**
3. **Measured beats quoted.** A number you read in a paper is a citation. A number you produced on
   your own machine, with a seed and a hardware line, is a result. This curriculum is built out of
   the second kind (Principle 8).

### 1.1 Stated non-goals (decisions, not blind spots)

| Excluded | Why |
| --- | --- |
| Training a frontier-scale model | Physically impossible at $0. §13 teaches the scaling laws that let you *reason* about frontier runs without doing one. |
| Agent frameworks, MCP, multi-agent orchestration | A different discipline with its own curriculum. Akshara stops at "the model, served and evaluated"; what you build *on top* of a model is elsewhere. |
| CUDA kernel authoring / Triton | ARCH and EFF teach what FlashAttention *does* and why it is IO-bound. Writing the kernel is a systems course. 🅿️ awareness only. |
| Classical ML (trees, SVMs, feature engineering) | Assumed unnecessary. Everything needed is built in §8, from scratch. |
| MLOps platform engineering (Kubeflow, feature stores) | SERVE covers serving a model honestly. Platform operations is its own field. |
| Paid APIs, paid GPUs, subscriptions | The $0 constraint (§4) is absolute. |

---

## 2 · 🧭 Core Principles — rules we never break

1. **Doc-first.** The day document is written before any code; the code follows the doc.
2. **One day, one commit.** Traceable, append-only history.
3. **Build first, compare after.** Hand-roll the mechanism once — BPE, attention, the training loop,
   the KV cache, LoRA, the denoiser — *then* open the library that does it, and diff your
   understanding against theirs. A library you have re-implemented is a convenience. A library you
   have only imported is a mystery with a nice API.
4. **Every concept is load-bearing.** If removing it would not change Akshara or change how you
   would defend Akshara, it does not get a day.
5. **Simple language plus a concrete example, always.** If a concept cannot be explained simply with
   an example, it is not understood yet (§28 enforces this).
6. **Never invent a version.** Package versions, model revisions, dataset revisions: looked up live,
   or a `TODO` containing **the exact lookup command**. Every pin gets a dated row in
   `docs/PACKAGES.md`, `docs/MODELS.md` or `docs/DATASETS.md`.
7. **Never invent an API.** Every library symbol is verified against that library's own docs or
   source **for the version actually pinned**, on the day it is used, and the document names what
   was checked. Library APIs churn; a tutorial from eighteen months ago is a hazard.
8. **Never invent a number.** Every empirical claim carries its provenance: either *"measured here,
   on `<hardware>`, seed `<n>`, `<date>`"* or *"reported in arXiv:XXXX.XXXXX §N"*. A benchmark
   number recalled from memory is a rumour, and rumours are how this field misleads itself.
9. **Seeds, configs and code are committed. Weights and data never are.** Every run is reproducible
   from what is in git plus a documented download. `docs/RUNS.md` is the run ledger; a run without a
   seed, a config hash and a hardware line did not happen.
10. **Fail honestly.** Errors surface, are logged, and are never papered over. A training run that
    diverged is reported as diverged. A quantization that cost four points of accuracy says so.
    This applies to you as much as to the code.
11. **Evals are tests.** Every day ends with at least one check that can go RED.
12. **Overfit one batch before you train anything.** A model that cannot memorise sixteen examples
    has a bug, not a hyperparameter problem. This ritual is Day 60 and every day after it.
13. **Blast radius before capability.** Every new power — code execution, a downloaded checkpoint, a
    scraped corpus, a served endpoint — arrives together with its containment story. **Never load a
    pickle you did not create**; safetensors or nothing (SAFE-11).
14. **If reality changes, the plan is amended first.** A library's breaking release, a dataset
    losing its licence, a free tier closing → versioned addendum + `docs/CHANGELOG_PLAN.md` → *then*
    code. Never silently adapt; stop and say so.
15. **Zero budget is a feature.** Memory math, quantization, LoRA, gradient checkpointing and
    sequence packing are the curriculum, not obstacles to it (§4). A researcher with eight GPUs
    never learns the memory equation. You will.
16. **Depth over density.** A day is a hub plus one document per subtopic (§25), never one long
    page. A wall of text is not depth — it is depth's disguise.
17. **No clocks.** A day is a unit of subject, not a unit of time. Never write a time estimate, a
    duration, an "estimated hours" field or a suggested pace — anywhere: frontmatter, prose or
    checklist. A topic is finished when it is understood, however many sittings that takes.
    **Never trim an explanation because a day is getting long; split it into another part instead.**
18. **Assume no prior knowledge, finish at production.** Open where someone who has never met the
    idea can stand, define every term on first use — *including terms from earlier days, with a link
    back* — and carry it through to the real-system version: what changes at scale, what a research
    engineer writes instead of the teaching version, what a reviewer says, what an interviewer
    probes. Basics and advanced technique are the same document, in that order.
19. **The day count is derived, not chosen.** 162 days is an *output* of decomposing 309 concepts
    into idea-sized units — not a target anyone picked, and not a schedule. When content demands a
    day be split, it is split by ADR and the count changes. **A round number would have been a
    warning sign** (§24.0).
20. **Shapes are stated, never inferred.** Any part that introduces or transforms a tensor carries a
    shape table (§25.4). More transformer bugs are shape bugs than are algorithm bugs, and a
    document that leaves the reader to guess `(B, T, C)` has taught them nothing they can debug.
21. **A paper the field rests on is taught, not cited.** Where a day's concept comes from a specific
    paper, that paper gets **its own part** — a full teaching document under the same contract as
    every other part, in the day's own paper section (§24.3, §25.10). A citation in a footnote tells
    the reader the idea has a source. A part tells them what the world looked like before it, what
    it actually claimed, what evidence it offered, what later work corrected, and what survived into
    the systems they will work on. **Naming a paper and moving on is the citation equivalent of an
    unexplained line of code.**

> Principles 8, 9, 12, 19, 20 and 21 are the ones this curriculum adds to ordinary engineering
> discipline, because generative work fails *quietly* (§6). They are made concrete by **§25, the
> depth contract**, and enforced mechanically by `scripts/depth_check.py` (`./m depth N`).

---

## 3 · 🏗️ The Artifact — what Akshara actually is

**Akshara is a small decoder-only language model, built end to end, plus the things you must build
around a model to claim you understand one.**

What exists when the plan is finished:

- **A tokenizer you wrote** — byte-level BPE, trained on your own corpus, with special tokens and a
  chat template, benchmarked against `tiktoken` and `tokenizers` and understood where it differs.
- **A transformer you wrote** — attention, multi-head, RoPE, RMSNorm, SwiGLU, the residual stream;
  a `from_pretrained`-free implementation whose every parameter you can count by hand.
- **A pretrained base model** — trained inside one free T4 session on a curated, deduplicated,
  decontaminated corpus, with a loss curve you can defend and a scaling-law argument for its size.
- **An instruction-tuned model** — SFT with correct chat-template masking, then preference-aligned
  with DPO, with the alignment tax measured rather than assumed.
- **An inference stack you wrote** — the sampler zoo, a KV cache, constrained JSON decoding,
  streaming — then compared honestly against `vLLM` and `llama.cpp`.
- **A quantized model** — 4-bit, with the accuracy damage *measured*, running on CPU.
- **An eval suite** — perplexity, task evals, an LLM judge with its biases characterised, a
  regression gate in CI.
- **A retrieval pipeline** — embeddings, chunking, hybrid search, a reranker, and an honest answer
  to "should this have been RAG at all?"
- **A tiny diffusion model** — forward process, denoiser, DDIM sampler, classifier-free guidance,
  trained on your own machine, because generative AI is not only autoregressive.
- **A vision–language projector** — CLIP-style contrastive understanding and a LLaVA-shaped bridge
  into Akshara, because the modality boundary is where most production systems actually live.
- **A served endpoint** — streaming HTTP, prefix caching, latency percentiles, cost per request,
  in a container.
- **A model card** — what it was trained on, what it cannot do, what it might leak, who should not
  use it. Written because SAFE-18 requires it, not because a form asked.

**Repo layout (established Day 0, grown daily):**

```
genai/
├── m                       # the driver — ./m check | depth | start | done   (Day 0)
├── Makefile                # a two-line shim so `make check` still reaches ./m check
├── CLAUDE.md               # standing instructions for the driver agent       (Day 0)
├── README.md               # what this is, and how a stranger runs it
├── .env                    # tokens (never committed)     .gitignore          (Day 0)
├── pyproject.toml          # uv-managed; every pin dated in docs/PACKAGES.md
├── uv.lock                 # the exact transitive tree; committed
│
├── days/                   # 📚 THE TEACHING — one folder per day
│   ├── README.md           #    how to read a day
│   └── day-NNN-<slug>/     #    the number is the identity, the slug says what it teaches
│       ├── LESSON.md       #    the hub: story, part map, setup, build brief, eval, budget
│       ├── CHECKLIST.md    #    the definition of done; ./m done NNN refuses until ticked
│       ├── parts/          #    one document per subtopic — the actual teaching
│       │   ├── 01-<slug>/1.1-<slug>.md …
│       │   └── 02-<slug>/2.1-<slug>.md …
│       └── lab/            #    the learner's own scratch code for that day
│
├── akshara/                # the model package — you write every line, from the docs
│   ├── tokenizer/          #   BPE, trained vocab, chat template
│   ├── model/              #   attention, blocks, the GPT
│   ├── train/              #   loop, data, schedules, checkpoints
│   ├── infer/              #   samplers, KV cache, constrained decoding
│   ├── eval/               #   metrics, harness, judge
│   └── serve/              #   the HTTP surface
├── configs/                # every run's config, committed. Weights are not.
├── scripts/                # repo tooling: depth_check.py · tracker.py · trace.py
├── tests/                  # pytest; deterministic, CPU-only, no network
├── notebooks/              # Colab/Kaggle notebooks, stripped of output before commit
└── docs/
    ├── 00_MASTER_PLAN.md          # this file
    ├── CURRICULUM_INDEX.md        # generated: ID → day
    ├── TRACKER.md · TRACEABILITY.md          # generated
    ├── PROGRESS.md · PACKAGES.md · DATASETS.md · MODELS.md · RUNS.md · CHANGELOG_PLAN.md
    └── adr/                       # architecture decision records
```

> ⚠️ **Nothing under `akshara/` or `tests/` is pre-written.** Every line is printed in a day
> document and typed by the learner (`days/README.md`, rule 1). You cannot debug an attention mask
> on Day 88 that you never typed on Day 31.
>
> ⚠️ **`.gitignore` blocks `*.safetensors`, `*.gguf`, `*.bin`, `*.pt`, `data/`, `checkpoints/`.**
> Principle 9: the repo holds what *reproduces* a model, never the model. A 400MB checkpoint in git
> history is unremovable and makes the repo unclonable.

---

## 4 · 💸 Compute & Budget Policy — the $0 constraint

**The rule: no day in this plan may require a payment, a billing account, or hardware the learner
does not have.** Everything runs on one of three tiers.

| Tier | What it is | What it runs |
| --- | --- | --- |
| **T0 — laptop CPU** | The default. No GPU assumed. | Every hand-rolled implementation: BPE, autograd, attention, the block, samplers, KV cache, quantization arithmetic, retrieval, evaluation, serving. The overwhelming majority of days. |
| **T1 — free notebook GPU** | One free Colab or Kaggle session (T4-class, ~16GB, time-limited, pre-emptible). | The pretraining run, the LoRA fine-tune, the DPO run, the diffusion training, the VLM projector. |
| **T2 — parked 🅿️** | Cannot be done at $0. | Frontier-scale pretraining, multi-node FSDP, full-parameter 7B fine-tunes, PPO at scale. Taught as reading, with the arithmetic worked so you can size one on paper. |

The rules that follow from it:

- **Every T1 day is designed to survive a disconnect.** Checkpoint-and-resume (TRAIN-15, TRAIN-16)
  is taught *before* the first real run, not after the first lost one.
- **Model sizes are chosen by the memory equation** (EFF-01), not by ambition. Akshara's parameter
  count is derived on Day 66 from the T4's actual VRAM, in public, with the arithmetic shown.
- **Every dataset must be freely licensed** and downloadable without payment. Licence, revision and
  size go in `docs/DATASETS.md` **before** the download.
- **No hosted inference API is a required dependency.** Where a day benefits from comparing against
  a large hosted model, that comparison is 🅿️ optional and its absence never blocks the day.
- **Quota is the currency.** Free notebook GPUs are metered in session-hours and can be revoked
  mid-run. Budgets in this plan are denominated in **GPU-minutes and session count**, not dollars.
  A day's hub states its budget; `0` is an answer and must be stated.
- **Never write code that silently requires a GPU.** Every training script runs on CPU at a toy
  scale, and the day says what the toy scale proves and what it does not.

---

## 5 · ⚙️ The Stack — versions, pins, verification

- **Language:** Python **3.12** (`uv`-managed). Exact `==` pins in `pyproject.toml`; `uv.lock`
  committed; a dated row in `docs/PACKAGES.md` for every install.
- **Numerics:** `numpy` first, then `torch`. NumPy is used deliberately for the days where the point
  is that *you* are doing the arithmetic (§8, the autograd engine). Torch arrives when the point
  becomes scale.
- **Libraries arrive on the day they are first used, never up front.** The comparison days
  (Principle 3) are exactly where `tokenizers`, `transformers`, `datasets`, `peft`, `trl`,
  `diffusers`, `sentence-transformers`, `faiss`, `llama-cpp-python` and `vllm` (🅿️) enter, each
  *after* the hand-rolled version exists.
- **Version verification is per-day and live** (Principle 6). No version in this plan is written
  from memory; every day's hub §8 names what was actually fetched and when.

### 5.1 Why pins are stricter here than in ordinary projects

A web app with a loose dependency range fails loudly. A machine-learning stack with a loose range
fails *silently and differently*: a changed default in an optimizer, a changed rounding mode in a
kernel, a changed normalization step in a tokenizer. **The result still trains. It just is not the
same model, and you cannot tell by looking.** That is why:

- every package is `==` pinned;
- every Hugging Face model and dataset is pinned by **revision SHA**, not by name — a repo owner can
  force-push and your "reproduction" silently becomes a different experiment (`docs/MODELS.md`,
  `docs/DATASETS.md`);
- every run records the pinned set it ran under (`docs/RUNS.md`).

---

## 6 · 💥 The Five Silent Failures

Ordinary software fails loudly: a stack trace, a 500, a red test. **Generative systems fail
quietly** — they train, they run, they emit fluent plausible output, and they are wrong. These five
are the ones that will cost you a week each if you have not been taught to look for them, and
**every day document that touches one must name it in words** (§25.4.1).

| # | Trap | What you see | What is actually happening |
| --- | --- | --- | --- |
| 1 | **Contamination** | Your model scores brilliantly on a benchmark. | The benchmark's test set was in your pretraining corpus. You measured memorization and called it reasoning. Decontamination is TRAIN-23; the day it bites is EVAL-05. |
| 2 | **Tokenizer / template mismatch** | Fine-tuning "works" but the model is subtly worse; or inference output starts with a stray space. | Training used one tokenizer, chat template or BOS convention and inference uses another. Nothing errors. TOK-17, TOK-19, POST-04. |
| 3 | **The loss that counted padding** | Loss goes down, generations are garbage. | Padding tokens, or the prompt itself, were included in the loss. The model is being rewarded for predicting `<pad>`. TRAIN-05, TRAIN-06, POST-05. |
| 4 | **Noise mistaken for improvement** | Version B beats version A by 1.5 points. | Different seed, different sampling temperature, different order — the gap is inside the noise band and you shipped a coin flip. TRAIN-17, EVAL-16, INFER-20. |
| 5 | **Evaluating on the format you trained on** | The fine-tune is a huge win on your eval. | Your eval prompts share the format of your training data. You measured format compliance, not capability. POST-07, EVAL-12. |

> Any day document that touches one of these areas must say which trap it is avoiding, and how the
> reader would detect it. A reader who has been following tutorials needs to be **told**, not
> protected.

---

## 7 · 🧶 The Seventeen Curricula & the ID scheme

Every concept in the plan has an ID. A day **closes** an ID when the concept is built into (or
demonstrably exercised against) Akshara and the day's gates are green. `docs/TRACEABILITY.md` is
regenerated from the day hubs by `scripts/trace.py`; **any open ID from a completed phase is a bug.**

The curricula are grouped into five books. The books are for navigation; the ID prefix is the
identity.

### Book I — Ground: the units of the field

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Foundations | `MATH` | 16 | Tensors, autograd, probability, information theory, numerics, optimization — built, not assumed |
| Tokenization | `TOK` | 20 | Bytes → Unicode → BPE from scratch → the production stacks → the pathologies |
| Representation | `EMB` | 10 | One-hot → lookup table → contextual states → similarity → weight tying |

### Book II — The Machine: architecture and training

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Architecture | `ARCH` | 40 | n-grams → RNNs → attention → the block → position → the variant zoo |
| Training | `TRAIN` | 28 | The loop, the data pipeline, precision, checkpoints, the debug rituals, corpus curation |
| Scaling | `SCALE` | 10 | Scaling laws, compute-optimal sizing, reading a run, when to stop |

### Book III — The Runtime: getting answers out

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Inference | `INFER` | 20 | The autoregressive loop, the sampler zoo, KV cache, prefill/decode, constrained decoding |
| Efficiency | `EFF` | 18 | The memory equation, quantization, LoRA/PEFT, FlashAttention, distillation, CPU inference |
| Serving | `SERVE` | 16 | Formats, a server from scratch, vLLM/llama.cpp, batching, caching, observability, cost |
| Operations | `OPS` | 10 | Repo discipline, secrets, ledgers, testing ML code, artifact hygiene, run tracking |

### Book IV — The Behaviour: making it useful and trustworthy

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Post-training | `POST` | 20 | Base→instruct, SFT, chat templates, preference data, reward models, RLHF, DPO |
| Reasoning | `REASON` | 14 | In-context learning, prompting as engineering, CoT, test-time compute, verifiers |
| Retrieval | `RAG` | 14 | Parametric knowledge, embeddings, chunking, ANN, hybrid, rerank, RAG evaluation |
| Evaluation | `EVAL` | 16 | Perplexity, benchmarks, contamination, LLM-judge, human eval, calibration, significance |
| Safety | `SAFE` | 20 | Threat model, hallucination, injection, memorization, poisoning, bias, licensing, provenance |

### Book V — Beyond text

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Multimodal | `MM` | 16 | ViT, CLIP, VLM projectors, audio, video, any-to-any, multimodal evaluation |
| Generative families | `GEN` | 21 | VAE, GAN 🅿️, diffusion from first principles, guidance, latent diffusion, flow matching |

**Total: 309 concept IDs across 17 curricula.**

> 🅿️ Some IDs are **parked** (awareness-level): you learn the map and the arithmetic, you do not
> build the thing — either because it cannot be done at $0 (§4, T2) or because it is a different
> discipline. A parked ID still gets a full part with a story, a mechanism and a production section.
> What it does not get is a build step. Parked IDs close normally.

The per-ID topics are stated in §§8–23. The **authoritative day→ID assignment is §24**, and a day
document closes **exactly** the IDs §24 assigns it — no more, no fewer.

---

## 8 · 📐 Curriculum MATH — Foundations (MATH-01..16)

Everything needed to build a transformer, built rather than assumed. No prior linear algebra or
calculus course is presumed; what is presumed is that you can read Python.

| ID | Concept | Closes on |
| --- | --- | --- |
| `MATH-01` | Tensors: shape, dtype, device — what "a tensor" actually is in memory | 2 |
| `MATH-02` | Broadcasting and indexing — the rules, and the bug they cause | 2 |
| `MATH-03` | Matrix multiplication as *the* primitive; why hardware loves it | 2 |
| `MATH-04` | Derivatives and the chain rule, from the definition | 3 |
| `MATH-05` | A scalar autograd engine you write — the computation graph, `backward()` | 3 |
| `MATH-06` | Backprop through a linear layer — the transpose that everyone gets wrong | 4 |
| `MATH-07` | Gradient checking — proving your backward pass with finite differences | 4 |
| `MATH-08` | Probability distributions over a vocabulary; logits vs probabilities | 5 |
| `MATH-09` | Sampling from a categorical distribution; the inverse-CDF trick | 5 |
| `MATH-10` | Entropy — the surprise measure, in bits and in nats | 6 |
| `MATH-11` | Cross-entropy and negative log-likelihood — **why this is the loss** | 6 |
| `MATH-12` | KL divergence and perplexity — the same quantity wearing three hats | 6 |
| `MATH-13` | Floating point: fp32, fp16, bf16 — range vs precision, and what overflows | 7 |
| `MATH-14` | The numerically stable softmax and the log-sum-exp trick | 7 |
| `MATH-15` | Gradient descent and momentum — the loss surface as a landscape | 8 |
| `MATH-16` | Adam and AdamW; the learning rate as *the* hyperparameter | 8 |

---

## 9 · 🔤 Curriculum TOK — Tokenization (TOK-01..20)

The first thing you build and the last thing anyone debugs. Silent Failure #2 lives here.

| ID | Concept | Closes on |
| --- | --- | --- |
| `TOK-01` | The vocabulary problem — why not words, why not letters | 9 |
| `TOK-02` | What a tokenizer is, and exactly where it sits in the stack | 9 |
| `TOK-03` | Unicode code points, normalization forms, and the grapheme you thought was a character | 10 |
| `TOK-04` | UTF-8 and bytes — the layer under every modern tokenizer | 10 |
| `TOK-05` | Character-level tokenization, built — and its sequence-length problem | 11 |
| `TOK-06` | Word-level tokenization, built — and the out-of-vocabulary wall that killed it | 11 |
| `TOK-07` | Byte-pair encoding: the merge algorithm, by hand on a toy corpus | 12 |
| `TOK-08` | Training a BPE vocabulary — the merge table as the learned artifact | 12 |
| `TOK-09` | BPE encode and decode — and why decode is not simply the inverse | 13 |
| `TOK-10` | The regex pre-tokenizer — the GPT-2/GPT-4 split patterns, read symbol by symbol | 13 |
| `TOK-11` | Byte-level BPE — how a 256-symbol alphabet represents every language | 13 |
| `TOK-12` | 🔍 Compare: `tiktoken` — speed, the vocabulary file format, what it does differently | 14 |
| `TOK-13` | 🔍 Compare: the `tokenizers` pipeline — normalizer, pre-tokenizer, model, post-processor, decoder | 14 |
| `TOK-14` | WordPiece and the `##` convention | 15 |
| `TOK-15` | Unigram LM and SentencePiece — a *probabilistic* vocabulary, and subword regularization | 15 |
| `TOK-16` | Special tokens — BOS, EOS, PAD, UNK, added tokens, and resizing an embedding matrix | 16 |
| `TOK-17` | Chat templates — roles as tokens; **Silent Failure #2's home** | 16 |
| `TOK-18` | Tokenization pathologies — numbers, whitespace, code, and multilingual token inflation | 17 |
| `TOK-19` | Token healing and the trailing-space bug | 17 |
| `TOK-20` | Vocabulary size as a design decision — the embedding/sequence-length tradeoff | 17 |

---

## 10 · 🧮 Curriculum EMB — Representation (EMB-01..10)

| ID | Concept | Closes on |
| --- | --- | --- |
| `EMB-01` | One-hot vectors and why the embedding lookup *is* a matrix multiply | 18 |
| `EMB-02` | The embedding matrix as learned parameters — what gradient reaches a row | 18 |
| `EMB-03` | Distributional semantics — "you shall know a word by the company it keeps" | 19 |
| `EMB-04` | word2vec and GloVe as history — what they got right, what they could not do | 19 |
| `EMB-05` | Static vs contextual embeddings — the same word, two vectors | 20 |
| `EMB-06` | What a hidden state actually is — the residual stream as a running representation | 20 |
| `EMB-07` | Similarity: cosine, dot product, Euclidean — and when they disagree | 21 |
| `EMB-08` | Anisotropy — why raw LM hidden states make disappointing embeddings | 21 |
| `EMB-09` | Weight tying between input embedding and output head | 22 |
| `EMB-10` | Embedding dimension, the unembedding head, and where the parameters actually are | 22 |

---

## 11 · 🏛️ Curriculum ARCH — Architecture (ARCH-01..40)

The largest thread. The arc is deliberately historical: you build the things that lost, feel exactly
why they lost, and only then build attention. A reader who meets attention first learns a recipe; a
reader who meets it after an LSTM learns an answer.

**11.1 The objective and the pre-transformer era**

| ID | Concept | Closes on |
| --- | --- | --- |
| `ARCH-01` | Next-token prediction as the objective — the whole field in one sentence | 23 |
| `ARCH-02` | Teacher forcing and the train/inference mismatch (exposure bias) | 23 |
| `ARCH-03` | n-gram models, built — counting, smoothing, and the sparsity wall | 24 |
| `ARCH-04` | The bigram neural LM — your first trained model | 25 |
| `ARCH-05` | The MLP language model — a fixed context window and the concatenation ceiling | 26 |
| `ARCH-06` | RNNs and backpropagation through time | 27 |
| `ARCH-07` | LSTM and GRU gating — how a gradient survives a long sequence | 27 |
| `ARCH-08` | 💥 The sequential bottleneck — what a GPU wants, and why recurrence lost | 28 |

**11.2 Attention**

| ID | Concept | Closes on |
| --- | --- | --- |
| `ARCH-09` | Attention as a soft lookup — query, key, value as a dictionary that returns a blend | 29 |
| `ARCH-10` | Scaled dot-product attention, built from the definition | 30 |
| `ARCH-11` | Why √d_k — the variance argument, derived and then measured | 30 |
| `ARCH-12` | Causal masking — the triangle, and the `-inf` before the softmax | 31 |
| `ARCH-13` | Multi-head attention — the reshape that confuses everyone, drawn | 32 |
| `ARCH-14` | Head specialization — reading attention maps, induction heads | 32 |
| `ARCH-15` | Self-attention vs cross-attention | 33 |
| `ARCH-16` | 💥 The O(n²) wall, attention sinks, and the off-by-one mask | 34 |

**11.3 The block and the model**

| ID | Concept | Closes on |
| --- | --- | --- |
| `ARCH-17` | The position-wise feed-forward network — and why it is 4× wide | 35 |
| `ARCH-18` | Activations: ReLU → GELU → SwiGLU, and the gating idea | 35 |
| `ARCH-19` | Residual connections and the residual stream as a shared bus | 36 |
| `ARCH-20` | LayerNorm and RMSNorm — what is normalized, over which axis | 37 |
| `ARCH-21` | Pre-norm vs post-norm — the stability argument that moved the whole field | 37 |
| `ARCH-22` | The transformer block assembled — one class, every piece accounted for | 38 |
| `ARCH-23` | Akshara v0: a full decoder-only model that runs | 39 |
| `ARCH-24` | Parameter counting by hand — where the parameters actually live | 39 |
| `ARCH-25` | The original paper vs what people actually build now — a diff, item by item | 40 |

**11.4 Position**

| ID | Concept | Closes on |
| --- | --- | --- |
| `ARCH-26` | Permutation equivariance — the proof that a transformer has no idea about order | 41 |
| `ARCH-27` | Sinusoidal and learned positional embeddings | 42 |
| `ARCH-28` | RoPE — rotation as relative position, built | 43 |
| `ARCH-29` | ALiBi and relative position biases | 43 |
| `ARCH-30` | Context-length extrapolation — position interpolation, NTK and YaRN scaling | 44 |
| `ARCH-31` | Sliding-window and sparse attention patterns | 44 |

**11.5 The variant zoo**

| ID | Concept | Closes on |
| --- | --- | --- |
| `ARCH-32` | Encoder-only models — bidirectional attention | 45 |
| `ARCH-33` | Masked language modelling — a different objective, a different tool | 45 |
| `ARCH-34` | Encoder–decoder models and cross-attention in anger | 46 |
| `ARCH-35` | Decoder-only, and the argument for why it won | 47 |
| `ARCH-36` | MQA and GQA — a KV-cache-shaped architecture decision | 48 |
| `ARCH-37` | Mixture of Experts — the router and the sparse forward pass | 49 |
| `ARCH-38` | MoE load balancing, capacity factors, and the expert that never gets used | 49 |
| `ARCH-39` | 🅿️ State-space models — Mamba, selective scan, what is genuinely different | 50 |
| `ARCH-40` | 🅿️ Linear attention and hybrid stacks | 50 |

---

## 12 · 🔁 Curriculum TRAIN — Training (TRAIN-01..28)

| ID | Concept | Closes on |
| --- | --- | --- |
| `TRAIN-01` | The first trained model — watching a loss go down, and knowing what "down" means | 25 |
| `TRAIN-02` | The training loop, anatomised — forward, loss, backward, step, zero | 51 |
| `TRAIN-03` | Train/validation split, and the overfitting you *want* on Day 60 | 51 |
| `TRAIN-04` | Datasets and dataloaders — streaming, shuffling, workers, the reproducible shuffle | 52 |
| `TRAIN-05` | Padding and attention masks — **Silent Failure #3's front door** | 53 |
| `TRAIN-06` | Sequence packing — and the document boundary that leaks across it | 53 |
| `TRAIN-07` | Initialization — why scale matters, and the residual-scaled init | 54 |
| `TRAIN-08` | Learning-rate warmup — what it is protecting you from | 55 |
| `TRAIN-09` | Cosine and linear decay; running an LR sweep you can actually afford | 55 |
| `TRAIN-10` | AdamW and decoupled weight decay — which parameters are excluded, and why | 56 |
| `TRAIN-11` | Gradient clipping — global norm, and reading the clip rate as a signal | 56 |
| `TRAIN-12` | Mixed precision — fp16 vs bf16, loss scaling, the master weights | 57 |
| `TRAIN-13` | Gradient accumulation — a large batch on a small card | 57 |
| `TRAIN-14` | Activation (gradient) checkpointing — trading compute for memory | 57 |
| `TRAIN-15` | Checkpoint format — what must be saved beyond the weights | 58 |
| `TRAIN-16` | Resume — the run that survives a disconnected free notebook | 58 |
| `TRAIN-17` | Determinism and seeds — what is reproducible and what never will be | 59 |
| `TRAIN-18` | 💥 Overfit one batch — the ritual that precedes every real run | 60 |
| `TRAIN-19` | Reading loss curves — plateaus, spikes, divergence, and the LR that caused each | 60 |
| `TRAIN-20` | 💥 NaN hunting, and the silent shape bug that trains anyway | 60 |
| `TRAIN-21` | Pretraining corpora — where text comes from, and quality filtering | 61 |
| `TRAIN-22` | Deduplication — exact, near-duplicate (MinHash), and why it matters more than you think | 62 |
| `TRAIN-23` | Decontamination against your eval sets — **Silent Failure #1's only defence** | 62 |
| `TRAIN-24` | Data mixtures and curriculum — the ratio that decides what the model is good at | 63 |
| `TRAIN-25` | Tokenizing a corpus at scale — the memmap file, and streaming without RAM | 64 |
| `TRAIN-26` | Throughput and MFU — is your run actually using the GPU you were given? | 67 |
| `TRAIN-27` | 🅿️ Distributed training — DP, DDP, FSDP/ZeRO stages, and the arithmetic of each | 66 |
| `TRAIN-28` | The hyperparameter budget — what to tune when you cannot afford to tune | 55 |

---

## 13 · 📈 Curriculum SCALE — Scaling & Pretraining (SCALE-01..10)

| ID | Concept | Closes on |
| --- | --- | --- |
| `SCALE-01` | The scaling-law idea — loss as a power law in compute | 65 |
| `SCALE-02` | Kaplan et al. — parameters, data, compute, and what it claimed | 65 |
| `SCALE-03` | Chinchilla — the compute-optimal correction, and what changed in practice | 65 |
| `SCALE-04` | Tokens per parameter as a planning number | 65 |
| `SCALE-05` | Sizing a model to a fixed compute budget — Akshara's parameter count, derived | 66 |
| `SCALE-06` | The loss-prediction workflow — small runs that justify a big claim | 66 |
| `SCALE-07` | 🅿️ Hyperparameter transfer (muP) — tuning small, running large | 67 |
| `SCALE-08` | Reading a real run — is this working, and how would you know early? | 68 |
| `SCALE-09` | Emergent abilities and the measurement critique | 68 |
| `SCALE-10` | When to stop — overtraining, inference-optimal models, and the small-model case | 68 |

---

## 14 · 🎲 Curriculum INFER — Decoding & Inference (INFER-01..20)

| ID | Concept | Closes on |
| --- | --- | --- |
| `INFER-01` | The autoregressive generation loop, written honestly | 69 |
| `INFER-02` | Why decoding is memory-bandwidth bound, not compute bound | 69 |
| `INFER-03` | Greedy decoding — and the repetition it produces | 70 |
| `INFER-04` | Beam search — and why it is wrong for open-ended text | 70 |
| `INFER-05` | Temperature — what dividing logits actually does to the distribution | 71 |
| `INFER-06` | Top-k and top-p (nucleus) sampling | 71 |
| `INFER-07` | Min-p, typical sampling, and the rest of the zoo, compared on your own model | 71 |
| `INFER-08` | Repetition, frequency and presence penalties | 72 |
| `INFER-09` | Logit bias and banned tokens | 72 |
| `INFER-10` | Stopping — EOS, stop strings, max tokens, and the truncated JSON | 73 |
| `INFER-11` | The KV cache, built — the optimisation that makes chat possible | 74 |
| `INFER-12` | KV-cache memory cost, eviction, and the context length you can afford | 74 |
| `INFER-13` | Prefill vs decode — two workloads with different bottlenecks | 75 |
| `INFER-14` | TTFT and TPOT — the two latency numbers users actually feel | 75 |
| `INFER-15` | Constrained decoding — JSON schemas without prayer | 76 |
| `INFER-16` | Grammars and finite-state decoding | 76 |
| `INFER-17` | 🅿️ Speculative decoding — draft models and verification | 77 |
| `INFER-18` | 🅿️ Continuous batching — the scheduler that made serving cheap | 77 |
| `INFER-19` | Streaming output — token-by-token, and the detokenization boundary bug | 75 |
| `INFER-20` | Determinism at temperature 0 — and why it still is not deterministic | 71 |

---

## 15 · 🗜️ Curriculum EFF — Efficiency (EFF-01..18)

Where the $0 constraint becomes the curriculum (Principle 15).

| ID | Concept | Closes on |
| --- | --- | --- |
| `EFF-01` | The memory equation — parameters, gradients, optimizer states, activations | 78 |
| `EFF-02` | KV-cache memory vs context length — the term everyone forgets | 78 |
| `EFF-03` | What quantization is — scales, zero points, symmetric vs asymmetric | 79 |
| `EFF-04` | Post-training quantization vs quantization-aware training | 79 |
| `EFF-05` | GPTQ and AWQ — calibration data and the outlier problem | 80 |
| `EFF-06` | GGUF and llama.cpp — the k-quant families | 80 |
| `EFF-07` | Measuring quantization damage — the number you must produce before shipping | 80 |
| `EFF-08` | LoRA from scratch — the low-rank update, derived and built | 81 |
| `EFF-09` | Rank, alpha, target modules, and merging an adapter back | 81 |
| `EFF-10` | QLoRA — 4-bit base weights, NF4, double quantization, paged optimizers | 82 |
| `EFF-11` | Adapters, prefix tuning, prompt tuning — the PEFT family compared | 82 |
| `EFF-12` | FlashAttention — IO-awareness, tiling, and why it is exact not approximate | 83 |
| `EFF-13` | PagedAttention — virtual memory for the KV cache | 83 |
| `EFF-14` | Knowledge distillation — hard labels, soft labels, and the temperature | 84 |
| `EFF-15` | Pruning and sparsity — structured, unstructured, and what hardware rewards | 84 |
| `EFF-16` | CPU inference — what actually makes it slow, and what fixes it | 85 |
| `EFF-17` | ONNX, `torch.compile` and graph capture | 85 |
| `EFF-18` | Offloading and memory-constrained loading — running a model bigger than your RAM | 85 |

---

## 16 · 🎯 Curriculum POST — Post-training & Alignment (POST-01..20)

| ID | Concept | Closes on |
| --- | --- | --- |
| `POST-01` | A base model is not a chatbot — the gap, demonstrated on your own model | 86 |
| `POST-02` | Instruction datasets — human, synthetic, and the licence question | 87 |
| `POST-03` | Data quality over quantity — the result that keeps being rediscovered | 87 |
| `POST-04` | Chat templates in training — **Silent Failure #2** | 88 |
| `POST-05` | Loss masking — train on the completion, not the prompt (**Silent Failure #3**) | 88 |
| `POST-06` | The LoRA fine-tuning run — Akshara learns to follow instructions | 89 |
| `POST-07` | Evaluating a fine-tune — did it learn the task or the format? (**Silent Failure #5**) | 90 |
| `POST-08` | Preference data — pairwise comparison as the annotation primitive | 91 |
| `POST-09` | Annotation noise, inter-annotator agreement, and the ceiling it imposes | 91 |
| `POST-10` | Reward model training — a classifier over pairs | 92 |
| `POST-11` | Reward hacking and Goodhart's law, observed | 92 |
| `POST-12` | RLHF with PPO — the four-model pipeline, explained honestly | 93 |
| `POST-13` | The KL penalty and the reference model — the leash | 93 |
| `POST-14` | DPO, built — preference optimization with no reward model | 94 |
| `POST-15` | ORPO, KTO, SimPO — the variants and what each removes | 94 |
| `POST-16` | Online vs offline preference optimization — the distribution-shift argument | 94 |
| `POST-17` | 🅿️ RLAIF and constitutional AI — AI feedback in place of human | 95 |
| `POST-18` | Rejection sampling, best-of-n, GRPO, and RL on verifiable rewards | 95 |
| `POST-19` | 💥 Catastrophic forgetting and the alignment tax, measured | 96 |
| `POST-20` | 💥 Over-refusal, sycophancy and mode collapse | 96 |

---

## 17 · 🧠 Curriculum REASON — Reasoning & Prompting (REASON-01..14)

| ID | Concept | Closes on |
| --- | --- | --- |
| `REASON-01` | In-context learning — the phenomenon, and the induction-head story | 97 |
| `REASON-02` | What few-shot examples actually do — format vs content | 97 |
| `REASON-03` | Prompt structure — instruction, context, examples, output format | 98 |
| `REASON-04` | System prompts and role conditioning — what is and is not privileged | 98 |
| `REASON-05` | Chain of thought — why generating steps helps a next-token predictor | 99 |
| `REASON-06` | Faithfulness — when the stated reasoning is a post-hoc story | 99 |
| `REASON-07` | Self-consistency and majority vote over samples | 100 |
| `REASON-08` | Decomposition and self-critique — and where self-critique fails | 100 |
| `REASON-09` | Reasoning models and thinking tokens — a budget you pay and never see | 101 |
| `REASON-10` | Test-time compute as a scaling axis | 101 |
| `REASON-11` | Verifiers and process reward models | 102 |
| `REASON-12` | Tools as the correctness escape hatch — when not to ask the model | 102 |
| `REASON-13` | 💥 Prompt sensitivity, position bias, lost-in-the-middle | 103 |
| `REASON-14` | Prompt injection — the preview (full treatment in SAFE) | 103 |

---

## 18 · 📚 Curriculum RAG — Knowledge & Retrieval (RAG-01..14)

| ID | Concept | Closes on |
| --- | --- | --- |
| `RAG-01` | Parametric knowledge — what a model stores, and where | 104 |
| `RAG-02` | The hallucination taxonomy — closed-book, open-book, intrinsic, extrinsic | 104 |
| `RAG-03` | Retrieval embeddings — contrastive training, hard negatives | 105 |
| `RAG-04` | Bi-encoder vs cross-encoder — the latency/quality trade | 105 |
| `RAG-05` | Chunking — the decision that silently sets your recall ceiling | 106 |
| `RAG-06` | Exact vs approximate nearest neighbour search | 107 |
| `RAG-07` | HNSW and IVF — the recall/latency/memory triangle | 107 |
| `RAG-08` | Lexical retrieval (BM25) and hybrid fusion | 108 |
| `RAG-09` | Rerankers — the second pass that earns its latency | 108 |
| `RAG-10` | The RAG pipeline assembled over Akshara | 109 |
| `RAG-11` | Retrieval metrics — recall@k, MRR, nDCG | 110 |
| `RAG-12` | Answer metrics — faithfulness, groundedness, attribution | 110 |
| `RAG-13` | Long context vs RAG vs fine-tuning — the decision table | 111 |
| `RAG-14` | 💥 When RAG is the wrong tool — and when it was a database query all along | 111 |

---

## 19 · 📊 Curriculum EVAL — Evaluation (EVAL-01..16)

| ID | Concept | Closes on |
| --- | --- | --- |
| `EVAL-01` | Why evaluation is the hardest problem in the field | 112 |
| `EVAL-02` | Perplexity — the definition, and computing it on your own model | 113 |
| `EVAL-03` | What perplexity hides — and why it is not comparable across tokenizers | 113 |
| `EVAL-04` | Benchmark suites — what MMLU, GSM8K, HumanEval actually measure | 114 |
| `EVAL-05` | Contamination and leakage — **Silent Failure #1**, detected | 114 |
| `EVAL-06` | n-gram metrics — BLEU, ROUGE, and why they are weak for generation | 115 |
| `EVAL-07` | Model-based metrics — BERTScore and friends | 115 |
| `EVAL-08` | LLM-as-judge — building one, and calibrating it against humans | 116 |
| `EVAL-09` | Judge biases — position, verbosity, self-preference, and the fixes | 116 |
| `EVAL-10` | Human evaluation — pairwise preference, and what to actually ask | 117 |
| `EVAL-11` | Elo and Bradley-Terry — turning comparisons into a ranking | 117 |
| `EVAL-12` | Rubrics and task-specific evalsets — **Silent Failure #5**'s antidote | 117 |
| `EVAL-13` | Regression discipline — evals as tests, in CI | 118 |
| `EVAL-14` | Calibration — does the probability mean anything? | 119 |
| `EVAL-15` | Uncertainty and abstention — teaching a model to say "I don't know" | 119 |
| `EVAL-16` | Statistical significance and sample size — **Silent Failure #4**'s antidote | 119 |

---

## 20 · 🖼️ Curriculum MM — Multimodal (MM-01..16)

| ID | Concept | Closes on |
| --- | --- | --- |
| `MM-01` | The general recipe — any modality becomes a sequence of vectors | 120 |
| `MM-02` | Images as patches — the Vision Transformer, built | 121 |
| `MM-03` | 2D position, variable resolution, and the aspect-ratio problem | 121 |
| `MM-04` | Contrastive learning and CLIP — the InfoNCE objective | 122 |
| `MM-05` | The shared embedding space — zero-shot classification, and its limits | 122 |
| `MM-06` | Vision–language models — the projector that bridges into an LLM | 123 |
| `MM-07` | VLM training stages and data — align, then instruction-tune | 123 |
| `MM-08` | Audio as spectrograms — the mel filterbank | 124 |
| `MM-09` | ASR and Whisper's encoder–decoder — and its hallucination on silence | 124 |
| `MM-10` | Neural audio codecs — discrete speech tokens, EnCodec-style | 125 |
| `MM-11` | Video — frames, temporal modelling, and frame sampling | 126 |
| `MM-12` | The cost problem in video — tokens per second of footage | 126 |
| `MM-13` | 🅿️ Any-to-any and unified models | 127 |
| `MM-14` | 💥 Multimodal hallucination and grounding failure | 128 |
| `MM-15` | Multimodal evaluation — and why it is even harder than text | 128 |
| `MM-16` | OCR and document understanding — the "just read the screenshot" trap | 127 |

---

## 21 · 🌫️ Curriculum GEN — Other Generative Families (GEN-01..21)

Generative AI is not one architecture. This book exists so you can say *why* diffusion beat GANs for
images while autoregression beat everything for text — and defend it.

| ID | Concept | Closes on |
| --- | --- | --- |
| `GEN-01` | The family tree — autoregressive, VAE, GAN, flow, diffusion; what each optimizes | 129 |
| `GEN-02` | Autoencoders and the latent space | 130 |
| `GEN-03` | VAEs — the ELBO and the reparameterization trick | 130 |
| `GEN-04` | 🅿️ GANs — the adversarial game | 131 |
| `GEN-05` | 🅿️ Mode collapse, training instability, and why GANs faded | 131 |
| `GEN-06` | The forward diffusion process — noising, and the closed form that makes it trainable | 132 |
| `GEN-07` | The reverse process — the denoiser and what it actually predicts | 133 |
| `GEN-08` | The DDPM training objective — simplified to a regression on noise | 133 |
| `GEN-09` | A tiny diffusion model, trained on your own machine | 134 |
| `GEN-10` | DDIM — deterministic sampling and the step/quality curve | 135 |
| `GEN-11` | Noise schedules — linear, cosine, and what the schedule controls | 135 |
| `GEN-12` | Classifier guidance | 136 |
| `GEN-13` | Classifier-free guidance and the guidance scale — the dial everyone turns | 136 |
| `GEN-14` | Latent diffusion — the VAE compressor that made it affordable | 137 |
| `GEN-15` | Text conditioning — cross-attention into the denoiser | 137 |
| `GEN-16` | ControlNet and structural conditioning | 138 |
| `GEN-17` | LoRA, DreamBooth and textual inversion for images | 138 |
| `GEN-18` | Flow matching and rectified flow — what replaced DDPM | 139 |
| `GEN-19` | 🅿️ Video generation — temporal consistency as the hard part | 140 |
| `GEN-20` | 🅿️ Audio and music generation, and modern TTS | 140 |
| `GEN-21` | Evaluating generative models — FID, CLIP score, and why human preference still wins | 140 |

---

## 22 · 🛡️ Curriculum SAFE — Safety, Security & Ethics (SAFE-01..20)

| ID | Concept | Closes on |
| --- | --- | --- |
| `SAFE-01` | Data provenance and consent at collection time | 61 |
| `SAFE-02` | The threat model for a generative system — who attacks it, and how | 141 |
| `SAFE-03` | Hallucination mechanisms — why a next-token predictor confabulates | 142 |
| `SAFE-04` | Measuring and mitigating hallucination | 142 |
| `SAFE-05` | Direct prompt injection and jailbreaks | 143 |
| `SAFE-06` | Indirect injection and the lethal trifecta (private data · untrusted content · exfiltration) | 143 |
| `SAFE-07` | Defenses and their limits — why "instruct it not to" is not a defence | 143 |
| `SAFE-08` | Memorization and training-data extraction | 144 |
| `SAFE-09` | Membership inference and PII in a corpus | 144 |
| `SAFE-10` | Data poisoning and backdoors | 145 |
| `SAFE-11` | Supply chain — pickle deserialization, safetensors, model provenance | 145 |
| `SAFE-12` | Bias — where it comes from in data and in objective | 146 |
| `SAFE-13` | Measuring bias and fairness — rather than deploring it | 146 |
| `SAFE-14` | Copyright, licensing and consent in training data | 147 |
| `SAFE-15` | Watermarking generated content, and its fragility | 148 |
| `SAFE-16` | Provenance standards (C2PA) and deepfakes — detection's real limits | 148 |
| `SAFE-17` | Guardrails and content filtering in practice | 149 |
| `SAFE-18` | Model cards and documentation as an engineering artifact | 149 |
| `SAFE-19` | 🅿️ The regulatory map — EU AI Act and the obligations that attach to a model | 149 |
| `SAFE-20` | Dual use and release decisions — open weights, gated, or closed | 149 |

---

## 23 · 🚀 Curriculum SERVE — Serving & Systems (SERVE-01..16) · OPS-01..10

| ID | Concept | Closes on |
| --- | --- | --- |
| `SERVE-01` | Model file formats — safetensors, GGUF, and the pickle you must not trust | 150 |
| `SERVE-02` | Loading — memory-mapped weights, lazy loading, and startup time | 150 |
| `SERVE-03` | An inference server from scratch — the request lifecycle | 151 |
| `SERVE-04` | Streaming over HTTP — SSE, chunked responses, and cancellation | 151 |
| `SERVE-05` | 🔍 Compare: vLLM and TGI — what they do that yours does not | 152 |
| `SERVE-06` | 🔍 Compare: llama.cpp and Ollama — the CPU/edge lane | 152 |
| `SERVE-07` | Continuous batching in production | 153 |
| `SERVE-08` | Admission control, queueing and backpressure | 153 |
| `SERVE-09` | Prefix and prompt caching — the cheapest win in serving | 154 |
| `SERVE-10` | Semantic caching — and when it returns the wrong answer | 154 |
| `SERVE-11` | Metrics — latency percentiles, tokens/s, cost per request | 155 |
| `SERVE-12` | Tracing one generation request end to end | 155 |
| `SERVE-13` | Model registry and versioning — which weights answered that request? | 156 |
| `SERVE-14` | Containerizing a model service | 156 |
| `SERVE-15` | Capacity planning — sizing a deployment from a latency target | 157 |
| `SERVE-16` | Build vs buy — self-host vs API economics, worked | 157 |

| ID | Concept | Closes on |
| --- | --- | --- |
| `OPS-01` | Repo bootstrap and layout | 1 |
| `OPS-02` | Secrets and API tokens — `.env`, `.gitignore`, the Hugging Face token | 1 |
| `OPS-03` | Ledgers and traceability tooling | 1 |
| `OPS-04` | Free-compute accounts; the notebook ↔ module discipline | 1 |
| `OPS-05` | Testing ML code — deterministic unit tests for tensors and layers | 59 |
| `OPS-06` | The `./m check` quality gate | 59 |
| `OPS-07` | Artifact discipline — what never enters git: weights, datasets, checkpoints | 64 |
| `OPS-08` | Experiment tracking — the run ledger, config capture, reproducing a run | 67 |
| `OPS-09` | Evals in CI — the regression gate | 118 |
| `OPS-10` | Observability and cost accounting for a served model | 155 |

---

## 24 · 🗓️ The Day Map (day → IDs closed)

### 24.0 Why there are 162 days and not 150

**Nobody chose 162.** The number is what came out of taking 309 concepts and splitting them at idea
boundaries until each day held one coherent unit of subject (Principle 19). It is an *output*, and
it is quoted here only so the tracker has something to count against.

This matters because the alternative — picking a round target first — silently corrupts everything
downstream. A plan that commits to "100 days" must then compress attention into two days and
tokenization into one, and the compression always lands on the same victim: the explanation.
Sixty-day plans are not shorter courses; they are the same course with the reasoning removed.

Three consequences you should hold on to:

1. **A day is not a session.** Day 60 might be one evening; Day 143 might be four. Both are the day
   being done properly (Principle 17). `./m done N` is gated on a ticked checklist and green checks,
   never on elapsed time.
2. **Days are not equal in size.** Day 24 closes one ID; Day 149 closes four. Day 71 has four IDs
   because temperature, top-k, top-p and determinism are genuinely one mental model; Day 29 has one
   ID because "attention as a soft lookup" is the single hardest idea in the plan and deserves a day
   with nothing else in it.
3. **The count changes when content demands it.** If a day turns out to hold two ideas, it is split
   — by ADR, with `docs/CHANGELOG_PLAN.md` updated, and the total moves. That is the plan working
   as designed, not the plan failing.

### 24.1 The 22 phases

| Phase | Days | Theme | Gate |
| --- | --- | --- | --- |
| **0** | **0** | **Foundry: the machine, the skeleton, the driver** | `./m check` green; one commit; no secret in git |
| 1 | 1–8 | The ground: tensors, gradients, information | A scalar autograd engine passes gradient checking |
| 2 | 9–17 | Text becomes numbers | Your BPE tokenizer round-trips every byte of a UTF-8 corpus |
| 3 | 18–22 | Representation | Embedding lookup implemented and tied to an output head |
| 4 | 23–28 | Before attention: the sequence problem | An LSTM trains; you can state its bottleneck in one sentence |
| 5 | 29–34 | Attention | Multi-head causal attention, hand-written, matches a reference within tolerance |
| 6 | 35–40 | The block and the model | Akshara v0 forward pass runs; parameter count matches your hand calculation |
| 7 | 41–44 | Position | RoPE implemented; position ablation shows the model degrades without it |
| 8 | 45–50 | The variant zoo | You can defend decoder-only, GQA and MoE choices with arithmetic |
| 9 | 51–60 | Training mechanics | Overfit-one-batch passes; `./m check` green including model unit tests |
| 10 | 61–68 | Data & the pretraining run | Akshara generates English-shaped text; loss curve and model size both defended |
| 11 | 69–77 | Decoding & inference | KV cache gives identical output to the naive loop, measurably faster |
| 12 | 78–85 | Efficiency | Akshara runs 4-bit on CPU; quantization damage measured, not assumed |
| 13 | 86–96 | Post-training & alignment | Instruction-following model; DPO run complete; alignment tax measured |
| 14 | 97–103 | Reasoning & prompting | A prompt-sensitivity study with error bars |
| 15 | 104–111 | Knowledge & retrieval | RAG pipeline over Akshara, with retrieval and answer metrics separated |
| 16 | 112–119 | Evaluation | Full eval suite green in CI; contamination check clean |
| 17 | 120–128 | Multimodal | A projector trained; Akshara answers a question about an image |
| 18 | 129–140 | Other generative families | A tiny diffusion model samples recognisable images with CFG |
| 19 | 141–149 | Safety, security & ethics | Injection attempts contained; model card written; corpus licence-audited |
| 20 | 150–157 | Serving & operations | Streaming endpoint in a container; p50/p95 and cost per request reported |
| 21 | 158–161 | Capstone | The whole system, cold, end to end + audit |

**Every phase gate includes the freshness check (§26).**

### 24.2 The map

> The authoritative day→ID assignment. Day documents close **exactly** these IDs — no more, no
> fewer. 🅿️ = parked/awareness-level treatment inside that day. 💥 = the day's deliberate-failure
> part is the day's centre of gravity. 🔍 = a "build first, compare after" day (Principle 3): the
> hand-rolled version already exists and today you open the library.

#### Phase 0 — Foundry (Day 0)

| Day | Title | IDs closed |
| --- | --- | --- |
| 0 | Toolchain, skeleton and the `./m` driver — one owner for the environment, a repo that cannot leak a token or commit a checkpoint, and a gate that refuses a half-finished day | — |

> Day 0 closes no IDs by design: it is the machine, the skeleton and the driver, which are
> preconditions for the curriculum rather than part of it. That is what keeps `TRACEABILITY.md`
> valid — no ID is assigned to a day that teaches no concept.

#### Phase 1 — The ground (Days 1–8)

| Day | Title | IDs closed |
| --- | --- | --- |
| 1 | Bootstrap & the map — repo, `.env` + `.gitignore`, uv + Python 3.12, the five ledgers, `scripts/trace.py`, and the free-compute accounts | OPS-01, OPS-02, OPS-03, OPS-04 |
| 2 | Tensors — shape, dtype, stride, device, broadcasting; the matmul that is 90% of everything you will run | MATH-01, MATH-02, MATH-03 |
| 3 | Derivatives by hand — the chain rule as a graph, and a scalar autograd engine you write | MATH-04, MATH-05 |
| 4 | Backprop through a layer — the transpose everyone gets wrong, proved by finite differences | MATH-06, MATH-07 |
| 5 | Probability over a vocabulary — logits, softmax, and sampling from a categorical | MATH-08, MATH-09 |
| 6 | Information — entropy, cross-entropy, KL, perplexity; **why the loss is the loss** | MATH-10, MATH-11, MATH-12 |
| 7 | 💥 Numerical reality — fp32/fp16/bf16, the softmax that returns NaN, and log-sum-exp | MATH-13, MATH-14 |
| 8 | Optimization — gradient descent, momentum, Adam/AdamW, and the learning rate | MATH-15, MATH-16 |

#### Phase 2 — Text becomes numbers (Days 9–17)

| Day | Title | IDs closed |
| --- | --- | --- |
| 9 | The vocabulary problem — why not words, why not letters, and what a tokenizer is for | TOK-01, TOK-02 |
| 10 | Unicode, code points and bytes — the layer under every tokenizer, and the emoji that is four characters | TOK-03, TOK-04 |
| 11 | Character-level and word-level tokenizers, built — and where each one dies | TOK-05, TOK-06 |
| 12 | BPE from scratch I — the merge loop, run by hand on a toy corpus, then trained | TOK-07, TOK-08 |
| 13 | BPE from scratch II — encode, decode, the regex pre-tokenizer, and byte-level BPE | TOK-09, TOK-10, TOK-11 |
| 14 | 🔍 Now compare — `tiktoken` and the `tokenizers` pipeline; what a production tokenizer does that yours does not | TOK-12, TOK-13 |
| 15 | The other families — WordPiece, Unigram and SentencePiece; a *probabilistic* vocabulary | TOK-14, TOK-15 |
| 16 | Special tokens & chat templates — BOS/EOS/PAD/UNK, resizing an embedding, and **Silent Failure #2** | TOK-16, TOK-17 |
| 17 | 💥 The tokenizer failure lab — numbers, whitespace, code, multilingual inflation, token healing, and choosing a vocabulary size | TOK-18, TOK-19, TOK-20 |

#### Phase 3 — Representation (Days 18–22)

| Day | Title | IDs closed |
| --- | --- | --- |
| 18 | From one-hot to a lookup table — what an embedding actually is, and which gradient reaches which row | EMB-01, EMB-02 |
| 19 | Distributional semantics — word2vec and GloVe as history, and what they got right | EMB-03, EMB-04 |
| 20 | Static vs contextual — the same word, two vectors; the residual stream as a running representation | EMB-05, EMB-06 |
| 21 | 💥 Measuring similarity — cosine, dot, Euclidean, and the anisotropy that makes raw LM states disappointing | EMB-07, EMB-08 |
| 22 | Weight tying and the unembedding head — where the parameters actually are | EMB-09, EMB-10 |

#### Phase 4 — Before attention: the sequence problem (Days 23–28)

| Day | Title | IDs closed |
| --- | --- | --- |
| 23 | Next-token prediction — the whole field in one sentence; teacher forcing and exposure bias | ARCH-01, ARCH-02 |
| 24 | The n-gram model, built — counting, smoothing, and the sparsity wall you hit immediately | ARCH-03 |
| 25 | The bigram neural LM — your first trained model, and what "the loss went down" means | ARCH-04, TRAIN-01 |
| 26 | The MLP language model — a fixed window, and the concatenation ceiling | ARCH-05 |
| 27 | RNNs and LSTMs, built — recurrence, BPTT, and how a gate keeps a gradient alive | ARCH-06, ARCH-07 |
| 28 | 💥 Why recurrence lost — the sequential bottleneck, measured against what a GPU wants | ARCH-08 |

#### Phase 5 — Attention (Days 29–34)

| Day | Title | IDs closed |
| --- | --- | --- |
| 29 | Attention as a soft lookup — query, key, value, and the dictionary that returns a blend | ARCH-09 |
| 30 | Scaled dot-product attention, built — and why √d_k, derived then measured | ARCH-10, ARCH-11 |
| 31 | Causal masking — the triangle that prevents cheating, and the `-inf` before the softmax | ARCH-12 |
| 32 | Multi-head attention — the reshape that confuses everyone, drawn; and what heads specialise in | ARCH-13, ARCH-14 |
| 33 | Self-attention vs cross-attention — the same mechanism, two wirings | ARCH-15 |
| 34 | 💥 The attention failure lab — the O(n²) wall, attention sinks, and the mask that was off by one | ARCH-16 |

#### Phase 6 — The block and the model (Days 35–40)

| Day | Title | IDs closed |
| --- | --- | --- |
| 35 | The feed-forward network — why 4× wide, and ReLU → GELU → SwiGLU | ARCH-17, ARCH-18 |
| 36 | Residual connections — the highway that makes depth trainable, and the stream as a shared bus | ARCH-19 |
| 37 | Normalization — LayerNorm vs RMSNorm, pre-norm vs post-norm, and the argument that moved the field | ARCH-20, ARCH-21 |
| 38 | The transformer block assembled — one class, every piece accounted for | ARCH-22 |
| 39 | **Akshara v0** — a full decoder-only model that runs, with every parameter counted by hand | ARCH-23, ARCH-24 |
| 40 | 🔍 Reading the original paper — the 2017 architecture vs what people actually build now, diffed item by item | ARCH-25 |

#### Phase 7 — Position (Days 41–44)

| Day | Title | IDs closed |
| --- | --- | --- |
| 41 | 💥 The model has no idea about order — permutation equivariance, proved by shuffling your own input | ARCH-26 |
| 42 | Sinusoidal and learned positional embeddings | ARCH-27 |
| 43 | RoPE, built — rotation as relative position; and ALiBi's different bet | ARCH-28, ARCH-29 |
| 44 | Long context — position interpolation, NTK/YaRN scaling, sliding-window and sparse attention | ARCH-30, ARCH-31 |

#### Phase 8 — The variant zoo (Days 45–50)

| Day | Title | IDs closed |
| --- | --- | --- |
| 45 | Encoder-only — bidirectional attention and masked language modelling; what BERT-shaped models are still best at | ARCH-32, ARCH-33 |
| 46 | Encoder–decoder — seq2seq and cross-attention in anger | ARCH-34 |
| 47 | Decoder-only, and the argument for why it won | ARCH-35 |
| 48 | MQA and GQA — an architecture decision made entirely by the KV cache | ARCH-36 |
| 49 | Mixture of Experts — the router, the sparse forward pass, load balancing, and the dead expert | ARCH-37, ARCH-38 |
| 50 | 🅿️ State-space models and hybrids — Mamba, selective scan, linear attention: what is genuinely different | ARCH-39, ARCH-40 |

#### Phase 9 — Training mechanics (Days 51–60)

| Day | Title | IDs closed |
| --- | --- | --- |
| 51 | The training loop, written once and properly — and the train/val split you will need on Day 60 | TRAIN-02, TRAIN-03 |
| 52 | Datasets and dataloaders — streaming, workers, and a shuffle you can reproduce | TRAIN-04 |
| 53 | 💥 Batching text — padding, attention masks, sequence packing, and **the loss that counted the pads** | TRAIN-05, TRAIN-06 |
| 54 | Initialization — why scale matters, and the residual-scaled init | TRAIN-07 |
| 55 | Learning-rate schedules — warmup, cosine decay, and the hyperparameter budget of someone who cannot afford a sweep | TRAIN-08, TRAIN-09, TRAIN-28 |
| 56 | AdamW, decoupled weight decay and gradient clipping — and reading the clip rate as a signal | TRAIN-10, TRAIN-11 |
| 57 | The three levers of a small card — mixed precision, gradient accumulation, activation checkpointing | TRAIN-12, TRAIN-13, TRAIN-14 |
| 58 | Checkpoint and resume — the run that survives a disconnected free notebook | TRAIN-15, TRAIN-16 |
| 59 | Determinism, seeds, and testing ML code — what a unit test for a layer looks like; the `./m check` gate | TRAIN-17, OPS-05, OPS-06 |
| 60 | 💥 The debug ritual — overfit one batch, read the loss curve, hunt the NaN, and find the shape bug that trains anyway | TRAIN-18, TRAIN-19, TRAIN-20 |

#### Phase 10 — Data & the pretraining run (Days 61–68)

| Day | Title | IDs closed |
| --- | --- | --- |
| 61 | Where pretraining data comes from — sources, quality filtering, and consent at collection time | TRAIN-21, SAFE-01 |
| 62 | 💥 Deduplication and decontamination — the two steps everyone skips, and **Silent Failure #1** | TRAIN-22, TRAIN-23 |
| 63 | Data mixtures and curriculum — the ratio that decides what your model is good at | TRAIN-24 |
| 64 | Tokenizing a corpus at scale — the memmap file; and what never enters git | TRAIN-25, OPS-07 |
| 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per parameter | SCALE-01, SCALE-02, SCALE-03, SCALE-04 |
| 66 | Sizing Akshara — the parameter count derived from one free T4's VRAM; 🅿️ what you would do with eight GPUs | SCALE-05, SCALE-06, TRAIN-27 |
| 67 | **The pretraining run** — launch, watch, and know whether the GPU is actually working; the run ledger | TRAIN-26, SCALE-07, OPS-08 |
| 68 | Phase gate — reading your own run; emergence and its critics; when to stop | SCALE-08, SCALE-09, SCALE-10 |

#### Phase 11 — Decoding & inference (Days 69–77)

| Day | Title | IDs closed |
| --- | --- | --- |
| 69 | The autoregressive loop, honestly — one token at a time, and why decoding is memory-bound | INFER-01, INFER-02 |
| 70 | Greedy and beam search — and why beam is the wrong tool for open-ended text | INFER-03, INFER-04 |
| 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on your own model; and why temperature 0 still is not deterministic | INFER-05, INFER-06, INFER-07, INFER-20 |
| 72 | Penalties and logit processors — repetition, frequency, presence, logit bias, banned tokens | INFER-08, INFER-09 |
| 73 | 💥 Stopping — EOS, stop strings, max tokens, and the truncated JSON at 3am | INFER-10 |
| 74 | The KV cache, built — the single optimisation that makes chat affordable, and what it costs in memory | INFER-11, INFER-12 |
| 75 | Prefill vs decode — TTFT, TPOT, streaming, and the detokenization boundary bug | INFER-13, INFER-14, INFER-19 |
| 76 | Constrained decoding — JSON schemas, grammars, and finite-state masking of logits | INFER-15, INFER-16 |
| 77 | 🅿️ Speculative decoding and continuous batching — the two ideas that made serving cheap | INFER-17, INFER-18 |

#### Phase 12 — Efficiency (Days 78–85)

| Day | Title | IDs closed |
| --- | --- | --- |
| 78 | The memory equation — parameters, gradients, optimizer states, activations, and the KV-cache term everyone forgets | EFF-01, EFF-02 |
| 79 | Quantization I — scales and zero points; what int8 and int4 actually do; PTQ vs QAT | EFF-03, EFF-04 |
| 80 | 💥 Quantization II — GPTQ, AWQ, GGUF; Akshara at 4 bits, with the damage **measured** | EFF-05, EFF-06, EFF-07 |
| 81 | LoRA from scratch — the low-rank update derived, built, and merged back | EFF-08, EFF-09 |
| 82 | 🔍 QLoRA and the PEFT family — NF4, double quantization, adapters, prefix and prompt tuning | EFF-10, EFF-11 |
| 83 | FlashAttention and PagedAttention — IO-awareness and virtual memory for the KV cache | EFF-12, EFF-13 |
| 84 | Distillation and pruning — smaller by teaching, smaller by cutting | EFF-14, EFF-15 |
| 85 | The laptop that serves — CPU inference, ONNX, `torch.compile`, and offloading a model bigger than your RAM | EFF-16, EFF-17, EFF-18 |

#### Phase 13 — Post-training & alignment (Days 86–96)

| Day | Title | IDs closed |
| --- | --- | --- |
| 86 | 💥 A base model is not a chatbot — the completion/instruction gap, demonstrated on your own weights | POST-01 |
| 87 | SFT I — instruction datasets, synthesis, licences, and quality over quantity | POST-02, POST-03 |
| 88 | 💥 SFT II — chat templates and loss masking; **the bug that trains on the prompt** | POST-04, POST-05 |
| 89 | **The fine-tuning run** — Akshara learns to follow instructions, on free compute | POST-06 |
| 90 | 💥 Evaluating a fine-tune — did it learn the task, or the format? (**Silent Failure #5**) | POST-07 |
| 91 | Preference data — pairwise comparison, annotation noise, and the agreement ceiling | POST-08, POST-09 |
| 92 | 💥 Reward models — training one, then watching it get hacked | POST-10, POST-11 |
| 93 | RLHF with PPO — the four-model pipeline, the KL leash, and an honest account of why it is hard | POST-12, POST-13 |
| 94 | **DPO, built** — preference optimization without a reward model; ORPO/KTO/SimPO; online vs offline | POST-14, POST-15, POST-16 |
| 95 | 🅿️ RLAIF, constitutional AI, rejection sampling, best-of-n, GRPO and verifiable rewards | POST-17, POST-18 |
| 96 | 💥 The alignment failure lab — catastrophic forgetting, the alignment tax, over-refusal, sycophancy, mode collapse | POST-19, POST-20 |

#### Phase 14 — Reasoning & prompting (Days 97–103)

| Day | Title | IDs closed |
| --- | --- | --- |
| 97 | In-context learning — what actually happens when you give examples | REASON-01, REASON-02 |
| 98 | Prompting as engineering — instruction, context, format, and what a system prompt really privileges | REASON-03, REASON-04 |
| 99 | 💥 Chain of thought — why it works, and when the stated reasoning is a story told afterwards | REASON-05, REASON-06 |
| 100 | Self-consistency, decomposition and self-critique — and where self-critique reliably fails | REASON-07, REASON-08 |
| 101 | Reasoning models and thinking tokens — test-time compute as a scaling axis you pay for | REASON-09, REASON-10 |
| 102 | Verifiers, process rewards, and tools as the correctness escape hatch | REASON-11, REASON-12 |
| 103 | 💥 The prompting failure lab — sensitivity, position bias, lost-in-the-middle, and a first look at injection | REASON-13, REASON-14 |

#### Phase 15 — Knowledge & retrieval (Days 104–111)

| Day | Title | IDs closed |
| --- | --- | --- |
| 104 | What a model knows — parametric knowledge, memorization vs generalization, and the hallucination taxonomy | RAG-01, RAG-02 |
| 105 | Retrieval embeddings — contrastive training, hard negatives, bi-encoder vs cross-encoder | RAG-03, RAG-04 |
| 106 | 💥 Chunking — the decision that silently sets your recall ceiling | RAG-05 |
| 107 | Vector search — exact vs approximate, HNSW and IVF, and the recall/latency/memory triangle | RAG-06, RAG-07 |
| 108 | Hybrid retrieval — BM25 fused with dense, and the reranker that earns its latency | RAG-08, RAG-09 |
| 109 | **The RAG pipeline** — assembled end to end over Akshara | RAG-10 |
| 110 | Evaluating RAG — retrieval metrics and answer metrics are not the same measurement | RAG-11, RAG-12 |
| 111 | 💥 When RAG is the wrong tool — long context, fine-tuning, or a database query all along | RAG-13, RAG-14 |

#### Phase 16 — Evaluation (Days 112–119)

| Day | Title | IDs closed |
| --- | --- | --- |
| 112 | Why evaluation is the hardest problem — and why every shortcut has already been tried | EVAL-01 |
| 113 | Perplexity — computed on your own model, and everything it hides | EVAL-02, EVAL-03 |
| 114 | 💥 Benchmarks and contamination — what MMLU measures, and finding leakage in your own corpus | EVAL-04, EVAL-05 |
| 115 | Generation metrics — BLEU, ROUGE, BERTScore, and why they are weak | EVAL-06, EVAL-07 |
| 116 | 💥 LLM-as-judge — building one, then characterising its position, verbosity and self-preference biases | EVAL-08, EVAL-09 |
| 117 | Human evaluation — pairwise preference, Elo/Bradley-Terry, and rubrics that survive contact with raters | EVAL-10, EVAL-11, EVAL-12 |
| 118 | Evals are tests — the regression gate in CI | EVAL-13, OPS-09 |
| 119 | 💥 Calibration, abstention and significance — **Silent Failure #4**, and the error bar you must report | EVAL-14, EVAL-15, EVAL-16 |

#### Phase 17 — Multimodal (Days 120–128)

| Day | Title | IDs closed |
| --- | --- | --- |
| 120 | The general recipe — any modality becomes a sequence of vectors | MM-01 |
| 121 | Images as patches — the Vision Transformer, built; 2D position and variable resolution | MM-02, MM-03 |
| 122 | Contrastive pretraining — CLIP, InfoNCE, the shared space, and the limits of zero-shot | MM-04, MM-05 |
| 123 | **Vision–language models** — the projector that bridges into Akshara, and the two-stage training recipe | MM-06, MM-07 |
| 124 | 💥 Audio understanding — spectrograms, Whisper's encoder–decoder, and its hallucination on silence | MM-08, MM-09 |
| 125 | Audio tokenization — neural codecs and discrete speech units | MM-10 |
| 126 | Video — frames, temporal modelling, frame sampling, and the token-per-second cost problem | MM-11, MM-12 |
| 127 | 🅿️ Any-to-any and unified models; OCR, documents, and the "just read the screenshot" trap | MM-13, MM-16 |
| 128 | 💥 Multimodal hallucination and evaluation — grounding failures, and why measuring them is harder than text | MM-14, MM-15 |

#### Phase 18 — Other generative families (Days 129–140)

| Day | Title | IDs closed |
| --- | --- | --- |
| 129 | The family tree — autoregressive, VAE, GAN, flow, diffusion, and what each one optimizes | GEN-01 |
| 130 | Autoencoders and VAEs — the latent space, the ELBO, and the reparameterization trick | GEN-02, GEN-03 |
| 131 | 🅿️ GANs — the adversarial game, mode collapse, and why they faded | GEN-04, GEN-05 |
| 132 | Diffusion I — the forward noising process, and the closed form that makes it trainable | GEN-06 |
| 133 | Diffusion II — the reverse process, the denoiser, and the objective that is just a regression | GEN-07, GEN-08 |
| 134 | **Diffusion III** — a tiny diffusion model, trained on your own machine | GEN-09 |
| 135 | Samplers and schedules — DDIM, step count vs quality, and what the noise schedule controls | GEN-10, GEN-11 |
| 136 | Guidance — classifier guidance, classifier-free guidance, and the scale dial everyone turns too far | GEN-12, GEN-13 |
| 137 | Latent diffusion — the VAE compressor that made it affordable, and text conditioning by cross-attention | GEN-14, GEN-15 |
| 138 | Control and personalization — ControlNet, LoRA for images, DreamBooth, textual inversion | GEN-16, GEN-17 |
| 139 | Flow matching and rectified flow — what replaced DDPM, and why it is simpler | GEN-18 |
| 140 | 🅿️ Video and audio generation; and 💥 evaluating generative models — FID, CLIP score, and why human preference still wins | GEN-19, GEN-20, GEN-21 |

#### Phase 19 — Safety, security & ethics (Days 141–149)

| Day | Title | IDs closed |
| --- | --- | --- |
| 141 | The threat model — who attacks a generative system, at which surface, for what | SAFE-02 |
| 142 | Hallucination — the mechanism, the measurement, and the mitigations that actually move the number | SAFE-03, SAFE-04 |
| 143 | 💥 Prompt injection and jailbreaks — direct, indirect, the lethal trifecta, and why "instruct it not to" is not a defence | SAFE-05, SAFE-06, SAFE-07 |
| 144 | 💥 Memorization — training-data extraction, membership inference, and PII in your own corpus | SAFE-08, SAFE-09 |
| 145 | 💥 Poisoning and the supply chain — backdoors, pickle deserialization, and model provenance | SAFE-10, SAFE-11 |
| 146 | Bias and fairness — where it enters, and how to measure it rather than deplore it | SAFE-12, SAFE-13 |
| 147 | Copyright, licensing and consent — auditing what Akshara was actually trained on | SAFE-14 |
| 148 | Watermarking, provenance and deepfakes — C2PA, and the honest limits of detection | SAFE-15, SAFE-16 |
| 149 | Guardrails, the model card, the regulatory map 🅿️, and the release decision | SAFE-17, SAFE-18, SAFE-19, SAFE-20 |

#### Phase 20 — Serving & operations (Days 150–157)

| Day | Title | IDs closed |
| --- | --- | --- |
| 150 | Model formats and loading — safetensors, GGUF, memory-mapped weights, and the pickle you must not trust | SERVE-01, SERVE-02 |
| 151 | **An inference server from scratch** — the request lifecycle, streaming over SSE, and cancellation | SERVE-03, SERVE-04 |
| 152 | 🔍 Now compare — vLLM, TGI, llama.cpp, Ollama; what they do that yours does not | SERVE-05, SERVE-06 |
| 153 | Batching and scheduling in production — continuous batching, admission control, backpressure | SERVE-07, SERVE-08 |
| 154 | 💥 Caching — prefix caching, semantic caching, and the day it returns the wrong answer | SERVE-09, SERVE-10 |
| 155 | Observability — latency percentiles, tokens/s, cost per request, and tracing one generation end to end | SERVE-11, SERVE-12, OPS-10 |
| 156 | Registry, versioning and the container — which weights answered that request? | SERVE-13, SERVE-14 |
| 157 | Capacity planning and build-vs-buy — sizing a deployment from a latency target, with the arithmetic shown | SERVE-15, SERVE-16 |

#### Phase 21 — Capstone (Days 158–161)

| Day | Title | IDs closed |
| --- | --- | --- |
| 158 | Capstone I — Akshara end to end, cold: corpus → tokenizer → pretrain → SFT → DPO → quantize → serve | — |
| 159 | Capstone II — the eval suite run in full, the model card written, the demo script | — |
| 160 | Capstone III — the interview drill: every ADR, every number, every trade defended out loud | — |
| 161 | Final gate — whole-system audit, the retrospective, and what you would do differently with a budget | — |

> Days 158–161 close no new IDs by design: they are integration days. Their gate is the whole-system
> demo, and `docs/TRACEABILITY.md` must show **zero open IDs** before Day 158 begins.

---

### 24.3 The Paper Roster — which days rest on which papers

**Principle 21: a paper the field rests on is taught, not cited.** Every paper below gets **its own
part**, in its day's paper section, under the contract in §25.10.

> ⚠️ **Papers are listed by title and year, never by identifier — on purpose.** Principle 8 forbids
> writing a number from memory, and an arXiv id is a number. The id, the exact title and the venue
> are **resolved live on the day the part is written**, and the row lands in `docs/PAPERS.md` before
> a word of the part is written. A plan that shipped ninety remembered identifiers would be teaching
> the opposite of what §25.10 exists to teach.
>
> This roster is the **floor, not the ceiling.** A day may add a paper it turns out to need; adding
> one is a `docs/PAPERS.md` row and a part, not an amendment. **Removing** one is an amendment,
> because it changes what the curriculum claims to cover.

Where a day's row says **"the day"**, the paper is not an appendix to the teaching — it *is* the
day, and the paper parts span several sections (§25.10.1).

#### Book I — Ground

| Day | Paper (title, year) | Why this day |
| --- | --- | --- |
| 8 | *Adam: A Method for Stochastic Optimization* (2014) | The optimizer every run in this plan uses |
| 12 | *Neural Machine Translation of Rare Words with Subword Units* (2015) | BPE — the algorithm you write by hand that day |
| 15 | *Japanese and Korean Voice Search* (2012) | WordPiece, and the `##` convention |
| 15 | *Subword Regularization* (2018) | The Unigram LM tokenizer — a *probabilistic* vocabulary |
| 15 | *SentencePiece: A simple and language independent subword tokenizer* (2018) | The implementation everyone actually ships |
| 19 | *Efficient Estimation of Word Representations in Vector Space* (2013) | word2vec — what "embedding" meant before contextual |
| 19 | *GloVe: Global Vectors for Word Representation* (2014) | The counting-based alternative, and why it lost |
| 21 | *How Contextual are Contextualized Word Representations?* (2019) | Anisotropy — why raw LM states disappoint as embeddings |

#### Book II — The Machine

| Day | Paper (title, year) | Why this day |
| --- | --- | --- |
| 26 | *A Neural Probabilistic Language Model* (2003) | The MLP language model you build that day, twenty years early |
| 27 | *Long Short-Term Memory* (1997) | The gate that keeps a gradient alive |
| 27 | *Learning Phrase Representations using RNN Encoder–Decoder* (2014) | GRU, and the encoder–decoder framing that outlived it |
| 29 | *Neural Machine Translation by Jointly Learning to Align and Translate* (2014) | **Attention, before transformers** — the paper that invented the soft lookup |
| 32 | *A Mathematical Framework for Transformer Circuits* (2021) | Induction heads — what a head specialises in, and how anyone knows |
| 34 | *Efficient Streaming Language Models with Attention Sinks* (2023) | Attention sinks — the first token everything attends to |
| 35 | *Gaussian Error Linear Units (GELUs)* (2016) | The activation that replaced ReLU in transformers |
| 35 | *GLU Variants Improve Transformer* (2020) | SwiGLU, and the honest "we offer no explanation" in its conclusion |
| 36 | *Deep Residual Learning for Image Recognition* (2015) | The residual connection, from the paper that made depth trainable |
| 37 | *Layer Normalization* (2016) | What is normalized, over which axis |
| 37 | *Root Mean Square Layer Normalization* (2019) | RMSNorm — the term that turned out not to matter |
| 37 | *On Layer Normalization in the Transformer Architecture* (2020) | Pre-norm vs post-norm: the argument that moved the whole field |
| 40 | *Attention Is All You Need* (2017) | **the day** — read end to end, against what people actually build now |
| 42 | *Convolutional Sequence to Sequence Learning* (2017) | Learned positional embeddings, and where the idea came from |
| 43 | *RoFormer: Enhanced Transformer with Rotary Position Embedding* (2021) | RoPE — the code you write that day |
| 43 | *Train Short, Test Long: Attention with Linear Biases* (2021) | ALiBi's different bet on extrapolation |
| 44 | *YaRN: Efficient Context Window Extension of Large Language Models* (2023) | Context extension, and what position interpolation costs |
| 44 | *Longformer: The Long-Document Transformer* (2020) | Sliding-window and sparse attention patterns |
| 45 | *BERT: Pre-training of Deep Bidirectional Transformers* (2018) | Encoder-only and masked language modelling |
| 46 | *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer* (2019) | T5, and the encoder–decoder case |
| 47 | *Language Models are Unsupervised Multitask Learners* (2019) | GPT-2 — the argument for decoder-only |
| 48 | *Fast Transformer Decoding: One Write-Head is All You Need* (2019) | MQA, and the KV cache that motivated it |
| 48 | *GQA: Training Generalized Multi-Query Transformer Models* (2023) | The compromise everyone shipped |
| 49 | *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer* (2017) | MoE routing, before it was fashionable |
| 49 | *Switch Transformers* (2021) | Load balancing, capacity factors, and the simplification that made MoE work |
| 50 | 🅿️ *Mamba: Linear-Time Sequence Modeling with Selective State Spaces* (2023) | What selective state spaces actually claim |
| 54 | *Understanding the difficulty of training deep feedforward neural networks* (2010) | Xavier/Glorot init — why scale matters |
| 54 | *Delving Deep into Rectifiers* (2015) | He init, and the ReLU correction |
| 57 | *Mixed Precision Training* (2017) | fp16, loss scaling, and the master weights |
| 57 | *Training Deep Nets with Sublinear Memory Cost* (2016) | Gradient checkpointing — compute traded for memory |
| 61 | *The Pile: An 800GB Dataset of Diverse Text* (2020) | What a pretraining corpus is actually made of |
| 61 | *The RefinedWeb Dataset for Falcon LLM* (2023) | Filtering alone beats curation — the result that changed data practice |
| 62 | *Deduplicating Training Data Makes Language Models Better* (2021) | Why dedup is not housekeeping |
| 62 | *Documenting Large Webtext Corpora* (2021) | What is actually in a web corpus, including the benchmarks |
| 65 | *Scaling Laws for Neural Language Models* (2020) | The power law, and the claim it made |
| 65 | *Training Compute-Optimal Large Language Models* (2022) | Chinchilla — the correction, and the arithmetic you use to size Akshara |
| 66 | 🅿️ *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models* (2019) | The distributed arithmetic you must be able to do without running it |
| 67 | 🅿️ *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer* (2022) | muP — tune small, run large |
| 68 | *Emergent Abilities of Large Language Models* (2022) | The claim |
| 68 | *Are Emergent Abilities of Large Language Models a Mirage?* (2023) | The rebuttal — read as a pair, which is the point |

#### Book III — The Runtime

| Day | Paper (title, year) | Why this day |
| --- | --- | --- |
| 70 | *On the Properties of Neural Machine Translation: Encoder–Decoder Approaches* (2014) | Beam search, and where it came from |
| 71 | *The Curious Case of Neural Text Degeneration* (2019) | Nucleus sampling — and the best demonstration in the field of why likelihood is not quality |
| 75 | *Efficiently Scaling Transformer Inference* (2022) | Prefill vs decode, and the latency arithmetic |
| 76 | *Efficient Guided Generation for Large Language Models* (2023) | Finite-state constrained decoding |
| 77 | 🅿️ *Fast Inference from Transformers via Speculative Decoding* (2022) | Draft-and-verify |
| 77 | 🅿️ *Orca: A Distributed Serving System for Transformer-Based Generative Models* (2022) | Continuous batching — the idea that made serving cheap |
| 79 | *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale* (2022) | The outlier features that make naive int8 fail |
| 80 | *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers* (2022) | Calibration-based PTQ |
| 80 | *AWQ: Activation-aware Weight Quantization* (2023) | The salient-weight argument |
| 81 | *LoRA: Low-Rank Adaptation of Large Language Models* (2021) | The update you derive and build that day |
| 82 | *QLoRA: Efficient Finetuning of Quantized LLMs* (2023) | NF4, double quantization, paged optimizers |
| 82 | *Prefix-Tuning: Optimizing Continuous Prompts for Generation* (2021) | The PEFT alternative |
| 82 | *The Power of Scale for Parameter-Efficient Prompt Tuning* (2021) | Prompt tuning, and when it catches up |
| 83 | *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness* (2022) | Exact, not approximate — the distinction everyone gets wrong |
| 83 | *Efficient Memory Management for Large Language Model Serving with PagedAttention* (2023) | vLLM, and virtual memory for the KV cache |
| 84 | *Distilling the Knowledge in a Neural Network* (2015) | Soft labels and the temperature |
| 84 | *SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot* (2023) | Pruning at scale |
| 84 | 🅿️ *The Lottery Ticket Hypothesis* (2018) | Why the sparsity result is more interesting than it looks |

#### Book IV — The Behaviour

| Day | Paper (title, year) | Why this day |
| --- | --- | --- |
| 87 | *Self-Instruct: Aligning Language Models with Self-Generated Instructions* (2022) | Where synthetic instruction data comes from |
| 87 | *LIMA: Less Is More for Alignment* (2023) | Quality over quantity, with the evidence |
| 91 | *Deep Reinforcement Learning from Human Preferences* (2017) | Pairwise comparison as the annotation primitive |
| 92 | *Scaling Laws for Reward Model Overoptimization* (2022) | Reward hacking, measured |
| 93 | *Proximal Policy Optimization Algorithms* (2017) | The optimizer inside RLHF |
| 93 | *Training language models to follow instructions with human feedback* (2022) | InstructGPT — the four-model pipeline, end to end |
| 94 | *Direct Preference Optimization: Your Language Model is Secretly a Reward Model* (2023) | The derivation you work through that day |
| 94 | *ORPO: Monolithic Preference Optimization without Reference Model* (2024) | What it removes |
| 94 | *KTO: Model Alignment as Prospect Theoretic Optimization* (2024) | Unpaired preference data |
| 94 | *SimPO: Simple Preference Optimization with a Reference-Free Reward* (2024) | The length-bias correction |
| 95 | 🅿️ *Constitutional AI: Harmlessness from AI Feedback* (2022) | RLAIF |
| 95 | *DeepSeekMath: Pushing the Limits of Mathematical Reasoning* (2024) | GRPO, and RL on verifiable rewards |
| 96 | *An Empirical Study of Catastrophic Forgetting in Large Language Models* (2023) | The alignment tax, measured rather than asserted |
| 97 | *Language Models are Few-Shot Learners* (2020) | GPT-3 — in-context learning as a phenomenon |
| 97 | *In-context Learning and Induction Heads* (2022) | The mechanism underneath it |
| 99 | *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* (2022) | Why generating steps helps a next-token predictor |
| 99 | *Language Models Don't Always Say What They Think* (2023) | Faithfulness — the paper that should make you cautious about CoT |
| 100 | *Self-Consistency Improves Chain of Thought Reasoning* (2022) | Majority vote over samples |
| 101 | *Scaling LLM Test-Time Compute Optimally* (2024) | Test-time compute as a scaling axis |
| 102 | *Let's Verify Step by Step* (2023) | Process rewards vs outcome rewards |
| 103 | *Lost in the Middle: How Language Models Use Long Contexts* (2023) | Position bias, with the U-shaped curve |
| 104 | *Extracting Training Data from Large Language Models* (2020) | What parametric knowledge actually stores |
| 105 | *Dense Passage Retrieval for Open-Domain Question Answering* (2020) | The bi-encoder, and hard negatives |
| 105 | *Sentence-BERT* (2019) | Why an LM's hidden state is not a sentence embedding |
| 107 | *Efficient and robust approximate nearest neighbor search using HNSW graphs* (2016) | The index everything uses |
| 108 | *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction* (2020) | Late interaction, between bi- and cross-encoder |
| 109 | *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (2020) | The paper the acronym comes from — and how different it is from what people call RAG |
| 110 | *RAGAS: Automated Evaluation of Retrieval Augmented Generation* (2023) | Separating retrieval metrics from answer metrics |
| 113 | *Perplexity — a measure of the difficulty of speech recognition tasks* (1977) | Where the metric came from, and what it assumed |
| 114 | *Measuring Massive Multitask Language Understanding* (2020) | MMLU — what it does and does not measure |
| 114 | *Training Verifiers to Solve Math Word Problems* (2021) | GSM8K |
| 114 | *Evaluating Large Language Models Trained on Code* (2021) | HumanEval, and pass@k |
| 115 | *BLEU: a Method for Automatic Evaluation of Machine Translation* (2002) | The metric everyone still reports and nobody trusts |
| 115 | *BERTScore: Evaluating Text Generation with BERT* (2019) | Model-based metrics |
| 116 | *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (2023) | The judge, and its measured biases |
| 119 | *On Calibration of Modern Neural Networks* (2017) | Why confidence stopped meaning anything |
| 141 | *Universal and Transferable Adversarial Attacks on Aligned Language Models* (2023) | GCG — jailbreaks as optimization, not wordplay |
| 143 | *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection* (2023) | The indirect-injection threat model |
| 144 | *Quantifying Memorization Across Neural Language Models* (2022) | How much a model memorises, as a function of what |
| 144 | *Membership Inference Attacks Against Machine Learning Models* (2016) | The original attack |
| 145 | *Poisoning Web-Scale Training Datasets is Practical* (2023) | Why the supply chain is a real threat and not a hypothetical |
| 146 | *On the Dangers of Stochastic Parrots* (2021) | The critique the field argued about, read rather than summarised |
| 146 | *BBQ: A Hand-Built Bias Benchmark for Question Answering* (2022) | Measuring bias rather than deploring it |
| 148 | *A Watermark for Large Language Models* (2023) | Watermarking, and its fragility |
| 149 | *Model Cards for Model Reporting* (2018) | The artifact you write that day |

#### Book V — Beyond text

| Day | Paper (title, year) | Why this day |
| --- | --- | --- |
| 121 | *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale* (2020) | ViT — the patch embedding you build |
| 122 | *Learning Transferable Visual Models From Natural Language Supervision* (2021) | CLIP, InfoNCE, and the shared space |
| 123 | *Visual Instruction Tuning* (2023) | LLaVA — the projector, and the two-stage recipe |
| 123 | *Flamingo: a Visual Language Model for Few-Shot Learning* (2022) | The other way to bridge modalities |
| 124 | *Robust Speech Recognition via Large-Scale Weak Supervision* (2022) | Whisper, and its hallucination on silence |
| 125 | *High Fidelity Neural Audio Compression* (2022) | EnCodec — discrete audio tokens |
| 128 | *Evaluating Object Hallucination in Large Vision-Language Models* (2023) | Multimodal grounding failure, measured |
| 130 | *Auto-Encoding Variational Bayes* (2013) | The VAE, the ELBO, the reparameterization trick |
| 131 | 🅿️ *Generative Adversarial Networks* (2014) | The adversarial game |
| 133 | *Denoising Diffusion Probabilistic Models* (2020) | **the centre of the diffusion phase** — the objective that is just a regression |
| 133 | *Deep Unsupervised Learning using Nonequilibrium Thermodynamics* (2015) | The original diffusion paper, five years early and ignored |
| 135 | *Denoising Diffusion Implicit Models* (2020) | DDIM — deterministic sampling, fewer steps |
| 136 | *Diffusion Models Beat GANs on Image Synthesis* (2021) | Classifier guidance |
| 136 | *Classifier-Free Diffusion Guidance* (2022) | The dial everyone turns too far |
| 137 | *High-Resolution Image Synthesis with Latent Diffusion Models* (2021) | The VAE compressor that made it affordable |
| 138 | *Adding Conditional Control to Text-to-Image Diffusion Models* (2023) | ControlNet |
| 138 | *DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation* (2022) | Personalization, and its failure modes |
| 139 | *Flow Matching for Generative Modeling* (2022) | What replaced DDPM, and why it is simpler |
| 140 | *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium* (2017) | FID — the metric, and what it is blind to |

#### 24.3.1 The count, and what it means for a day

**130 papers across 88 of the 162 days.** Most paper-carrying days carry one or two; Day 40 is a
paper end to end, and Days 15, 43, 94 and 114 carry three or more because those ideas only make
sense against each other. Seventy-four days carry none.

This is the single largest addition to the length of the curriculum, and it is the one most worth
paying for (§25.10.4). A day with two paper parts is not a day with two extra pages of citation —
it is a day where the reader learns the argument, the evidence, and what the evidence does not
support, which is the difference between knowing a result and being able to use one.

**Days with no papers are normal and are not a defect.** Day 0 is a toolchain. Day 53 is padding and
attention masks — a mechanism the field never wrote a paper about, and one that costs more engineers
more days than most of the papers above. `papers: []` in a hub is an explicit statement that the day
was checked, not that it was skipped.

---

## 25 · 📐 The Depth Contract — how a day is written

> **Why this section exists.** The default failure mode of a technical curriculum is a long page per
> topic. It looks thorough. It is not: a reader cannot revisit *one* idea without re-reading four,
> there is no artifact that distinguishes a thinly-covered subtopic from a missing one, and a time
> estimate at the top silently authorises the worst edit in technical writing — cutting the
> explanation because the document is getting long.
>
> A day here is **one hub plus one document per subtopic**, every document written from zero prior
> knowledge through to how the idea is used in a real system. This section states exactly what
> "covered properly" means, so it can be reviewed by reading and partly checked by a script. It is
> Principles 16, 17, 18 and 20 made concrete.

### 25.1 The four commitments

**One idea per document.** A subtopic that cannot be read alone, understood without scrolling past a
different subtopic, and explained back out loud is not one subtopic — it is several, badly stacked.
If a document needs the word "also" to introduce its second half, it is two documents.

**No clocks.** Nothing in a day folder carries a time estimate, an "estimated hours" field, a "this
should take 90 minutes", or a suggested pace. **Content is never trimmed to fit a schedule**, and a
day is never declared finished because a duration elapsed.

> **What "no clocks" does *not* ban.** A *measured* duration is data, not a clock: "the run took
> 43 minutes on a T4, seed 1337", a GPU-minute budget in a hub's §6, a p95 latency in milliseconds,
> a tokens-per-second throughput. Those are Principle 8 doing its job. The ban is on estimates aimed
> at the reader's schedule — anything that tells them how fast they ought to be going, and thereby
> licenses trimming the explanation. `./m depth` distinguishes the two.

**Zero to production, in one document.** Each part starts where a reader who has never heard of the
idea can stand, and ends where a working professional stands: how the idea appears in a real system,
what a research engineer does differently from the tutorial version, what fails at scale, and what a
reviewer or an interviewer will probe.

**Every number has a provenance.** Any empirical claim in any part is either *measured here* — with
hardware, seed and date — or *cited* with an arXiv id and section. Never recalled (Principle 8).

### 25.2 The folder shape

```
days/day-NNN-<day-slug>/
├── LESSON.md          # the hub — orientation, story, part map, build brief, eval, budget, ledger
├── CHECKLIST.md       # the definition of done; ./m done NNN refuses to commit until ticked
├── parts/             # THE TEACHING — one document per subtopic
│   ├── 01-<slug>/     # section 1 — two digits, zero-padded, then what the section is about
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   ├── 02-<slug>/
│   │   └── 2.1-<slug>.md
│   └── 03-<slug>/
│       └── 3.1-<slug>.md
└── lab/               # created by ./m scaffold NNN; the learner's own scratch code
```

`parts/` is mandatory. **A day with no `parts/` directory is, by definition, not written** — the
tracker reports it as pending and the phase gate cannot go green.

**Day numbers are three digits, zero-padded** — `day-007-numerical-reality`, `day-143-injection`.
The plan runs past 99, and `day-9` sorting after `day-100` in every file listing is a papercut paid
162 times.

**Every folder name carries its subject.** A number alone is an address, not an answer:

| Folder | Shape | Slug from | Length |
| --- | --- | --- | --- |
| the day | `day-NNN-<slug>` | the hub's `title` frontmatter, minus articles | 1–4 words |
| a section | `NN-<slug>` | the section's heading in the hub's §2 map | 1–3 words |

**The number is the identity; the slug is a label on it.** Every tool resolves a day by number and
accepts whatever slug follows, so a folder can be renamed to a better slug at any time without
breaking `./m`, `depth_check.py`, `tracker.py` or `trace.py`.

**Every part lives inside its section's folder.** A part document is never loose in `parts/`, and
the folder number must agree with the number before the dot in the filename:
`parts/02-attention/2.3-<slug>.md` is correct; `parts/02-attention/3.1-<slug>.md` is a bug the depth
check rejects.

**Links between parts are relative.** A sibling is `1.2-<slug>.md`; another section is
`../01-<slug>/1.5-<slug>.md`; the hub is `../../LESSON.md`.

### 25.3 The numbering rule — what `1.1` and `2.3` mean

Part numbers are **`<section>.<subtopic>`**, both scoped to the day.

- The **section** groups subtopics that share one mental model — usually one curriculum ID, one
  stage of a pipeline, or one phase of a mechanism.
- The **subtopic** is the reading order inside that section. It starts at `1`, never `0`, and has no
  gaps.

The hub's §2 map declares what each section *is*. A typical two-ID day:

| Section | Means | Example subtopics |
| --- | --- | --- |
| **1.x** | the day's first ID | `1.1` what it is · `1.2` how it behaves · `1.3` where it bites |
| **2.x** | the day's second ID | `2.1` … `2.2` … |
| **3.x** | the synthesis — the two IDs meeting | `3.1` the trap visible only when both are true |

An architecture day uses sections as *forward-pass stages*: `1.x` the shape of the input, `2.x` the
operation, `3.x` the backward pass, `4.x` the failure surface. A training day uses them as
*loop position*. **The grouping must be stated in the hub;** an unexplained numbering is a bug.

### 25.4 What a part document must contain

Every file in `parts/` carries all eleven of these, **in this order**. Two of them — *Shapes* and
*Line by line* — are conditional; the other nine are unconditional.

| # | Section | The rule |
| --- | --- | --- |
| 1 | **frontmatter** | `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next`. Machine-read. **No duration field of any kind** (Principle 17). |
| 2 | **One-line answer** | The subtopic's claim in a single sentence, before anything else. A reader who reads only this line has learned something true. |
| 3 | **The story** | A concrete scene before any abstraction: a person, a machine, a failure, a decision. It comes **first**, in plain words, with **no jargon at all**. It is the hook the definition hangs on, not decoration. |
| 4 | **The idea in plain language** | The concept itself, assuming the reader has never met it. Every term defined the first time it appears — **including terms from earlier days**, with a link to the part that introduced them. No code. |
| 5 | **Why Akshara needs it** | The concrete later day that breaks without this. *"You meet this again on Day 88, where a chat template written the other way silently trains the model on its own prompt"* is the shape. Never "this is important". |
| 6 | **The mechanism** | How it actually works: the runnable code, the derivation written out, or the diagram. Nothing skipped as "obvious". Mermaid whenever the concept is spatial, sequential, or a state machine. |
| 7 | **Shapes** ⟵ *conditional* | **Required whenever the part introduces or transforms a tensor.** A table with one row per tensor: name, shape in symbols (`(B, T, C)`), shape with this part's concrete numbers, and what the axes *mean*. More transformer bugs are shape bugs than algorithm bugs; a document that leaves the reader to infer an axis has taught them something they cannot debug (Principle 20). A part with no tensors omits this section and `./m depth` does not ask for it. |
| 8 | **Line by line** ⟵ *conditional* | Every non-obvious token of every code block, explained — and *why it is that line and not another*. Written as a `**Line by line:**` list **immediately after each code block**. Blocks showing error output, a bare check command, or a diagram are exempt. **An unexplained line is a bug in the doc.** A part carrying no code needing a walkthrough omits this section. |
| 9 | **When it breaks** | The **real** error text, reproduced verbatim — the traceback, the shape-mismatch message, the CUDA OOM, the NaN. What it says, what it actually means, and the smallest fix. For this field it also covers the *silent* breakages (§6): what the wrong-but-running version looks like, and the check that catches it. |
| 10 | **In production** | Where this idea shows up in a real system and what changes there: the version a research engineer writes instead of the teaching version, what degrades at scale, the failure that only appears with real data, the review comment, and the question an interviewer asks to find out whether you have actually used it. **Not optional. This is the section that makes the document professional rather than introductory.** |
| 11 | **Check yourself** | One command the reader can run right now — **which prints a number, not just a pass** — plus one question they must answer **out loud** without scrolling up. |

Four further rules that have no section of their own:

- **The one-idea test.** If a part needs "also" to introduce its second half, split it.
- **The standalone test.** A part must be readable cold. If it depends on an earlier idea, **name
  that part and link it** — never assume the reader remembers Day 30 on Day 121.
- **The no-shortcut test.** "For now, just accept that" is banned unless it links forward to the part
  that explains it. **A deferred explanation must have an address.**
- **The provenance test.** Every number in the part is measured-here or cited. No exceptions.

#### 25.4.1 Akshara's five additional part rules

These come from Principles 6, 7, 8, 13 and §6, and apply on top of the eleven sections:

1. **Never invent an API.** Any part using a library symbol names the doc page or source file
   checked **for the pinned version**, inline, next to the code: *"Verified against
   `torch` 2.x `nn/functional.py::scaled_dot_product_attention` on YYYY-MM-DD."*
2. **Never invent a version.** Any part that installs something states the version it verified and
   how, or leaves a `TODO` containing **the exact lookup command**. The row lands in
   `docs/PACKAGES.md` the same day. Any part that downloads a model or dataset pins the **revision
   SHA** and records it in `docs/MODELS.md` / `docs/DATASETS.md`.
3. **Never invent a number.** Measured-here (hardware, seed, date) or cited (arXiv id, section).
4. **Name the silent failure.** Any part touching one of the five (§6) says which one it is avoiding
   and how the reader would detect it. A reader who has been following tutorials needs to be told.
5. **State the compute tier.** Any part that runs something says whether it is T0 (CPU), T1 (free
   notebook GPU) or T2 (🅿️ parked, cannot be done at $0), and what the T0 version proves.

### 25.5 What the hub (`LESSON.md`) must contain

The hub is **orientation and assembly, never the teaching itself**. It carries no `Line by line:`
walkthrough and no `Shapes` table — those live in the parts. Required, in this order:

1. **frontmatter** — `day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
   `plan_version`, `parts` (the count), `papers` (the list, from §24.3 — **`papers: []` when the day
   rests on none**; an empty list is a decision, a missing key is an oversight), `compute_tier`,
   `generated`, `status`, `lab_scaffolded`, `commit`.
2. **yesterday / today / tomorrow** — one line each, as a blockquote. No time estimate.
3. **`## §1 Where we are`** — the day's whole idea as a scene and an analogy, in plain language,
   before any code and before any jargon.
4. **`## §2 The map`** — a table of every part: number, linked title, what it answers, and its
   `level`. Grouped by section, with **one line saying what each section means for this day**.
   **No minutes column, ever.**
5. **`## §3 Setup — run this`** — every `mkdir`, `touch`, `uv add <pkg>==<exact>` the day needs,
   pinned, with the version verified that day. Plus the notebook link if the day is T1.
6. **`## §4 Build brief`** — the files to create, with `TODO(me)` markers left **unsolved**.
7. **`## §5 The eval that must be able to fail`** — the check that is RED before the TODOs are done
   (Principle 11).
8. **`## §6 Compute budget`** — the tier (T0/T1/T2), and for T1 days the GPU-minutes and session
   count. `0` is an answer; state it.
9. **`## §7 Traps`** — the mistakes that eat an evening, including the named Silent Failure (§6) if
   the day touches one.
10. **`## §8 Verify before you code`** — the live URLs actually fetched on the day of writing:
    library doc pages, the arXiv ids cited, the model/dataset cards read (Principles 6, 7, 8).
11. **`## §9 Say it in an interview`** — one paragraph, spoken voice, honest, tied to what was built
    and to a number you measured.
12. **`## §10 Done when`** — pointer to `CHECKLIST.md`. Defined by understanding and green checks,
    **never by elapsed time**.
13. **`## §11 Ledger & commit`** — the verbatim snippets that end every day: the `PROGRESS.md` row,
    any `PACKAGES.md` / `DATASETS.md` / `MODELS.md` / `RUNS.md` rows, and the commit message
    `day NNN: <title> — closes <IDs>`. **The hub ends with these.**

### 25.6 The `level` field — how a day climbs

| `level` | The reader at the end of this part |
| --- | --- |
| `foundation` | Knows what the thing *is* and could define it to someone else without using the word itself. |
| `working` | Can implement or use it correctly on their own problem, and recognises its error messages on sight. |
| `production` | Knows what changes in a real system — scale, memory, throughput, data quality, review — and can defend the choice with arithmetic. |

A day that is all `foundation` is a tutorial. A day that opens at `production` has skipped the
reader. Most days run `foundation → working → production`.

### 25.7 How finely to split

Split by **idea boundaries, never by length or by pace**. A part is finished when its one idea is
fully explained — *including its production face* — and not before.

| Day kind | Split by |
| --- | --- |
| `setup` | one tool, one file, or one command per part |
| `math` | one definition → one derivation → one implementation → one failure of intuition |
| `build` (1 ID) | mechanism → shapes → behaviour → edge case → failure mode → production use |
| `build` (2–3 IDs) | one section per ID, plus a synthesis section where they meet |
| `compare` 🔍 | one dimension of difference per part (correctness, speed, API surface, what they handle that you don't) |
| `run` | one stage of the run per part: config → launch → watch → interpret → what went wrong |
| `concept` | one claim per part, each with its evidence |
| `gate` | one acceptance criterion per part |
| `capstone` | one component per part, in build order |

There is deliberately **no target part count and no target length**. If a subject needs five parts it
gets five; if it needs twenty-four it gets twenty-four. The only wrong answers are a part that
carries two ideas and a part that stops before production.

**Every day carries at least one part whose subject is a deliberate failure.** Breaking the thing on
purpose, at `production` level, is the whole point of that document.

### 25.8 What "in depth" is not

The failure modes this contract exists to prevent, stated so they can be caught in review:

- **Splitting without deepening.** Cutting one long page into six shorter ones changes nothing. Each
  part must **gain** the story, the shapes, the mechanism, the failure text, the production face and
  the check it never had.
- **Summary in place of explanation.** *"This line applies the mask"* is a caption. *"`masked_fill`
  writes `-inf` **before** the softmax, not zero after it, because a zero probability has to come out
  of the normalization — zeroing afterwards leaves the other probabilities summing to less than
  one"* is an explanation.
- **Stopping at the toy example.** A part that shows attention working on an 8-token sequence and
  never says what happens at 8192 has taught half the subject.
- **Assuming the previous day.** Each part names its prerequisite and links it. 162 days is long
  enough that Day 30 is genuinely forgotten by Day 121.
- **Code without failure.** Every mechanism has a matching *When it breaks* with the **actual** error
  string — and, for this field, the *silent* failure too.
- **Numbers without provenance.** "LoRA typically uses rank 8–64" is a rumour. "rank 16 on this
  model, on this data, cost 0.3 points of eval accuracy versus a full fine-tune, seed 1337,
  2026-08-25" is a result.
- **Shapes left to the reader.** If a tensor changes shape and the document does not say to what,
  the document has created a bug it will not be around to fix.
- **Trimming to fit.** Cutting an explanation because the day "is getting long" is the one edit this
  format forbids outright. **Split it into another part instead.**
- **Solved reps.** `TODO(me)` stays `TODO(me)`.

### 25.9 Enforcement

`scripts/depth_check.py`, run as `./m depth [NNN]`, is the machine-readable half of this contract.
It fails on:

- a missing `parts/` directory;
- a day folder that is not `day-NNN-<slug>` with a three-digit number and a slug;
- a part loose in `parts/` instead of inside a section folder;
- a section folder that is not two zero-padded digits plus a slug;
- a part whose section folder disagrees with the number in its filename;
- a filename that does not match `<section>.<subtopic>-<slug>.md`;
- a gap in the section or subtopic numbering;
- any of the nine unconditional part sections missing or out of contract order;
- a code block with no `Line by line:` walkthrough following it;
- a part that mentions a tensor shape in code but carries no `## Shapes` section;
- a `level` outside `foundation` · `working` · `production`;
- **any reader-directed time estimate anywhere in a day folder** (Principle 17) — an "estimated
  hours" field, a `duration:` key, a "should take about 40 minutes", an "allow two hours", a
  "quick detour", a suggested pace;
- a hub that carries teaching, or whose §2 map does not link every part on disk;
- a `parts:` frontmatter count that disagrees with the directory;
- a hub with no `papers:` frontmatter key (`papers: []` is the answer when a day rests on none —
  an empty list is an explicit decision, a missing key is an oversight);
- a hub declaring N papers whose `parts/` holds a different number of `kind: paper` parts (§25.10.3
  rule 1: one paper, one part);
- a `kind: paper` part missing `paper_title`, `paper_year`, or an identifier
  (`paper_arxiv` or `paper_venue`);
- a `kind: paper` part missing `## The paper in one small project`, `## What the paper showed` or
  `## What came after`, or carrying them out of contract order (§25.10.2);
- a `## The paper in one small project` section containing no code block — a project you cannot run
  is a description (§25.10.2);
- a missing `CHECKLIST.md`.

What it **cannot** check is whether an explanation is any good. That is what §25.8 is for, and it is
reviewed by reading. `docs/TRACKER.md` reports the part count of every written day, so a thin day is
visible from the progress table alone.

`scripts/trace.py` is the ID-level check: it reads each `days/day-NNN-<slug>/LESSON.md` against §24
and regenerates `docs/TRACEABILITY.md`. **An open ID in a completed phase is a bug.**

### 25.10 Paper parts — how a paper is taught

**Principle 21: a paper the field rests on is taught, not cited.**

Roughly ninety days in this plan rest on a specific published result (§24.3). The tempting way to
handle that is a citation — *"scaled dot-product attention (arXiv:1706.03762)"* — and it is the
citation equivalent of an unexplained line of code. It tells the reader the idea has a source and
teaches them nothing about it. Meanwhile "read the paper" is advice nobody acts on, because the
reader has no idea which parts of a nine-page PDF matter or what the notation means.

So: **a paper gets a part.**

#### 25.10.1 Where paper parts live

A day that rests on one or more papers carries a **dedicated section, last in the day**, holding
**one part per paper**:

```
days/day-043-rope-and-alibi/
├── parts/
│   ├── 01-position-by-rotation/     # the teaching: RoPE, in your own words and code
│   ├── 02-alibis-different-bet/     # the teaching: ALiBi
│   └── 03-the-papers/               # ⟵ the paper section, one part per paper
│       ├── 3.1-roformer-rope.md
│       └── 3.2-train-short-test-long-alibi.md
```

The section comes **last on purpose.** The mechanism is taught first, in plain language and running
code, so that when the reader opens the paper they already understand the idea and are reading for
*how it was argued and what it cost* — which is the skill this section is actually building. A
reader sent to the paper first learns to be intimidated by papers.

The section is named `NN-the-papers/` (or `NN-the-paper/` when there is one). Where a whole day *is*
a paper — Day 40, reading the original transformer paper — the paper parts are the day, spread over
several sections, and §25.10.2 still governs each one.

Each paper part's small project (§25.10.2 section 9) lives in the day's lab, one directory per paper:

```
days/day-043-rope-and-alibi/
└── lab/
    └── papers/
        ├── roformer-rope/
        │   ├── demo.py          # runs on CPU, one command, prints a number
        │   └── README.md        # what it shows, what it does NOT show
        └── alibi/
            ├── demo.py
            └── README.md
```

The project is printed in full in the part, with its `Line by line` walkthrough, and typed by the
learner like every other line of code in this curriculum.

#### 25.10.2 What a paper part must contain

A paper part carries the **nine unconditional sections of §25.4**, plus `Shapes` and `Line by line`
under the same conditions, plus **three more that are unconditional for paper parts**. The order:

| # | Section | The rule, for a paper |
| --- | --- | --- |
| 1 | **frontmatter** | as §25.4, plus `kind: paper`, `paper_title`, `paper_arxiv` (or `paper_venue` where there is no arXiv id), `paper_year`. |
| 2 | **One-line answer** | What the paper *claimed*, in one sentence, in your own words. |
| 3 | **The story** | **The world before the paper.** What people were actually doing, what it cost them, and the specific frustration this paper was a response to. No jargon, and no hindsight — the story is told from inside the year it was written. |
| 4 | **The idea in plain language** | The paper's core idea with no math and no notation. If you cannot state it without an equation, you have not finished reading it. |
| 5 | **Why Akshara needs it** | The line of your own code that is this paper. *"`apply_rope()` in `akshara/model/position.py` is §3.4.2 of this paper"* is the shape. |
| 6 | **The mechanism** | The paper's actual contribution: the equation, the algorithm box, the architecture figure — **reproduced and then read symbol by symbol.** Every symbol in every equation is named, with its shape where it has one. This is `Line by line`, applied to mathematics: **an unexplained symbol is a bug in the doc.** |
| 7 | **Shapes** *(conditional)* | As §25.4. Papers use their own notation; the table maps the paper's symbols onto the curriculum's (`B`, `T`, `C`, `H`, `hs`, `V`) so the reader can move between the paper and their own code without re-deriving anything. |
| 8 | **Line by line** *(conditional)* | As §25.4, for any code block. |
| 9 | **The paper in one small project** ⟵ *paper-specific* | **The smallest end-to-end runnable project that implements the paper's contribution and nothing else.** Not a snippet — a project: it starts from nothing, runs with one command, and prints a result. And it is *only* the paper: no surrounding model, no other features, no scaffolding the paper did not introduce. **The isolation is the pedagogy** — being able to strip an idea down to the smallest thing that still demonstrates it is the proof you understood what the paper actually added, and it is the single hardest part of writing one of these. It must run at **T0** (laptop CPU, seconds to a couple of minutes) on synthetic or tiny data. It must include the **A/B**: the same project with the paper's idea switched off, because a demo that only shows *it runs* demonstrates nothing — **the ablation is the demo.** It ends by stating what it does **not** show: the claims that only appear at scale. |
| 10 | **What the paper showed** ⟵ *paper-specific* | The evidence, **cited to the table or section it came from** — "Table 3", "§5.2" — with the numbers **as reported** (Principle 8: these are cited, not measured, and the part says so). Then the honest part: **what the evidence does and does not support.** Ablations that were not run, baselines that were not tuned, the single seed, the benchmark that was already saturating. This section is where a reader learns to read a results table like a reviewer rather than like an audience. |
| 11 | **When it breaks** | As §25.4: where this idea fails in practice, with the real error or the real wrong output. |
| 12 | **What came after** ⟵ *paper-specific* | The paper's afterlife. What was corrected, superseded, or failed to reproduce; what the community quietly stopped doing; which follow-up paper is the one people actually implement now. **A paper taught as though it were the final word is taught wrong** — this section is why the reader will not be defending a 2017 default in 2027. |
| 13 | **In production** | What survived into real systems, what everybody changed, and the thing the paper recommends that nobody does. Plus the interview question — for papers, usually *"why is it √d_k and not d_k?"*-shaped: a question you can only answer if you read the argument rather than the abstract. |
| 14 | **Check yourself** | As §25.4 — one command that prints a number — **plus one instruction that sends the reader into the paper itself**: *"read §3.2.1 and say, out loud, what breaks if the scaling is removed."* The reader must open the PDF at least once per paper part. |

#### 25.10.3 The rules around paper parts

1. **One paper, one part.** Two papers in a day is two parts. If a part needs "and also, the ALiBi
   paper" it is two parts — the one-idea test (§25.4) applies unchanged.
2. **Resolve the identifier live, never from memory** (Principle 8). The arXiv id, the year, the
   exact title and the venue are looked up on the day the part is written, and the row lands in
   `docs/PAPERS.md` **before** the part is written. **§24.3 deliberately lists papers by title and
   year rather than by id**, precisely so that no id in this plan is a remembered one.
3. **Quote numbers as reported, and label them.** A number from a paper is a *citation*, not a
   measurement, and the part says which: `[reported: Table 3]` versus `[measured here: T4, seed
   1337, 2026-08-25]`. Mixing the two is how a curriculum starts lying to itself.
4. **Read the actual paper.** A paper part written from an abstract, a blog summary, or memory is
   worse than no paper part, because it launders unreliability through the appearance of a citation.
   The hub's §8 records the URL fetched and the date.
5. **Say what you skipped.** Papers have sections that do not matter for this curriculum. The part
   says so — *"§6 is a machine-translation evaluation you can skip"* — because a reader who thinks
   they must understand all nine pages will not open page one.
6. **A parked 🅿️ concept still gets its paper part** — *including its small project*. You are not
   building a Mamba, and you can still build a fifty-line selective scan on a toy sequence and watch
   it do the thing the paper claims. 🅿️ means "not built into Akshara", never "not built at all".
7. **The small project lives in the day's lab**, at `lab/papers/<paper-slug>/`, and is printed in
   full in the part with its `Line by line` walkthrough. The learner types it, like all other code.
8. **The small project must be honest about its scale.** It will not reproduce the paper — a 500-step
   run on synthetic data never does. It reproduces the *mechanism* and the *direction* of the
   paper's effect. The part says which, in words, and the `What the paper showed` section that
   follows is where your number and their number get compared out loud. **A demo presented as a
   reproduction is Silent Failure #4 wearing a lab coat.**
9. **If you cannot isolate it, you have not understood it.** A paper whose small project keeps
   dragging in the rest of the transformer is a signal to re-read, not a signal to write a bigger
   demo. The one genuine exception is a paper whose contribution *is* a system-level property
   (continuous batching, FSDP); there the project simulates the mechanism — a queue of fake
   requests, a fake device mesh — and says so.

#### 25.10.4 Why this is worth the length

Three reasons, and the third is the real one.

- **It is where the field's reasoning lives.** The plan teaches you *that* attention scales by √d_k.
  The paper part is where you learn *why the variance argument leads there*, which is what lets you
  reason about the next architecture rather than memorise this one.
- **It is a transferable skill.** After ninety paper parts, a reader can open an unfamiliar paper,
  find the contribution, find the evidence, and find what the evidence does not support. That skill
  outlives every specific result in this plan.
- **The small project is where "I read it" becomes "I can build it".** A paper you have re-implemented
  in fifty lines, with the ablation showing the effect appear and disappear, is a paper you can
  argue about. One you have only read is a paper you can quote. This is Principle 3 —
  build first, compare after — applied to the literature rather than to libraries.
- **It is the antidote to the field's actual failure mode.** Generative AI runs on half-remembered
  claims — "temperature 0.7 is best", "you need 20 tokens per parameter", "LoRA rank 16 is
  standard". Every one of those is a real result, from a real paper, under conditions nobody
  restates. **Principle 8 says never invent a number; §25.10 is how the curriculum earns the right
  to say that**, by teaching where numbers come from and what they were measured on.

---

## 26 · 🚦 Phase Gates & the Freshness Check

A phase is **green** only when:

1. Every day in the phase has its row in `docs/PROGRESS.md` with gates green.
2. `scripts/trace.py` shows **no open IDs** from this or any earlier phase.
3. `./m check` passes on the whole repo — lint, format, tests, **and the §25 depth contract for
   every written day**.
4. Every day in the phase has a `parts/` directory. A day with no `parts/` is not written (§25.2),
   so a phase containing one cannot be green.
5. Every training run performed in the phase has a row in `docs/RUNS.md` carrying a seed, a config
   hash and a hardware line (Principle 9). **A run without a row did not happen.**
6. Every model or dataset downloaded in the phase has a row in `docs/MODELS.md` / `docs/DATASETS.md`
   with a revision SHA and a licence, recorded **before** first use (Principle 13).
7. The **freshness check** passes:
   - Pinned libraries — has a breaking release landed? A changed default is a silent experiment
     change (§5.1). Breaking change → amend first.
   - Pinned model/dataset revisions still resolve, and their licences have not changed.
   - Free-compute terms re-checked: session limits, GPU availability, storage quotas.
   - Any paper the phase cites — is there a correction, a retraction, or a superseding result?
8. Any deviation is recorded: an ADR for structural changes, `docs/CHANGELOG_PLAN.md` for plan text.

**Never** skip a day, merge two days, or reorder days without an ADR.

> A gate is never passed because time ran out (Principle 17). `./m done N` is gated on a ticked
> `CHECKLIST.md` and green checks, and on nothing else.

---

## 27 · 📒 Ledgers & Traceability

All ledgers live in `docs/`.

| File | Nature | Rule |
| --- | --- | --- |
| `docs/PROGRESS.md` | Append-only | One row per completed day; **the last row is where we are.** |
| `docs/PACKAGES.md` | Append-only | Every install: package, version, date, day, why. No invented versions (Principle 6). |
| `docs/DATASETS.md` | Append-only | Every dataset **before** it is downloaded: name, source URL, revision SHA, licence, size, day, and whether it has been decontaminated against the eval sets. |
| `docs/MODELS.md` | Append-only | Every pretrained checkpoint **before** it is loaded: repo, revision SHA, licence, format (safetensors only — Principle 13), size, day, why. |
| `docs/RUNS.md` | Append-only | Every training run: run id, day, config path, config hash, seed, hardware, steps, tokens seen, final train/val loss, wall time, checkpoint location, outcome (**including "diverged"** — Principle 10). |
| `docs/PAPERS.md` | Append-only | Every paper taught: title, year, **identifier resolved live** (arXiv id or venue), the day and part that teaches it, the URL fetched and the date it was fetched. Written **before** the paper part is (Principle 8, §25.10.3). |
| `docs/CHANGELOG_PLAN.md` | Append-only | Every amendment to this plan (Principle 14). |
| `docs/TRACEABILITY.md` | Regenerated | `scripts/trace.py` scans every day hub against §24; an open ID in a completed phase is a bug. |
| `docs/TRACKER.md` | Regenerated | `scripts/tracker.py` reports what is written, **how many parts each day has**, and what is pending. A thin day is visible from this table alone. |
| `docs/CURRICULUM_INDEX.md` | Regenerated | The ID → day cross-table read out of §24. Answers *"where do I learn `ARCH-28`?"* |

**Three ledgers are regenerated and seven are written by hand — do not confuse them.**
`TRACEABILITY.md`, `TRACKER.md` and `CURRICULUM_INDEX.md` are outputs; editing them by hand only
means the next `./m check` silently overwrites you. `PROGRESS.md`, `PACKAGES.md`, `DATASETS.md`,
`MODELS.md`, `RUNS.md`, `PAPERS.md` and `CHANGELOG_PLAN.md` are append-only history, written by the
day you are finishing — every day document ends with the exact rows to paste (§25.5).

> **`RUNS.md` is the ledger this curriculum has that an ordinary project does not**, and it is the
> one that will save you. Six weeks after a training run, the only difference between a result and
> an anecdote is a row containing a seed, a config hash and a hardware line.

ADRs are `docs/adr/ADR-NNNN-*.md`.

---

## 28 · ✍️ The Style Guide

§25 says what a day must *contain*. This section says how it must *read*.

### 28.1 The register

1. **Storytelling is the default, not a flourish.** A scene before an abstraction, every time. The
   story section of a part carries **no jargon at all** — a person, a machine, an afternoon lost. A
   reader remembers the engineer whose model trained perfectly for six hours and produced pure
   `<pad>` long after they have forgotten the phrase "loss masking".
2. **Simple language first.** Plain words → concrete example → *only then* the terminology. If a
   twelve-year-old could not follow the first sentence, rewrite the first sentence. This is not
   dumbing down; it is putting the definition after the thing it defines.
3. **Define every term on first use — including your own terms from earlier days.** 162 days is long
   enough that Day 30 is genuinely forgotten by Day 121. Link the part that introduced it. "As we
   saw earlier" is not a link.
4. **Second person, present tense, active voice.** "You divide by √d_k, and the variance of the
   scores comes back to 1." Not "the scores are then scaled".
5. **No person names, no course or creator brand names.** This curriculum is self-contained and
   promotes nobody: never name an instructor, author, channel, academy, bootcamp or training
   company — in a lesson, a checklist, a docstring or a commit message. Naming the **tools and
   libraries** you actually use is required and unaffected (PyTorch, NumPy, `tokenizers`,
   `transformers`, llama.cpp…), as is **citing a paper by its arXiv id and title** — a citation is
   provenance (Principle 8), not a brand.

### 28.2 The scene format

For failures and motivations, use the four-beat scene:

> 🎬 **The scene:** what you are doing.
> 😬 **The naive fix:** what everyone tries.
> 💥 **Why it fails:** the mechanism — not the symptom.
> 💡 **The insight:** the principle that survives after the details are forgotten.

### 28.3 Code, shapes and commands

6. **Every command is given in full.** `mkdir -p`, `uv add pkg==1.2.3`, the run command, the check
   command. A reader should never have to infer "and now presumably I create a folder".
7. **Every code block is followed by `**Line by line:**`** — every non-obvious token, and *why it is
   that line and not another*. **An unexplained line is a bug in the doc.**
8. **Every tensor gets a shape.** In code, as a trailing comment: `x = tok_emb + pos_emb  # (B, T, C)`.
   In prose, as the `## Shapes` table (§25.4). Symbols are used consistently across the whole
   curriculum: `B` batch · `T` time/sequence · `C` channels/`d_model` · `H` heads · `hs` head size ·
   `V` vocabulary. Any part introducing a new symbol defines it.
9. **Every mechanism has a matching failure with the real error text**, reproduced verbatim.
   Paraphrasing a traceback is worse than omitting it — the reader searches for the string. For
   silent failures, show the *wrong output* verbatim instead.
10. **`TODO(me)` stays unsolved.** The doc teaches; it never does the reps.
11. **Mermaid whenever the concept is spatial, sequential, or a state machine.** Attention flow, the
    diffusion forward/reverse process, the RLHF pipeline, a request through a batching scheduler,
    the KV cache growing — all earn a diagram.

### 28.4 Facts

12. **No invented facts.** Versions, model revisions, dataset licences, API signatures, benchmark
    numbers, paper claims: looked up live and dated, or explicitly `TODO`'d **with the exact lookup
    command**. Principles 6, 7 and 8 wearing their writing hat.
13. **Cite papers by arXiv id.** *"the √d_k scaling argument (arXiv:1706.03762 §3.2.1)"*. A claim
    attributed to "the literature" is not a citation.
14. **Tables for enumerable facts, prose for reasoning.** Never a table of one row.
15. **Emoji section markers, consistent not decorative** — 🎬 🎯 📚 🛠️ 💥 🎤 ✅ 💡 🅿️ 🔍 📌 ⚠️ 📐.
16. **🅿️ = parked**: awareness-level, interview-ready, deliberately not built (§4, T2). A parked ID
    still gets a part with a story, a mechanism and a production section; what it does not get is a
    build step. **The arithmetic is still worked** — you must be able to size the thing you did not
    run.
17. **🔍 = compare**: a "build first, compare after" day (Principle 3). The hand-rolled version
    already exists; today you open the library and diff your understanding against theirs. A compare
    part must state at least one thing the library does that yours does not, and **why**.
18. **The interview paragraph is honest.** An answer you could actually defend, tied to what you
    built and to a number you measured. A war story with numbers beats an adjective.

### 28.5 The two things that are never written

19. **Never a clock.** Not "estimated hours", not "this takes an evening", not "quick", not "a short
    detour". `./m depth` fails the day on any of them (Principle 17).
20. **Never a trim.** If the day is getting long, it gets another part (§25.7). Cutting an
    explanation to fit is the one edit this format forbids outright.

### 28.6 The ritual

21. **Every day ends the same way** — the checklist, then the ledger rows, then the commit message
    `day NNN: <title> — closes <IDs>`. The sameness is the point: the repo is the memory, not the
    chat, and a stranger — or a different CLI agent six months from now — has to be able to pick up
    from the last row of `docs/PROGRESS.md` alone.

---

## 29 · 📝 Amendment record

| Version | Change |
| --- | --- |
| **v1.1.0** | **Papers become teaching, not citations.** Adds Principle 21, §24.3 (the paper roster — 130 papers across 88 days, listed by title and year so that no identifier in this plan is a remembered one), §25.10 (the paper-part contract: one part per paper, in the day's own paper section, carrying two extra unconditional sections — *What the paper showed* and *What came after*), the `papers:` hub frontmatter key, and the `docs/PAPERS.md` ledger. No curriculum ID, day boundary, phase, gate or compute policy changed. See ADR-0005. |
| **v1.0.0** | Initial plan. 17 curricula, 309 IDs, 162 days, 22 phases. Establishes the twenty principles (§2), the five silent failures (§6), the hub + `parts/` documentation architecture with the eleven-section part contract including the mandatory **Shapes** table (§25), the three-tier $0 compute policy (§4), and the six hand-written / three generated ledgers including `RUNS.md` (§27). |
