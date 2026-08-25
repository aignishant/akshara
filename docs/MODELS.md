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
