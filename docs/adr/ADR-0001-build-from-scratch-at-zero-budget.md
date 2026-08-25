# ADR-0001 — Build from scratch, at zero budget, around one carried-forward model

- **Date:** 2026-08-25
- **Day:** 0 (pre-curriculum)
- **Phase:** 0
- **Status:** accepted
- **Establishes:** master plan v1.0.0

## Context

A generative-AI curriculum has to answer three questions before it can write a single day, and the
answers are not independent.

1. **How does the learner meet an idea?** Through an API, or through an implementation?
2. **What hardware is assumed?**
3. **What holds the 309 concepts together?**

The default answer to all three — use the APIs, assume a GPU, teach topic by topic — produces
somebody who can call a library and cannot debug it. That is the outcome this plan exists to avoid.

## Decision

**1. Build first, compare after** (Principle 3). Every mechanism the curriculum teaches is
hand-rolled before the library that implements it is opened: BPE before `tokenizers`, attention
before `transformers`, the KV cache before `vLLM`, LoRA before `peft`, the denoiser before
`diffusers`. The comparison day (🔍) is a first-class day kind, and must name at least one thing the
library does that the hand-rolled version does not, and why.

**2. Zero budget, three tiers** (§4). T0 is a laptop CPU and carries the overwhelming majority of
days. T1 is one free pre-emptible notebook GPU and carries the handful of real training runs. T2 is
parked 🅿️ — taught as reading **with the arithmetic worked**, so a run you cannot afford is still a
run you can size. No day may require a payment.

**3. One artifact, carried forward** (§3). Akshara — a small decoder-only language model — is grown
day by day: its tokenizer trains it, its chat template breaks the fine-tune, its checkpoint gets
quantized and served. Concepts that genuinely do not fit the spine (diffusion, ASR, ViT) are built
as their own artifacts in the same repo rather than being dropped.

## Consequences

**Good.**

- The learner can debug what they built. This is the entire justification for the extra length.
- The $0 constraint is pedagogically load-bearing, not a limitation: the memory equation,
  quantization, LoRA, gradient checkpointing and sequence packing are *forced* by a 16GB
  pre-emptible card. A learner with eight GPUs never has to learn them.
- Checkpoint-and-resume is taught before the first real run, because pre-emption is normal.

**Costly, accepted.**

- It is long. 162 days is the price of implementing rather than importing, and Principle 19 says the
  count is an output rather than a target.
- Akshara will be a *small* model. It will not be good. The plan says so out loud and teaches the
  scaling laws (§13) that let the learner reason about the runs they cannot perform.
- Some days are noticeably harder to design at T0 than they would be with a GPU. That work is done
  in the day, not passed to the learner.

**Rejected alternatives.**

| Alternative | Why not |
| --- | --- |
| API-first, mechanism by diagram | Produces exactly the "nice API over a mystery" outcome the plan exists to avoid. |
| Assume a local CUDA GPU | Makes the curriculum unrunnable for the person most likely to need it, and removes the constraint that teaches efficiency. |
| Topic-by-topic lab notebook, no spine | Nothing breaks on Day 88 because of Day 16, so nothing is load-bearing, so nothing is remembered. |
| A round day count (100, 150) | Forces compression, and compression always lands on the explanation. See Principle 19. |
