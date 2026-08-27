# Model Ledger — Project Akshara

Append-only. Every pretrained checkpoint gets a row **before it is loaded** (Principle 13).

**Format must be `safetensors`.** Principle 13: never load a pickle you did not create. A
`pytorch_model.bin` is a pickle, and `torch.load` on an untrusted pickle executes arbitrary code at
load time (SAFE-11). If a repo offers only `.bin`, the row says so and the day says why it is
nevertheless safe — or the model is not used.

**Pin the revision SHA.** `main` moves. Two runs against "the same model" on different days are two
different experiments if you did not pin (plan §5.1).

Checkpoints **you** train are not in this table — they are in `docs/RUNS.md`, keyed by run id.

| Model | Repo | Revision SHA | Licence | Format | Params | Date | Day | Why |
| ----- | ---- | ------------ | ------- | ------ | ------ | ---- | --- | --- |
| `gpt2` BPE ranks | `openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe` | sha256 `1ce1664773c50f3e0cc8842619a93edc4624525b728b188a9e0be33b7726adc5` | MIT (via `tiktoken`) | text (`vocab.bpe`) | n/a — vocabulary only | 2026-08-27 | 14 | The published GPT-2 merge list, to compare against the one trained on Day 12. **Not a pickle** (P13); `tiktoken` verifies this hash on download. |
| `gpt2` encoder | `openaipublic.blob.core.windows.net/gpt-2/encodings/main/encoder.json` | sha256 `196139668be63f3b5d6574427317ae82f612a97c5d1cdaf36ed2256dbf636783` | MIT (via `tiktoken`) | JSON | n/a — vocabulary only | 2026-08-27 | 14 | The token→id table paired with the merge list above. |
| `cl100k_base` ranks | `openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken` | sha256 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` | MIT (via `tiktoken`) | text (`.tiktoken`) | n/a — vocabulary only | 2026-08-27 | 14 | A later, larger vocabulary with the three-digit number cap Day 13 part 2.4 quoted. |
| `o200k_base` ranks | `openaipublic.blob.core.windows.net/encodings/o200k_base.tiktoken` | sha256 `446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d` | MIT (via `tiktoken`) | text (`.tiktoken`) | n/a — vocabulary only | 2026-08-27 | 14 | The multilingual vocabulary part 3.2 measures the Hindi tax against. |
