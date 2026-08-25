# 📇 Curriculum index — Project Akshara

_Generated 2026-08-25 by `scripts/trace.py` from the master plan's §24._
**Do not edit by hand.**

§24 answers *what does day 88 teach?* This file answers the reverse — *where do I learn
`ARCH-28`?* — which is the question you have when a later day cites an ID you no longer
remember. Every ID appears exactly once; a duplicate or a missing ID is a plan bug.

## `MATH` — Foundations (16 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `MATH-01` | 2 | Tensors — shape, dtype, stride, device, broadcasting; the matmul that is 90% of everythi… |
| `MATH-02` | 2 | Tensors — shape, dtype, stride, device, broadcasting; the matmul that is 90% of everythi… |
| `MATH-03` | 2 | Tensors — shape, dtype, stride, device, broadcasting; the matmul that is 90% of everythi… |
| `MATH-04` | 3 | Derivatives by hand — the chain rule as a graph, and a scalar autograd engine you write |
| `MATH-05` | 3 | Derivatives by hand — the chain rule as a graph, and a scalar autograd engine you write |
| `MATH-06` | 4 | Backprop through a layer — the transpose everyone gets wrong, proved by finite differences |
| `MATH-07` | 4 | Backprop through a layer — the transpose everyone gets wrong, proved by finite differences |
| `MATH-08` | 5 | Probability over a vocabulary — logits, softmax, and sampling from a categorical |
| `MATH-09` | 5 | Probability over a vocabulary — logits, softmax, and sampling from a categorical |
| `MATH-10` | 6 | Information — entropy, cross-entropy, KL, perplexity; **why the loss is the loss** |
| `MATH-11` | 6 | Information — entropy, cross-entropy, KL, perplexity; **why the loss is the loss** |
| `MATH-12` | 6 | Information — entropy, cross-entropy, KL, perplexity; **why the loss is the loss** |
| `MATH-13` | 7 | 💥 Numerical reality — fp32/fp16/bf16, the softmax that returns NaN, and log-sum-exp |
| `MATH-14` | 7 | 💥 Numerical reality — fp32/fp16/bf16, the softmax that returns NaN, and log-sum-exp |
| `MATH-15` | 8 | Optimization — gradient descent, momentum, Adam/AdamW, and the learning rate |
| `MATH-16` | 8 | Optimization — gradient descent, momentum, Adam/AdamW, and the learning rate |

## `TOK` — Tokenization (20 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `TOK-01` | 9 | The vocabulary problem — why not words, why not letters, and what a tokenizer is for |
| `TOK-02` | 9 | The vocabulary problem — why not words, why not letters, and what a tokenizer is for |
| `TOK-03` | 10 | Unicode, code points and bytes — the layer under every tokenizer, and the emoji that is … |
| `TOK-04` | 10 | Unicode, code points and bytes — the layer under every tokenizer, and the emoji that is … |
| `TOK-05` | 11 | Character-level and word-level tokenizers, built — and where each one dies |
| `TOK-06` | 11 | Character-level and word-level tokenizers, built — and where each one dies |
| `TOK-07` | 12 | BPE from scratch I — the merge loop, run by hand on a toy corpus, then trained |
| `TOK-08` | 12 | BPE from scratch I — the merge loop, run by hand on a toy corpus, then trained |
| `TOK-09` | 13 | BPE from scratch II — encode, decode, the regex pre-tokenizer, and byte-level BPE |
| `TOK-10` | 13 | BPE from scratch II — encode, decode, the regex pre-tokenizer, and byte-level BPE |
| `TOK-11` | 13 | BPE from scratch II — encode, decode, the regex pre-tokenizer, and byte-level BPE |
| `TOK-12` | 14 | 🔍 Now compare — `tiktoken` and the `tokenizers` pipeline; what a production tokenizer do… |
| `TOK-13` | 14 | 🔍 Now compare — `tiktoken` and the `tokenizers` pipeline; what a production tokenizer do… |
| `TOK-14` | 15 | The other families — WordPiece, Unigram and SentencePiece; a *probabilistic* vocabulary |
| `TOK-15` | 15 | The other families — WordPiece, Unigram and SentencePiece; a *probabilistic* vocabulary |
| `TOK-16` | 16 | Special tokens & chat templates — BOS/EOS/PAD/UNK, resizing an embedding, and **Silent F… |
| `TOK-17` | 16 | Special tokens & chat templates — BOS/EOS/PAD/UNK, resizing an embedding, and **Silent F… |
| `TOK-18` | 17 | 💥 The tokenizer failure lab — numbers, whitespace, code, multilingual inflation, token h… |
| `TOK-19` | 17 | 💥 The tokenizer failure lab — numbers, whitespace, code, multilingual inflation, token h… |
| `TOK-20` | 17 | 💥 The tokenizer failure lab — numbers, whitespace, code, multilingual inflation, token h… |

## `EMB` — Representation (10 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `EMB-01` | 18 | From one-hot to a lookup table — what an embedding actually is, and which gradient reach… |
| `EMB-02` | 18 | From one-hot to a lookup table — what an embedding actually is, and which gradient reach… |
| `EMB-03` | 19 | Distributional semantics — word2vec and GloVe as history, and what they got right |
| `EMB-04` | 19 | Distributional semantics — word2vec and GloVe as history, and what they got right |
| `EMB-05` | 20 | Static vs contextual — the same word, two vectors; the residual stream as a running repr… |
| `EMB-06` | 20 | Static vs contextual — the same word, two vectors; the residual stream as a running repr… |
| `EMB-07` | 21 | 💥 Measuring similarity — cosine, dot, Euclidean, and the anisotropy that makes raw LM st… |
| `EMB-08` | 21 | 💥 Measuring similarity — cosine, dot, Euclidean, and the anisotropy that makes raw LM st… |
| `EMB-09` | 22 | Weight tying and the unembedding head — where the parameters actually are |
| `EMB-10` | 22 | Weight tying and the unembedding head — where the parameters actually are |

## `ARCH` — Architecture (40 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `ARCH-01` | 23 | Next-token prediction — the whole field in one sentence; teacher forcing and exposure bias |
| `ARCH-02` | 23 | Next-token prediction — the whole field in one sentence; teacher forcing and exposure bias |
| `ARCH-03` | 24 | The n-gram model, built — counting, smoothing, and the sparsity wall you hit immediately |
| `ARCH-04` | 25 | The bigram neural LM — your first trained model, and what "the loss went down" means |
| `ARCH-05` | 26 | The MLP language model — a fixed window, and the concatenation ceiling |
| `ARCH-06` | 27 | RNNs and LSTMs, built — recurrence, BPTT, and how a gate keeps a gradient alive |
| `ARCH-07` | 27 | RNNs and LSTMs, built — recurrence, BPTT, and how a gate keeps a gradient alive |
| `ARCH-08` | 28 | 💥 Why recurrence lost — the sequential bottleneck, measured against what a GPU wants |
| `ARCH-09` | 29 | Attention as a soft lookup — query, key, value, and the dictionary that returns a blend |
| `ARCH-10` | 30 | Scaled dot-product attention, built — and why √d_k, derived then measured |
| `ARCH-11` | 30 | Scaled dot-product attention, built — and why √d_k, derived then measured |
| `ARCH-12` | 31 | Causal masking — the triangle that prevents cheating, and the `-inf` before the softmax |
| `ARCH-13` | 32 | Multi-head attention — the reshape that confuses everyone, drawn; and what heads special… |
| `ARCH-14` | 32 | Multi-head attention — the reshape that confuses everyone, drawn; and what heads special… |
| `ARCH-15` | 33 | Self-attention vs cross-attention — the same mechanism, two wirings |
| `ARCH-16` | 34 | 💥 The attention failure lab — the O(n²) wall, attention sinks, and the mask that was off… |
| `ARCH-17` | 35 | The feed-forward network — why 4× wide, and ReLU → GELU → SwiGLU |
| `ARCH-18` | 35 | The feed-forward network — why 4× wide, and ReLU → GELU → SwiGLU |
| `ARCH-19` | 36 | Residual connections — the highway that makes depth trainable, and the stream as a share… |
| `ARCH-20` | 37 | Normalization — LayerNorm vs RMSNorm, pre-norm vs post-norm, and the argument that moved… |
| `ARCH-21` | 37 | Normalization — LayerNorm vs RMSNorm, pre-norm vs post-norm, and the argument that moved… |
| `ARCH-22` | 38 | The transformer block assembled — one class, every piece accounted for |
| `ARCH-23` | 39 | **Akshara v0** — a full decoder-only model that runs, with every parameter counted by hand |
| `ARCH-24` | 39 | **Akshara v0** — a full decoder-only model that runs, with every parameter counted by hand |
| `ARCH-25` | 40 | 🔍 Reading the original paper — the 2017 architecture vs what people actually build now, … |
| `ARCH-26` | 41 | 💥 The model has no idea about order — permutation equivariance, proved by shuffling your… |
| `ARCH-27` | 42 | Sinusoidal and learned positional embeddings |
| `ARCH-28` | 43 | RoPE, built — rotation as relative position; and ALiBi's different bet |
| `ARCH-29` | 43 | RoPE, built — rotation as relative position; and ALiBi's different bet |
| `ARCH-30` | 44 | Long context — position interpolation, NTK/YaRN scaling, sliding-window and sparse atten… |
| `ARCH-31` | 44 | Long context — position interpolation, NTK/YaRN scaling, sliding-window and sparse atten… |
| `ARCH-32` | 45 | Encoder-only — bidirectional attention and masked language modelling; what BERT-shaped m… |
| `ARCH-33` | 45 | Encoder-only — bidirectional attention and masked language modelling; what BERT-shaped m… |
| `ARCH-34` | 46 | Encoder–decoder — seq2seq and cross-attention in anger |
| `ARCH-35` | 47 | Decoder-only, and the argument for why it won |
| `ARCH-36` | 48 | MQA and GQA — an architecture decision made entirely by the KV cache |
| `ARCH-37` | 49 | Mixture of Experts — the router, the sparse forward pass, load balancing, and the dead e… |
| `ARCH-38` | 49 | Mixture of Experts — the router, the sparse forward pass, load balancing, and the dead e… |
| `ARCH-39` | 50 | 🅿️ State-space models and hybrids — Mamba, selective scan, linear attention: what is gen… |
| `ARCH-40` | 50 | 🅿️ State-space models and hybrids — Mamba, selective scan, linear attention: what is gen… |

## `TRAIN` — Training (28 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `TRAIN-01` | 25 | The bigram neural LM — your first trained model, and what "the loss went down" means |
| `TRAIN-02` | 51 | The training loop, written once and properly — and the train/val split you will need on … |
| `TRAIN-03` | 51 | The training loop, written once and properly — and the train/val split you will need on … |
| `TRAIN-04` | 52 | Datasets and dataloaders — streaming, workers, and a shuffle you can reproduce |
| `TRAIN-05` | 53 | 💥 Batching text — padding, attention masks, sequence packing, and **the loss that counte… |
| `TRAIN-06` | 53 | 💥 Batching text — padding, attention masks, sequence packing, and **the loss that counte… |
| `TRAIN-07` | 54 | Initialization — why scale matters, and the residual-scaled init |
| `TRAIN-08` | 55 | Learning-rate schedules — warmup, cosine decay, and the hyperparameter budget of someone… |
| `TRAIN-09` | 55 | Learning-rate schedules — warmup, cosine decay, and the hyperparameter budget of someone… |
| `TRAIN-10` | 56 | AdamW, decoupled weight decay and gradient clipping — and reading the clip rate as a sig… |
| `TRAIN-11` | 56 | AdamW, decoupled weight decay and gradient clipping — and reading the clip rate as a sig… |
| `TRAIN-12` | 57 | The three levers of a small card — mixed precision, gradient accumulation, activation ch… |
| `TRAIN-13` | 57 | The three levers of a small card — mixed precision, gradient accumulation, activation ch… |
| `TRAIN-14` | 57 | The three levers of a small card — mixed precision, gradient accumulation, activation ch… |
| `TRAIN-15` | 58 | Checkpoint and resume — the run that survives a disconnected free notebook |
| `TRAIN-16` | 58 | Checkpoint and resume — the run that survives a disconnected free notebook |
| `TRAIN-17` | 59 | Determinism, seeds, and testing ML code — what a unit test for a layer looks like; the `… |
| `TRAIN-18` | 60 | 💥 The debug ritual — overfit one batch, read the loss curve, hunt the NaN, and find the … |
| `TRAIN-19` | 60 | 💥 The debug ritual — overfit one batch, read the loss curve, hunt the NaN, and find the … |
| `TRAIN-20` | 60 | 💥 The debug ritual — overfit one batch, read the loss curve, hunt the NaN, and find the … |
| `TRAIN-21` | 61 | Where pretraining data comes from — sources, quality filtering, and consent at collectio… |
| `TRAIN-22` | 62 | 💥 Deduplication and decontamination — the two steps everyone skips, and **Silent Failure… |
| `TRAIN-23` | 62 | 💥 Deduplication and decontamination — the two steps everyone skips, and **Silent Failure… |
| `TRAIN-24` | 63 | Data mixtures and curriculum — the ratio that decides what your model is good at |
| `TRAIN-25` | 64 | Tokenizing a corpus at scale — the memmap file; and what never enters git |
| `TRAIN-26` | 67 | **The pretraining run** — launch, watch, and know whether the GPU is actually working; t… |
| `TRAIN-27` | 66 | Sizing Akshara — the parameter count derived from one free T4's VRAM; 🅿️ what you would … |
| `TRAIN-28` | 55 | Learning-rate schedules — warmup, cosine decay, and the hyperparameter budget of someone… |

## `SCALE` — Scaling (10 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `SCALE-01` | 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per parameter |
| `SCALE-02` | 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per parameter |
| `SCALE-03` | 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per parameter |
| `SCALE-04` | 65 | Scaling laws — the power law, Kaplan, Chinchilla, and tokens per parameter |
| `SCALE-05` | 66 | Sizing Akshara — the parameter count derived from one free T4's VRAM; 🅿️ what you would … |
| `SCALE-06` | 66 | Sizing Akshara — the parameter count derived from one free T4's VRAM; 🅿️ what you would … |
| `SCALE-07` | 67 | **The pretraining run** — launch, watch, and know whether the GPU is actually working; t… |
| `SCALE-08` | 68 | Phase gate — reading your own run; emergence and its critics; when to stop |
| `SCALE-09` | 68 | Phase gate — reading your own run; emergence and its critics; when to stop |
| `SCALE-10` | 68 | Phase gate — reading your own run; emergence and its critics; when to stop |

## `INFER` — Inference (20 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `INFER-01` | 69 | The autoregressive loop, honestly — one token at a time, and why decoding is memory-bound |
| `INFER-02` | 69 | The autoregressive loop, honestly — one token at a time, and why decoding is memory-bound |
| `INFER-03` | 70 | Greedy and beam search — and why beam is the wrong tool for open-ended text |
| `INFER-04` | 70 | Greedy and beam search — and why beam is the wrong tool for open-ended text |
| `INFER-05` | 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on your own model; and wh… |
| `INFER-06` | 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on your own model; and wh… |
| `INFER-07` | 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on your own model; and wh… |
| `INFER-08` | 72 | Penalties and logit processors — repetition, frequency, presence, logit bias, banned tok… |
| `INFER-09` | 72 | Penalties and logit processors — repetition, frequency, presence, logit bias, banned tok… |
| `INFER-10` | 73 | 💥 Stopping — EOS, stop strings, max tokens, and the truncated JSON at 3am |
| `INFER-11` | 74 | The KV cache, built — the single optimisation that makes chat affordable, and what it co… |
| `INFER-12` | 74 | The KV cache, built — the single optimisation that makes chat affordable, and what it co… |
| `INFER-13` | 75 | Prefill vs decode — TTFT, TPOT, streaming, and the detokenization boundary bug |
| `INFER-14` | 75 | Prefill vs decode — TTFT, TPOT, streaming, and the detokenization boundary bug |
| `INFER-15` | 76 | Constrained decoding — JSON schemas, grammars, and finite-state masking of logits |
| `INFER-16` | 76 | Constrained decoding — JSON schemas, grammars, and finite-state masking of logits |
| `INFER-17` | 77 | 🅿️ Speculative decoding and continuous batching — the two ideas that made serving cheap |
| `INFER-18` | 77 | 🅿️ Speculative decoding and continuous batching — the two ideas that made serving cheap |
| `INFER-19` | 75 | Prefill vs decode — TTFT, TPOT, streaming, and the detokenization boundary bug |
| `INFER-20` | 71 | 💥 The sampler zoo — temperature, top-k, top-p, min-p, compared on your own model; and wh… |

## `EFF` — Efficiency (18 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `EFF-01` | 78 | The memory equation — parameters, gradients, optimizer states, activations, and the KV-c… |
| `EFF-02` | 78 | The memory equation — parameters, gradients, optimizer states, activations, and the KV-c… |
| `EFF-03` | 79 | Quantization I — scales and zero points; what int8 and int4 actually do; PTQ vs QAT |
| `EFF-04` | 79 | Quantization I — scales and zero points; what int8 and int4 actually do; PTQ vs QAT |
| `EFF-05` | 80 | 💥 Quantization II — GPTQ, AWQ, GGUF; Akshara at 4 bits, with the damage **measured** |
| `EFF-06` | 80 | 💥 Quantization II — GPTQ, AWQ, GGUF; Akshara at 4 bits, with the damage **measured** |
| `EFF-07` | 80 | 💥 Quantization II — GPTQ, AWQ, GGUF; Akshara at 4 bits, with the damage **measured** |
| `EFF-08` | 81 | LoRA from scratch — the low-rank update derived, built, and merged back |
| `EFF-09` | 81 | LoRA from scratch — the low-rank update derived, built, and merged back |
| `EFF-10` | 82 | 🔍 QLoRA and the PEFT family — NF4, double quantization, adapters, prefix and prompt tuning |
| `EFF-11` | 82 | 🔍 QLoRA and the PEFT family — NF4, double quantization, adapters, prefix and prompt tuning |
| `EFF-12` | 83 | FlashAttention and PagedAttention — IO-awareness and virtual memory for the KV cache |
| `EFF-13` | 83 | FlashAttention and PagedAttention — IO-awareness and virtual memory for the KV cache |
| `EFF-14` | 84 | Distillation and pruning — smaller by teaching, smaller by cutting |
| `EFF-15` | 84 | Distillation and pruning — smaller by teaching, smaller by cutting |
| `EFF-16` | 85 | The laptop that serves — CPU inference, ONNX, `torch.compile`, and offloading a model bi… |
| `EFF-17` | 85 | The laptop that serves — CPU inference, ONNX, `torch.compile`, and offloading a model bi… |
| `EFF-18` | 85 | The laptop that serves — CPU inference, ONNX, `torch.compile`, and offloading a model bi… |

## `POST` — Post-training (20 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `POST-01` | 86 | 💥 A base model is not a chatbot — the completion/instruction gap, demonstrated on your o… |
| `POST-02` | 87 | SFT I — instruction datasets, synthesis, licences, and quality over quantity |
| `POST-03` | 87 | SFT I — instruction datasets, synthesis, licences, and quality over quantity |
| `POST-04` | 88 | 💥 SFT II — chat templates and loss masking; **the bug that trains on the prompt** |
| `POST-05` | 88 | 💥 SFT II — chat templates and loss masking; **the bug that trains on the prompt** |
| `POST-06` | 89 | **The fine-tuning run** — Akshara learns to follow instructions, on free compute |
| `POST-07` | 90 | 💥 Evaluating a fine-tune — did it learn the task, or the format? (**Silent Failure #5**) |
| `POST-08` | 91 | Preference data — pairwise comparison, annotation noise, and the agreement ceiling |
| `POST-09` | 91 | Preference data — pairwise comparison, annotation noise, and the agreement ceiling |
| `POST-10` | 92 | 💥 Reward models — training one, then watching it get hacked |
| `POST-11` | 92 | 💥 Reward models — training one, then watching it get hacked |
| `POST-12` | 93 | RLHF with PPO — the four-model pipeline, the KL leash, and an honest account of why it i… |
| `POST-13` | 93 | RLHF with PPO — the four-model pipeline, the KL leash, and an honest account of why it i… |
| `POST-14` | 94 | **DPO, built** — preference optimization without a reward model; ORPO/KTO/SimPO; online … |
| `POST-15` | 94 | **DPO, built** — preference optimization without a reward model; ORPO/KTO/SimPO; online … |
| `POST-16` | 94 | **DPO, built** — preference optimization without a reward model; ORPO/KTO/SimPO; online … |
| `POST-17` | 95 | 🅿️ RLAIF, constitutional AI, rejection sampling, best-of-n, GRPO and verifiable rewards |
| `POST-18` | 95 | 🅿️ RLAIF, constitutional AI, rejection sampling, best-of-n, GRPO and verifiable rewards |
| `POST-19` | 96 | 💥 The alignment failure lab — catastrophic forgetting, the alignment tax, over-refusal, … |
| `POST-20` | 96 | 💥 The alignment failure lab — catastrophic forgetting, the alignment tax, over-refusal, … |

## `REASON` — Reasoning (14 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `REASON-01` | 97 | In-context learning — what actually happens when you give examples |
| `REASON-02` | 97 | In-context learning — what actually happens when you give examples |
| `REASON-03` | 98 | Prompting as engineering — instruction, context, format, and what a system prompt really… |
| `REASON-04` | 98 | Prompting as engineering — instruction, context, format, and what a system prompt really… |
| `REASON-05` | 99 | 💥 Chain of thought — why it works, and when the stated reasoning is a story told afterwa… |
| `REASON-06` | 99 | 💥 Chain of thought — why it works, and when the stated reasoning is a story told afterwa… |
| `REASON-07` | 100 | Self-consistency, decomposition and self-critique — and where self-critique reliably fails |
| `REASON-08` | 100 | Self-consistency, decomposition and self-critique — and where self-critique reliably fails |
| `REASON-09` | 101 | Reasoning models and thinking tokens — test-time compute as a scaling axis you pay for |
| `REASON-10` | 101 | Reasoning models and thinking tokens — test-time compute as a scaling axis you pay for |
| `REASON-11` | 102 | Verifiers, process rewards, and tools as the correctness escape hatch |
| `REASON-12` | 102 | Verifiers, process rewards, and tools as the correctness escape hatch |
| `REASON-13` | 103 | 💥 The prompting failure lab — sensitivity, position bias, lost-in-the-middle, and a firs… |
| `REASON-14` | 103 | 💥 The prompting failure lab — sensitivity, position bias, lost-in-the-middle, and a firs… |

## `RAG` — Retrieval (14 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `RAG-01` | 104 | What a model knows — parametric knowledge, memorization vs generalization, and the hallu… |
| `RAG-02` | 104 | What a model knows — parametric knowledge, memorization vs generalization, and the hallu… |
| `RAG-03` | 105 | Retrieval embeddings — contrastive training, hard negatives, bi-encoder vs cross-encoder |
| `RAG-04` | 105 | Retrieval embeddings — contrastive training, hard negatives, bi-encoder vs cross-encoder |
| `RAG-05` | 106 | 💥 Chunking — the decision that silently sets your recall ceiling |
| `RAG-06` | 107 | Vector search — exact vs approximate, HNSW and IVF, and the recall/latency/memory triangle |
| `RAG-07` | 107 | Vector search — exact vs approximate, HNSW and IVF, and the recall/latency/memory triangle |
| `RAG-08` | 108 | Hybrid retrieval — BM25 fused with dense, and the reranker that earns its latency |
| `RAG-09` | 108 | Hybrid retrieval — BM25 fused with dense, and the reranker that earns its latency |
| `RAG-10` | 109 | **The RAG pipeline** — assembled end to end over Akshara |
| `RAG-11` | 110 | Evaluating RAG — retrieval metrics and answer metrics are not the same measurement |
| `RAG-12` | 110 | Evaluating RAG — retrieval metrics and answer metrics are not the same measurement |
| `RAG-13` | 111 | 💥 When RAG is the wrong tool — long context, fine-tuning, or a database query all along |
| `RAG-14` | 111 | 💥 When RAG is the wrong tool — long context, fine-tuning, or a database query all along |

## `EVAL` — Evaluation (16 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `EVAL-01` | 112 | Why evaluation is the hardest problem — and why every shortcut has already been tried |
| `EVAL-02` | 113 | Perplexity — computed on your own model, and everything it hides |
| `EVAL-03` | 113 | Perplexity — computed on your own model, and everything it hides |
| `EVAL-04` | 114 | 💥 Benchmarks and contamination — what MMLU measures, and finding leakage in your own cor… |
| `EVAL-05` | 114 | 💥 Benchmarks and contamination — what MMLU measures, and finding leakage in your own cor… |
| `EVAL-06` | 115 | Generation metrics — BLEU, ROUGE, BERTScore, and why they are weak |
| `EVAL-07` | 115 | Generation metrics — BLEU, ROUGE, BERTScore, and why they are weak |
| `EVAL-08` | 116 | 💥 LLM-as-judge — building one, then characterising its position, verbosity and self-pref… |
| `EVAL-09` | 116 | 💥 LLM-as-judge — building one, then characterising its position, verbosity and self-pref… |
| `EVAL-10` | 117 | Human evaluation — pairwise preference, Elo/Bradley-Terry, and rubrics that survive cont… |
| `EVAL-11` | 117 | Human evaluation — pairwise preference, Elo/Bradley-Terry, and rubrics that survive cont… |
| `EVAL-12` | 117 | Human evaluation — pairwise preference, Elo/Bradley-Terry, and rubrics that survive cont… |
| `EVAL-13` | 118 | Evals are tests — the regression gate in CI |
| `EVAL-14` | 119 | 💥 Calibration, abstention and significance — **Silent Failure #4**, and the error bar yo… |
| `EVAL-15` | 119 | 💥 Calibration, abstention and significance — **Silent Failure #4**, and the error bar yo… |
| `EVAL-16` | 119 | 💥 Calibration, abstention and significance — **Silent Failure #4**, and the error bar yo… |

## `MM` — Multimodal (16 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `MM-01` | 120 | The general recipe — any modality becomes a sequence of vectors |
| `MM-02` | 121 | Images as patches — the Vision Transformer, built; 2D position and variable resolution |
| `MM-03` | 121 | Images as patches — the Vision Transformer, built; 2D position and variable resolution |
| `MM-04` | 122 | Contrastive pretraining — CLIP, InfoNCE, the shared space, and the limits of zero-shot |
| `MM-05` | 122 | Contrastive pretraining — CLIP, InfoNCE, the shared space, and the limits of zero-shot |
| `MM-06` | 123 | **Vision–language models** — the projector that bridges into Akshara, and the two-stage … |
| `MM-07` | 123 | **Vision–language models** — the projector that bridges into Akshara, and the two-stage … |
| `MM-08` | 124 | 💥 Audio understanding — spectrograms, Whisper's encoder–decoder, and its hallucination o… |
| `MM-09` | 124 | 💥 Audio understanding — spectrograms, Whisper's encoder–decoder, and its hallucination o… |
| `MM-10` | 125 | Audio tokenization — neural codecs and discrete speech units |
| `MM-11` | 126 | Video — frames, temporal modelling, frame sampling, and the token-per-second cost problem |
| `MM-12` | 126 | Video — frames, temporal modelling, frame sampling, and the token-per-second cost problem |
| `MM-13` | 127 | 🅿️ Any-to-any and unified models; OCR, documents, and the "just read the screenshot" trap |
| `MM-14` | 128 | 💥 Multimodal hallucination and evaluation — grounding failures, and why measuring them i… |
| `MM-15` | 128 | 💥 Multimodal hallucination and evaluation — grounding failures, and why measuring them i… |
| `MM-16` | 127 | 🅿️ Any-to-any and unified models; OCR, documents, and the "just read the screenshot" trap |

## `GEN` — Generative families (21 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `GEN-01` | 129 | The family tree — autoregressive, VAE, GAN, flow, diffusion, and what each one optimizes |
| `GEN-02` | 130 | Autoencoders and VAEs — the latent space, the ELBO, and the reparameterization trick |
| `GEN-03` | 130 | Autoencoders and VAEs — the latent space, the ELBO, and the reparameterization trick |
| `GEN-04` | 131 | 🅿️ GANs — the adversarial game, mode collapse, and why they faded |
| `GEN-05` | 131 | 🅿️ GANs — the adversarial game, mode collapse, and why they faded |
| `GEN-06` | 132 | Diffusion I — the forward noising process, and the closed form that makes it trainable |
| `GEN-07` | 133 | Diffusion II — the reverse process, the denoiser, and the objective that is just a regre… |
| `GEN-08` | 133 | Diffusion II — the reverse process, the denoiser, and the objective that is just a regre… |
| `GEN-09` | 134 | **Diffusion III** — a tiny diffusion model, trained on your own machine |
| `GEN-10` | 135 | Samplers and schedules — DDIM, step count vs quality, and what the noise schedule controls |
| `GEN-11` | 135 | Samplers and schedules — DDIM, step count vs quality, and what the noise schedule controls |
| `GEN-12` | 136 | Guidance — classifier guidance, classifier-free guidance, and the scale dial everyone tu… |
| `GEN-13` | 136 | Guidance — classifier guidance, classifier-free guidance, and the scale dial everyone tu… |
| `GEN-14` | 137 | Latent diffusion — the VAE compressor that made it affordable, and text conditioning by … |
| `GEN-15` | 137 | Latent diffusion — the VAE compressor that made it affordable, and text conditioning by … |
| `GEN-16` | 138 | Control and personalization — ControlNet, LoRA for images, DreamBooth, textual inversion |
| `GEN-17` | 138 | Control and personalization — ControlNet, LoRA for images, DreamBooth, textual inversion |
| `GEN-18` | 139 | Flow matching and rectified flow — what replaced DDPM, and why it is simpler |
| `GEN-19` | 140 | 🅿️ Video and audio generation; and 💥 evaluating generative models — FID, CLIP score, and… |
| `GEN-20` | 140 | 🅿️ Video and audio generation; and 💥 evaluating generative models — FID, CLIP score, and… |
| `GEN-21` | 140 | 🅿️ Video and audio generation; and 💥 evaluating generative models — FID, CLIP score, and… |

## `SAFE` — Safety (20 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `SAFE-01` | 61 | Where pretraining data comes from — sources, quality filtering, and consent at collectio… |
| `SAFE-02` | 141 | The threat model — who attacks a generative system, at which surface, for what |
| `SAFE-03` | 142 | Hallucination — the mechanism, the measurement, and the mitigations that actually move t… |
| `SAFE-04` | 142 | Hallucination — the mechanism, the measurement, and the mitigations that actually move t… |
| `SAFE-05` | 143 | 💥 Prompt injection and jailbreaks — direct, indirect, the lethal trifecta, and why "inst… |
| `SAFE-06` | 143 | 💥 Prompt injection and jailbreaks — direct, indirect, the lethal trifecta, and why "inst… |
| `SAFE-07` | 143 | 💥 Prompt injection and jailbreaks — direct, indirect, the lethal trifecta, and why "inst… |
| `SAFE-08` | 144 | 💥 Memorization — training-data extraction, membership inference, and PII in your own cor… |
| `SAFE-09` | 144 | 💥 Memorization — training-data extraction, membership inference, and PII in your own cor… |
| `SAFE-10` | 145 | 💥 Poisoning and the supply chain — backdoors, pickle deserialization, and model provenance |
| `SAFE-11` | 145 | 💥 Poisoning and the supply chain — backdoors, pickle deserialization, and model provenance |
| `SAFE-12` | 146 | Bias and fairness — where it enters, and how to measure it rather than deplore it |
| `SAFE-13` | 146 | Bias and fairness — where it enters, and how to measure it rather than deplore it |
| `SAFE-14` | 147 | Copyright, licensing and consent — auditing what Akshara was actually trained on |
| `SAFE-15` | 148 | Watermarking, provenance and deepfakes — C2PA, and the honest limits of detection |
| `SAFE-16` | 148 | Watermarking, provenance and deepfakes — C2PA, and the honest limits of detection |
| `SAFE-17` | 149 | Guardrails, the model card, the regulatory map 🅿️, and the release decision |
| `SAFE-18` | 149 | Guardrails, the model card, the regulatory map 🅿️, and the release decision |
| `SAFE-19` | 149 | Guardrails, the model card, the regulatory map 🅿️, and the release decision |
| `SAFE-20` | 149 | Guardrails, the model card, the regulatory map 🅿️, and the release decision |

## `SERVE` — Serving (16 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `SERVE-01` | 150 | Model formats and loading — safetensors, GGUF, memory-mapped weights, and the pickle you… |
| `SERVE-02` | 150 | Model formats and loading — safetensors, GGUF, memory-mapped weights, and the pickle you… |
| `SERVE-03` | 151 | **An inference server from scratch** — the request lifecycle, streaming over SSE, and ca… |
| `SERVE-04` | 151 | **An inference server from scratch** — the request lifecycle, streaming over SSE, and ca… |
| `SERVE-05` | 152 | 🔍 Now compare — vLLM, TGI, llama.cpp, Ollama; what they do that yours does not |
| `SERVE-06` | 152 | 🔍 Now compare — vLLM, TGI, llama.cpp, Ollama; what they do that yours does not |
| `SERVE-07` | 153 | Batching and scheduling in production — continuous batching, admission control, backpres… |
| `SERVE-08` | 153 | Batching and scheduling in production — continuous batching, admission control, backpres… |
| `SERVE-09` | 154 | 💥 Caching — prefix caching, semantic caching, and the day it returns the wrong answer |
| `SERVE-10` | 154 | 💥 Caching — prefix caching, semantic caching, and the day it returns the wrong answer |
| `SERVE-11` | 155 | Observability — latency percentiles, tokens/s, cost per request, and tracing one generat… |
| `SERVE-12` | 155 | Observability — latency percentiles, tokens/s, cost per request, and tracing one generat… |
| `SERVE-13` | 156 | Registry, versioning and the container — which weights answered that request? |
| `SERVE-14` | 156 | Registry, versioning and the container — which weights answered that request? |
| `SERVE-15` | 157 | Capacity planning and build-vs-buy — sizing a deployment from a latency target, with the… |
| `SERVE-16` | 157 | Capacity planning and build-vs-buy — sizing a deployment from a latency target, with the… |

## `OPS` — Operations (10 IDs)

| ID | Day | Day title |
| --- | --- | --- |
| `OPS-01` | 1 | Bootstrap & the map — repo, `.env` + `.gitignore`, uv + Python 3.12, the five ledgers, `… |
| `OPS-02` | 1 | Bootstrap & the map — repo, `.env` + `.gitignore`, uv + Python 3.12, the five ledgers, `… |
| `OPS-03` | 1 | Bootstrap & the map — repo, `.env` + `.gitignore`, uv + Python 3.12, the five ledgers, `… |
| `OPS-04` | 1 | Bootstrap & the map — repo, `.env` + `.gitignore`, uv + Python 3.12, the five ledgers, `… |
| `OPS-05` | 59 | Determinism, seeds, and testing ML code — what a unit test for a layer looks like; the `… |
| `OPS-06` | 59 | Determinism, seeds, and testing ML code — what a unit test for a layer looks like; the `… |
| `OPS-07` | 64 | Tokenizing a corpus at scale — the memmap file; and what never enters git |
| `OPS-08` | 67 | **The pretraining run** — launch, watch, and know whether the GPU is actually working; t… |
| `OPS-09` | 118 | Evals are tests — the regression gate in CI |
| `OPS-10` | 155 | Observability — latency percentiles, tokens/s, cost per request, and tracing one generat… |
