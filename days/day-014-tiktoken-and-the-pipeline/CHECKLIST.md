# Day 14 — CHECKLIST

**IDs closed:** TOK-12, TOK-13
**Principles served:** 1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18
**Parts:** 14 across 4 sections
**Compute tier:** T0 (laptop CPU) · GPU-minutes: 0 · longest step 39.0 s

> `./m done 14` refuses to commit while any box below is unticked. It cannot tell whether you were
> honest — that part is yours.

## Demo command

```bash
./m check && ./m status && git log --oneline -1
```

Expected: `OK all green`, a status line whose **written** count reads 15, then one commit reading
`day 014: 🔍 compare — tiktoken, the tokenizers pipeline, and the gap neither closes — closes TOK-12, TOK-13`.

---

## Setup — and the ledger comes first

- [ ] Day 13's checklist is fully ticked and `./m done 13` committed
- [ ] `./m scaffold 14` run; the lab directory exists
- [ ] Versions looked up **live** on PyPI, not recalled — `tiktoken==0.14.0`, `tokenizers==0.23.1`
- [ ] `uv add` run with exact `==` pins; `uv.lock` committed
- [ ] `regex` noted as a **transitive** dependency at `2026.7.19`, and you can say why it is not pinned directly
- [ ] **`docs/PACKAGES.md` rows written** — three, dated
- [ ] **`docs/MODELS.md` rows written BEFORE the first `get_encoding` call** — four rows, three encodings
- [ ] You can say why a `.tiktoken` file is permitted by Principle 13 where a pickle is not
- [ ] Corpus sha256 printed and compared against `9760f2b6d4340b97`; yours recorded

## TOK-12 — `tiktoken` (section 1)

- [ ] Read 1.1; ran its check-yourself
- [ ] Measured all four tokenizers on **one** `text` variable
- [ ] Trained a `tokenizers` BPE at `V = 1000` and measured the gap against your Day 13 count
- [ ] Can say how much of the 39% compression gap is your code (measured figure)
- [ ] Timed with **best-of-5**, and can say why the minimum rather than the mean
- [ ] Can say why that reasoning is *not* the same as "report three seeds and their spread"
- [ ] Read 1.2; ran its check-yourself
- [ ] Read `r50k_pat_str` from `tiktoken_ext/openai_public.py` yourself — not from this document
- [ ] Ran the published pattern under `regex` and counted the disagreements with Day 13's approximation
- [ ] **Found the culprit character and named its Unicode category**
- [ ] Confirmed possessive `++` compiles in stdlib `re` on your Python, and can say what actually blocked Day 13
- [ ] Read 1.3; ran its check-yourself
- [ ] Opened all three file formats and can describe each in one sentence
- [ ] Can explain, in terms of Day 13's `encode_chunk`, why `cl100k_base` needs no merge list
- [ ] Asserted the rank column is dense and ordered
- [ ] Can say what happens if you ship `encoder.json` without `vocab.bpe`
- [ ] Read 1.4; ran its check-yourself
- [ ] Measured agreement between your merge list and `gpt2`'s at five window sizes
- [ ] **Confirmed the agreement decays monotonically on your corpus** — and if it did not, found out why
- [ ] Decoded the merges that are yours alone and can name three that are markdown rather than English
- [ ] Can state what the direction of the overlap comparison changes
- [ ] Read 1.5; ran its check-yourself
- [ ] Encoded the same string three ways and got 9 ids, 4 ids, and a `ValueError`
- [ ] **Observed that both id sequences round-trip to the same string**
- [ ] Can state the rule for `encode` versus `encode_ordinary` in one sentence
- [ ] Can describe the prompt-injection exploit in two sentences

## TOK-13 — the `tokenizers` pipeline (section 2)

- [ ] Read 2.1; ran its check-yourself
- [ ] Can name the five stages in order and say which one changes the text
- [ ] Ran each stage separately and saw two of them are `None`
- [ ] **Broke the decoder deliberately** and saw `Ġ` leak into the output
- [ ] Can say why nothing checks that stage 5 inverts stage 2
- [ ] Read 2.2; ran its check-yourself
- [ ] Compared your merge list against the Rust trainer's, positionally and as sets
- [ ] Found the first divergence and **replayed your trainer to prove it was a tie, not a mistake**
- [ ] Can name the line in your Day 13 trainer that decided it
- [ ] Can say what "stable tie-break" means and what the unstable version depends on
- [ ] Read 2.3; ran its check-yourself
- [ ] Printed every token beside the source span it came from
- [ ] Used `word_ids` to expand a per-chunk label to per-token, without string matching
- [ ] **Ran the tiling assertion on ASCII and on `café`, and watched it pass then fail**
- [ ] Can say why two tokens sharing one span is honest rather than a bug
- [ ] Can name the exact line in your Day 13 `tokenize` where the positions are lost
- [ ] Read 2.4; ran its check-yourself
- [ ] Padded a ragged batch and confirmed the mask recovers the original lengths exactly
- [ ] Measured the padding waste on your own batch
- [ ] **Set `pad_id=0` deliberately and saw `Hi` decode as `Hi!`**
- [ ] Truncated a document and confirmed the attention mask is **all ones**
- [ ] Checked `overflowing` and can say why nothing computes it for you
- [ ] Can say which side padding goes on for a decoder-only model, and the symptom of getting it wrong
- [ ] Read 2.5; ran its check-yourself
- [ ] Switched on `NFKC` and watched `decode(encode(s)) == s` become `False`
- [ ] Printed `normalize_str` output and its length beside the input's
- [ ] Found a span claimed by four different tokens
- [ ] Measured a word that got **cheaper** and one that got **dearer** under the same normalizer
- [ ] Can state the difference between canonical and compatibility normalization

## Section 3 — the remaining gap

- [ ] Read 3.1; ran its check-yourself
- [ ] Saved a tokenizer and read all nine top-level keys
- [ ] Can name the two keys that are not stages but still change the output
- [ ] Can say what `byte_fallback`, `dropout`, `unk_token` and `ignore_merges` do, and which two Day 15 needs
- [ ] Built a `TemplateProcessing` post-processor and saw `special_tokens_mask` become non-zero
- [ ] **Round-tripped through the FILE** — saved, reloaded, compared ids — with a non-ASCII probe
- [ ] Read 3.2; ran its check-yourself
- [ ] Measured the per-character rate for at least three non-English scripts
- [ ] **Confirmed your own tokenizer emits one token per byte for them, and can say why**
- [ ] Normalized by the English rate and can say why the raw counts mislead
- [ ] Can state the difference between zero-OOV and affordability in one sentence
- [ ] Can give the compute multiplier for a 6.88× token multiplier, and why it is not 6.88
- [ ] Read 3.3; ran its check-yourself
- [ ] Reproduced the mismatch: loaded the file, rebuilt one stage, and got 4/4 different ids
- [ ] **Confirmed both paths round-trip perfectly**
- [ ] Wrote `assert_same_tokenizer` and watched it go red
- [ ] Ran the **positive control**: a clean reload agrees on every probe
- [ ] Can name three structural controls that prevent this class of bug

## Section 4 — together

- [ ] Read 4.1; ran its check-yourself
- [ ] Built the six-row table from **one** `text` variable and **your** corpus hash
- [ ] Can say which row compresses best and which column vetoes it
- [ ] Can say what rows 4 and 5 agreeing establishes — and what it does not
- [ ] Can name three columns the table lacks, and which one costs a training run

## The eval that can go red (Principle 11)

- [ ] `tests/test_tokenizer_compare.py` exists and runs CPU-only and deterministically
- [ ] **Observed red before green:** pre-tokenizer rebuilt after load → `assert_same_tokenizer` fails 4/4
- [ ] **Observed green where you expected red:** comparing strings instead of ids → nothing fails
- [ ] **Observed red before green:** `pad_id=0` → the `pad_id >= 256` assertion fails
- [ ] **Observed red before green:** mask dropped → lengths not recovered
- [ ] **Observed red before green:** `NFKC` added → the round trip goes `False`
- [ ] **Observed red before green:** tiling assertion on `café` → fails, and passes on ASCII
- [ ] You have at least **three** assertions that assert a *failure*, and can say why each pins a boundary

## Silent failures ruled out (plan §6)

- [ ] **#2 tokenizer/template mismatch** — you reproduced it deliberately, and can name four real-world
      forms it takes (template in code, normalizer drift, library version, merge list travelling alone)
- [ ] **#3 the loss counted padding** — you can describe what padding looks like in the mask and name the
      two-line check from §6
- [ ] **#5 evaluated on the format you trained on** — you can name **three** checks in this day that pass on
      an English-only probe list while something is wrong

## Honesty (Principle 8)

- [ ] Every number you wrote down is **measured on your machine**, with the corpus hash beside it
- [ ] You did **not** copy this day's `0.043%`, `46291`, `9.9x`, `6.88x`, `28889`, `551`, `59.7%` or
      `2.57x` figures into your notes as if they were yours
- [ ] Your **timings** carry your own hardware line, and you can say which numbers are hardware-dependent
- [ ] Your notes record that `enc._pat_str` is a **private** attribute, and why it is not fit for `akshara/`
- [ ] Your notes record that possessive quantifiers work in stdlib `re` on Python 3.11+ — the opposite of
      what a reasonable person would guess from Day 13
- [ ] Part 3.2's language probes are recorded with the exact sentences used, since the rates depend on them

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] Longest single step recorded, with hardware
- [ ] You can name the one question this day **cannot** answer, and what it would cost to answer

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **three rows**, dated, versions looked up live
- [ ] `docs/MODELS.md` — **four rows**, and you can confirm they were written *before* the first load
- [ ] `docs/DATASETS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**, and you can say why a tokenizer training is not a run
- [ ] `pyproject.toml` and `uv.lock` committed together
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-12 and TOK-13 closed on day 14
- [ ] `./m done 14` committed with the message from §11
