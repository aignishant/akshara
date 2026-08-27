# 📊 Tracker — Project Akshara

_Generated 2026-08-27 by `scripts/tracker.py`._ **Do not edit by hand.**

**0 / 162 days complete** · 14 written on disk · 166 part documents in total.

`complete` means a row in `docs/PROGRESS.md` (plan §27). `written` means the folder exists
with a `parts/` directory. A day with no `parts/` is not written, whatever the folder looks
like (plan §25.2).

**Read the parts column.** A day closing three IDs with two parts is thin, and thin is
visible from this table without opening the day.

## 🚧 Phase 0 — Foundry: the machine, the skeleton, the driver  (0/1 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| [0](../days/day-000-toolchain-skeleton-driver/LESSON.md) | Toolchain, skeleton and the `./m` driver — one owner for the environ… | 0 | 13 | 6 | 🚧 written |

## 🚧 Phase 1 — The ground: tensors, gradients, information  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| [1](../days/day-001-bootstrap-and-map/LESSON.md) | Bootstrap & the map — the repo as Akshara's memory, `.env` + the Hug… | 4 | 14 | 4 | 🚧 written |
| [2](../days/day-002-tensors-shape-stride/LESSON.md) | Tensors — shape, dtype, stride, device, broadcasting; the matmul tha… | 3 | 13 | 4 | 🚧 written |
| [3](../days/day-003-derivatives-and-autograd/LESSON.md) | Derivatives by hand — the chain rule as a graph, and a scalar autogr… | 2 | 12 | 3 | 🚧 written |
| [4](../days/day-004-backprop-and-gradcheck/LESSON.md) | Backprop through a layer — the transpose everyone gets wrong, proved… | 2 | 11 | 3 | 🚧 written |
| [5](../days/day-005-logits-softmax-sampling/LESSON.md) | Probability over a vocabulary — logits, softmax, and sampling from a… | 2 | 11 | 3 | 🚧 written |
| [6](../days/day-006-entropy-cross-entropy-perplexity/LESSON.md) | Information — entropy, cross-entropy, KL, perplexity; **why the loss… | 3 | 12 | 3 | 🚧 written |
| [7](../days/day-007-floating-point-and-logsumexp/LESSON.md) | 💥 Numerical reality — fp32/fp16/bf16, the softmax that returns NaN, … | 2 | 11 | 3 | 🚧 written |
| [8](../days/day-008-gradient-descent-and-adam/LESSON.md) | Optimization — gradient descent, momentum, Adam/AdamW, and the learn… | 2 | 12 | 3 | 🚧 written |

## 🚧 Phase 2 — Text becomes numbers  (0/9 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| [9](../days/day-009-the-vocabulary-problem/LESSON.md) | The vocabulary problem — why not words, why not letters, and what a … | 2 | 11 | 3 | 🚧 written |
| [10](../days/day-010-unicode-code-points-bytes/LESSON.md) | Unicode, code points and bytes — the layer under every tokenizer, an… | 2 | 11 | 3 | 🚧 written |
| [11](../days/day-011-character-and-word-tokenizers/LESSON.md) | Character-level and word-level tokenizers, built — and where each on… | 2 | 11 | 3 | 🚧 written |
| [12](../days/day-012-bpe-the-merge-loop/LESSON.md) | BPE from scratch I — the merge loop, run by hand on a toy corpus, th… | 2 | 11 | 3 | 🚧 written |
| [13](../days/day-013-bpe-encode-decode-bytes/LESSON.md) | BPE from scratch II — encode, decode, the regex pre-tokenizer, and b… | 3 | 13 | 4 | 🚧 written |
| 14 | 🔍 Now compare — `tiktoken` and the `tokenizers` pipeline; what a pro… | 2 | — | — | ⬜ pending |
| 15 | The other families — WordPiece, Unigram and SentencePiece; a *probab… | 2 | — | — | ⬜ pending |
| 16 | Special tokens & chat templates — BOS/EOS/PAD/UNK, resizing an embed… | 2 | — | — | ⬜ pending |
| 17 | 💥 The tokenizer failure lab — numbers, whitespace, code, multilingua… | 3 | — | — | ⬜ pending |

## ⬜ Phase 3 — Representation  (0/5 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 18 | From one-hot to a lookup table — what an embedding actually is, and … | 2 | — | — | ⬜ pending |
| 19 | Distributional semantics — word2vec and GloVe as history, and what t… | 2 | — | — | ⬜ pending |
| 20 | Static vs contextual — the same word, two vectors; the residual stre… | 2 | — | — | ⬜ pending |
| 21 | 💥 Measuring similarity — cosine, dot, Euclidean, and the anisotropy … | 2 | — | — | ⬜ pending |
| 22 | Weight tying and the unembedding head — where the parameters actuall… | 2 | — | — | ⬜ pending |

## ⬜ Phase 4 — Before attention: the sequence problem  (0/6 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 23 | Next-token prediction — the whole field in one sentence; teacher for… | 2 | — | — | ⬜ pending |
| 24 | The n-gram model, built — counting, smoothing, and the sparsity wall… | 1 | — | — | ⬜ pending |
| 25 | The bigram neural LM — your first trained model, and what "the loss … | 2 | — | — | ⬜ pending |
| 26 | The MLP language model — a fixed window, and the concatenation ceiling | 1 | — | — | ⬜ pending |
| 27 | RNNs and LSTMs, built — recurrence, BPTT, and how a gate keeps a gra… | 2 | — | — | ⬜ pending |
| 28 | 💥 Why recurrence lost — the sequential bottleneck, measured against … | 1 | — | — | ⬜ pending |

## ⬜ Phase 5 — Attention  (0/6 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 29 | Attention as a soft lookup — query, key, value, and the dictionary t… | 1 | — | — | ⬜ pending |
| 30 | Scaled dot-product attention, built — and why √d_k, derived then mea… | 2 | — | — | ⬜ pending |
| 31 | Causal masking — the triangle that prevents cheating, and the `-inf`… | 1 | — | — | ⬜ pending |
| 32 | Multi-head attention — the reshape that confuses everyone, drawn; an… | 2 | — | — | ⬜ pending |
| 33 | Self-attention vs cross-attention — the same mechanism, two wirings | 1 | — | — | ⬜ pending |
| 34 | 💥 The attention failure lab — the O(n²) wall, attention sinks, and t… | 1 | — | — | ⬜ pending |

## ⬜ Phase 6 — The block and the model  (0/6 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 35 | The feed-forward network — why 4× wide, and ReLU → GELU → SwiGLU | 2 | — | — | ⬜ pending |
| 36 | Residual connections — the highway that makes depth trainable, and t… | 1 | — | — | ⬜ pending |
| 37 | Normalization — LayerNorm vs RMSNorm, pre-norm vs post-norm, and the… | 2 | — | — | ⬜ pending |
| 38 | The transformer block assembled — one class, every piece accounted for | 1 | — | — | ⬜ pending |
| 39 | **Akshara v0** — a full decoder-only model that runs, with every par… | 2 | — | — | ⬜ pending |
| 40 | 🔍 Reading the original paper — the 2017 architecture vs what people … | 1 | — | — | ⬜ pending |

## ⬜ Phase 7 — Position  (0/4 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 41 | 💥 The model has no idea about order — permutation equivariance, prov… | 1 | — | — | ⬜ pending |
| 42 | Sinusoidal and learned positional embeddings | 1 | — | — | ⬜ pending |
| 43 | RoPE, built — rotation as relative position; and ALiBi's different bet | 2 | — | — | ⬜ pending |
| 44 | Long context — position interpolation, NTK/YaRN scaling, sliding-win… | 2 | — | — | ⬜ pending |

## ⬜ Phase 8 — The variant zoo  (0/6 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 45 | Encoder-only — bidirectional attention and masked language modelling… | 2 | — | — | ⬜ pending |
| 46 | Encoder–decoder — seq2seq and cross-attention in anger | 1 | — | — | ⬜ pending |
| 47 | Decoder-only, and the argument for why it won | 1 | — | — | ⬜ pending |
| 48 | MQA and GQA — an architecture decision made entirely by the KV cache | 1 | — | — | ⬜ pending |
| 49 | Mixture of Experts — the router, the sparse forward pass, load balan… | 2 | — | — | ⬜ pending |
| 50 | 🅿️ State-space models and hybrids — Mamba, selective scan, linear at… | 2 | — | — | ⬜ pending |

## ⬜ Phase 9 — Training mechanics  (0/10 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 51 | The training loop, written once and properly — and the train/val spl… | 2 | — | — | ⬜ pending |
| 52 | Datasets and dataloaders — streaming, workers, and a shuffle you can… | 1 | — | — | ⬜ pending |
| 53 | 💥 Batching text — padding, attention masks, sequence packing, and **… | 2 | — | — | ⬜ pending |
| 54 | Initialization — why scale matters, and the residual-scaled init | 1 | — | — | ⬜ pending |
| 55 | Learning-rate schedules — warmup, cosine decay, and the hyperparamet… | 3 | — | — | ⬜ pending |
| 56 | AdamW, decoupled weight decay and gradient clipping — and reading th… | 2 | — | — | ⬜ pending |
| 57 | The three levers of a small card — mixed precision, gradient accumul… | 3 | — | — | ⬜ pending |
| 58 | Checkpoint and resume — the run that survives a disconnected free no… | 2 | — | — | ⬜ pending |
| 59 | Determinism, seeds, and testing ML code — what a unit test for a lay… | 3 | — | — | ⬜ pending |
| 60 | 💥 The debug ritual — overfit one batch, read the loss curve, hunt th… | 3 | — | — | ⬜ pending |

## ⬜ Phase 10 — Data & the pretraining run  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 61 | Where pretraining data comes from — sources, quality filtering, and … | 2 | — | — | ⬜ pending |
| 62 | 💥 Deduplication and decontamination — the two steps everyone skips, … | 2 | — | — | ⬜ pending |
| 63 | Data mixtures and curriculum — the ratio that decides what your mode… | 1 | — | — | ⬜ pending |
| 64 | Tokenizing a corpus at scale — the memmap file; and what never enter… | 2 | — | — | ⬜ pending |
| 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per par… | 4 | — | — | ⬜ pending |
| 66 | Sizing Akshara — the parameter count derived from one free T4's VRAM… | 3 | — | — | ⬜ pending |
| 67 | **The pretraining run** — launch, watch, and know whether the GPU is… | 3 | — | — | ⬜ pending |
| 68 | Phase gate — reading your own run; emergence and its critics; when t… | 3 | — | — | ⬜ pending |

## ⬜ Phase 11 — Decoding & inference  (0/9 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 69 | The autoregressive loop, honestly — one token at a time, and why dec… | 2 | — | — | ⬜ pending |
| 70 | Greedy and beam search — and why beam is the wrong tool for open-end… | 2 | — | — | ⬜ pending |
| 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on yo… | 4 | — | — | ⬜ pending |
| 72 | Penalties and logit processors — repetition, frequency, presence, lo… | 2 | — | — | ⬜ pending |
| 73 | 💥 Stopping — EOS, stop strings, max tokens, and the truncated JSON a… | 1 | — | — | ⬜ pending |
| 74 | The KV cache, built — the single optimisation that makes chat afford… | 2 | — | — | ⬜ pending |
| 75 | Prefill vs decode — TTFT, TPOT, streaming, and the detokenization bo… | 3 | — | — | ⬜ pending |
| 76 | Constrained decoding — JSON schemas, grammars, and finite-state mask… | 2 | — | — | ⬜ pending |
| 77 | 🅿️ Speculative decoding and continuous batching — the two ideas that… | 2 | — | — | ⬜ pending |

## ⬜ Phase 12 — Efficiency  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 78 | The memory equation — parameters, gradients, optimizer states, activ… | 2 | — | — | ⬜ pending |
| 79 | Quantization I — scales and zero points; what int8 and int4 actually… | 2 | — | — | ⬜ pending |
| 80 | 💥 Quantization II — GPTQ, AWQ, GGUF; Akshara at 4 bits, with the dam… | 3 | — | — | ⬜ pending |
| 81 | LoRA from scratch — the low-rank update derived, built, and merged b… | 2 | — | — | ⬜ pending |
| 82 | 🔍 QLoRA and the PEFT family — NF4, double quantization, adapters, pr… | 2 | — | — | ⬜ pending |
| 83 | FlashAttention and PagedAttention — IO-awareness and virtual memory … | 2 | — | — | ⬜ pending |
| 84 | Distillation and pruning — smaller by teaching, smaller by cutting | 2 | — | — | ⬜ pending |
| 85 | The laptop that serves — CPU inference, ONNX, `torch.compile`, and o… | 3 | — | — | ⬜ pending |

## ⬜ Phase 13 — Post-training & alignment  (0/11 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 86 | 💥 A base model is not a chatbot — the completion/instruction gap, de… | 1 | — | — | ⬜ pending |
| 87 | SFT I — instruction datasets, synthesis, licences, and quality over … | 2 | — | — | ⬜ pending |
| 88 | 💥 SFT II — chat templates and loss masking; **the bug that trains on… | 2 | — | — | ⬜ pending |
| 89 | **The fine-tuning run** — Akshara learns to follow instructions, on … | 1 | — | — | ⬜ pending |
| 90 | 💥 Evaluating a fine-tune — did it learn the task, or the format? (**… | 1 | — | — | ⬜ pending |
| 91 | Preference data — pairwise comparison, annotation noise, and the agr… | 2 | — | — | ⬜ pending |
| 92 | 💥 Reward models — training one, then watching it get hacked | 2 | — | — | ⬜ pending |
| 93 | RLHF with PPO — the four-model pipeline, the KL leash, and an honest… | 2 | — | — | ⬜ pending |
| 94 | **DPO, built** — preference optimization without a reward model; ORP… | 3 | — | — | ⬜ pending |
| 95 | 🅿️ RLAIF, constitutional AI, rejection sampling, best-of-n, GRPO and… | 2 | — | — | ⬜ pending |
| 96 | 💥 The alignment failure lab — catastrophic forgetting, the alignment… | 2 | — | — | ⬜ pending |

## ⬜ Phase 14 — Reasoning & prompting  (0/7 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 97 | In-context learning — what actually happens when you give examples | 2 | — | — | ⬜ pending |
| 98 | Prompting as engineering — instruction, context, format, and what a … | 2 | — | — | ⬜ pending |
| 99 | 💥 Chain of thought — why it works, and when the stated reasoning is … | 2 | — | — | ⬜ pending |
| 100 | Self-consistency, decomposition and self-critique — and where self-c… | 2 | — | — | ⬜ pending |
| 101 | Reasoning models and thinking tokens — test-time compute as a scalin… | 2 | — | — | ⬜ pending |
| 102 | Verifiers, process rewards, and tools as the correctness escape hatch | 2 | — | — | ⬜ pending |
| 103 | 💥 The prompting failure lab — sensitivity, position bias, lost-in-th… | 2 | — | — | ⬜ pending |

## ⬜ Phase 15 — Knowledge & retrieval  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 104 | What a model knows — parametric knowledge, memorization vs generaliz… | 2 | — | — | ⬜ pending |
| 105 | Retrieval embeddings — contrastive training, hard negatives, bi-enco… | 2 | — | — | ⬜ pending |
| 106 | 💥 Chunking — the decision that silently sets your recall ceiling | 1 | — | — | ⬜ pending |
| 107 | Vector search — exact vs approximate, HNSW and IVF, and the recall/l… | 2 | — | — | ⬜ pending |
| 108 | Hybrid retrieval — BM25 fused with dense, and the reranker that earn… | 2 | — | — | ⬜ pending |
| 109 | **The RAG pipeline** — assembled end to end over Akshara | 1 | — | — | ⬜ pending |
| 110 | Evaluating RAG — retrieval metrics and answer metrics are not the sa… | 2 | — | — | ⬜ pending |
| 111 | 💥 When RAG is the wrong tool — long context, fine-tuning, or a datab… | 2 | — | — | ⬜ pending |

## ⬜ Phase 16 — Evaluation  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 112 | Why evaluation is the hardest problem — and why every shortcut has a… | 1 | — | — | ⬜ pending |
| 113 | Perplexity — computed on your own model, and everything it hides | 2 | — | — | ⬜ pending |
| 114 | 💥 Benchmarks and contamination — what MMLU measures, and finding lea… | 2 | — | — | ⬜ pending |
| 115 | Generation metrics — BLEU, ROUGE, BERTScore, and why they are weak | 2 | — | — | ⬜ pending |
| 116 | 💥 LLM-as-judge — building one, then characterising its position, ver… | 2 | — | — | ⬜ pending |
| 117 | Human evaluation — pairwise preference, Elo/Bradley-Terry, and rubri… | 3 | — | — | ⬜ pending |
| 118 | Evals are tests — the regression gate in CI | 2 | — | — | ⬜ pending |
| 119 | 💥 Calibration, abstention and significance — **Silent Failure #4**, … | 3 | — | — | ⬜ pending |

## ⬜ Phase 17 — Multimodal  (0/9 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 120 | The general recipe — any modality becomes a sequence of vectors | 1 | — | — | ⬜ pending |
| 121 | Images as patches — the Vision Transformer, built; 2D position and v… | 2 | — | — | ⬜ pending |
| 122 | Contrastive pretraining — CLIP, InfoNCE, the shared space, and the l… | 2 | — | — | ⬜ pending |
| 123 | **Vision–language models** — the projector that bridges into Akshara… | 2 | — | — | ⬜ pending |
| 124 | 💥 Audio understanding — spectrograms, Whisper's encoder–decoder, and… | 2 | — | — | ⬜ pending |
| 125 | Audio tokenization — neural codecs and discrete speech units | 1 | — | — | ⬜ pending |
| 126 | Video — frames, temporal modelling, frame sampling, and the token-pe… | 2 | — | — | ⬜ pending |
| 127 | 🅿️ Any-to-any and unified models; OCR, documents, and the "just read… | 2 | — | — | ⬜ pending |
| 128 | 💥 Multimodal hallucination and evaluation — grounding failures, and … | 2 | — | — | ⬜ pending |

## ⬜ Phase 18 — Other generative families  (0/12 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 129 | The family tree — autoregressive, VAE, GAN, flow, diffusion, and wha… | 1 | — | — | ⬜ pending |
| 130 | Autoencoders and VAEs — the latent space, the ELBO, and the reparame… | 2 | — | — | ⬜ pending |
| 131 | 🅿️ GANs — the adversarial game, mode collapse, and why they faded | 2 | — | — | ⬜ pending |
| 132 | Diffusion I — the forward noising process, and the closed form that … | 1 | — | — | ⬜ pending |
| 133 | Diffusion II — the reverse process, the denoiser, and the objective … | 2 | — | — | ⬜ pending |
| 134 | **Diffusion III** — a tiny diffusion model, trained on your own mach… | 1 | — | — | ⬜ pending |
| 135 | Samplers and schedules — DDIM, step count vs quality, and what the n… | 2 | — | — | ⬜ pending |
| 136 | Guidance — classifier guidance, classifier-free guidance, and the sc… | 2 | — | — | ⬜ pending |
| 137 | Latent diffusion — the VAE compressor that made it affordable, and t… | 2 | — | — | ⬜ pending |
| 138 | Control and personalization — ControlNet, LoRA for images, DreamBoot… | 2 | — | — | ⬜ pending |
| 139 | Flow matching and rectified flow — what replaced DDPM, and why it is… | 1 | — | — | ⬜ pending |
| 140 | 🅿️ Video and audio generation; and 💥 evaluating generative models — … | 3 | — | — | ⬜ pending |

## ⬜ Phase 19 — Safety, security & ethics  (0/9 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 141 | The threat model — who attacks a generative system, at which surface… | 1 | — | — | ⬜ pending |
| 142 | Hallucination — the mechanism, the measurement, and the mitigations … | 2 | — | — | ⬜ pending |
| 143 | 💥 Prompt injection and jailbreaks — direct, indirect, the lethal tri… | 3 | — | — | ⬜ pending |
| 144 | 💥 Memorization — training-data extraction, membership inference, and… | 2 | — | — | ⬜ pending |
| 145 | 💥 Poisoning and the supply chain — backdoors, pickle deserialization… | 2 | — | — | ⬜ pending |
| 146 | Bias and fairness — where it enters, and how to measure it rather th… | 2 | — | — | ⬜ pending |
| 147 | Copyright, licensing and consent — auditing what Akshara was actuall… | 1 | — | — | ⬜ pending |
| 148 | Watermarking, provenance and deepfakes — C2PA, and the honest limits… | 2 | — | — | ⬜ pending |
| 149 | Guardrails, the model card, the regulatory map 🅿️, and the release d… | 4 | — | — | ⬜ pending |

## ⬜ Phase 20 — Serving & operations  (0/8 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 150 | Model formats and loading — safetensors, GGUF, memory-mapped weights… | 2 | — | — | ⬜ pending |
| 151 | **An inference server from scratch** — the request lifecycle, stream… | 2 | — | — | ⬜ pending |
| 152 | 🔍 Now compare — vLLM, TGI, llama.cpp, Ollama; what they do that your… | 2 | — | — | ⬜ pending |
| 153 | Batching and scheduling in production — continuous batching, admissi… | 2 | — | — | ⬜ pending |
| 154 | 💥 Caching — prefix caching, semantic caching, and the day it returns… | 2 | — | — | ⬜ pending |
| 155 | Observability — latency percentiles, tokens/s, cost per request, and… | 3 | — | — | ⬜ pending |
| 156 | Registry, versioning and the container — which weights answered that… | 2 | — | — | ⬜ pending |
| 157 | Capacity planning and build-vs-buy — sizing a deployment from a late… | 2 | — | — | ⬜ pending |

## ⬜ Phase 21 — Capstone  (0/4 complete)

| Day | Title | IDs | Parts | Sections | Status |
| --- | --- | --- | --- | --- | --- |
| 158 | Capstone I — Akshara end to end, cold: corpus → tokenizer → pretrain… | 0 | — | — | ⬜ pending |
| 159 | Capstone II — the eval suite run in full, the model card written, th… | 0 | — | — | ⬜ pending |
| 160 | Capstone III — the interview drill: every ADR, every number, every t… | 0 | — | — | ⬜ pending |
| 161 | Final gate — whole-system audit, the retrospective, and what you wou… | 0 | — | — | ⬜ pending |
