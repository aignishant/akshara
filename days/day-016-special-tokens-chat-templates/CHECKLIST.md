# Day 16 — Checklist

**Definition of done.** `./m done 16` refuses to commit until every box is ticked. A box you ticked
without running the thing is a lie to the only person it can hurt.

## Demo command

The one command that shows the day's headline result — one newline, three tokens, a different model:

```bash
uv run python days/day-016-special-tokens-chat-templates/lab/mismatch_01.py
```

- [ ] It prints `A (train) ids: 55`, `B (serve) ids: 58`, first divergence at **15**, and
      `positions still equal: 16/55`
- [ ] It prints both decodes, and you can see that **both are fine**

## Setup

- [ ] `uv add "jinja2==3.1.6"` run; `uv run python -c "import jinja2; print(jinja2.__version__)"` prints
      `3.1.6`
- [ ] `markupsafe` arrived as a transitive dependency; its version recorded
- [ ] `jinja2`'s licence read from the installed distribution — classifier **and** `LICENSE.txt` — not
      recalled
- [ ] `docs/MODELS.md` rows written **before** the two downloads (Principle 13)
- [ ] Both files downloaded at revision `12fd25f7…`; `sha256sum` matches the hub's §3 expected output
- [ ] Corpus hash confirmed: `9760f2b6d4340b97`, 113,283 bytes — the same corpus as Days 14 and 15

## Section 01 — The tokens themselves

- [ ] **1.1** read; check-yourself run — it prints `1000`, `1000`, `None`, `256`
- [ ] **1.1** four jobs named out loud, as jobs rather than token names
- [ ] **1.2** read; check-yourself run — `<|endoftext|>` is **8** tokens as text and **1** as a marker
- [ ] **1.2** you can say where in the pipeline the special-token match happens, and why that ordering
      makes the guarantee absolute
- [ ] **1.3** read; check-yourself run — `1000`, `1004`, `1003`, `1004`
- [ ] **1.3** you watched `E[-1] is E[999]` return `True` and can say why that is worse than an exception
- [ ] **1.4** read; check-yourself run — the second string is 25 characters with a **double space**
- [ ] **1.4** you can name the one behaviour `special=True` buys, and two it does not

## Section 02 — Attaching them

- [ ] **2.1** read; check-yourself run — `6 0` then `8 2`, mask `[1,0,0,0,0,0,0,1]`
- [ ] **2.1** you can state the rule that explains an all-zero mask in 1.4 and a non-zero one here
- [ ] **2.2** read; check-yourself run — `48` positions, `21` padding (43.8%), all three rows disagreeing
      at **14 of 16**
- [ ] **2.2** you can write the one-line loss mask that breaks when `pad_id == eos_id`, and say what it
      destroys
- [ ] **2.3** read; check-yourself run — `False`, `22 ids, eos present: True`, `27 ids, eos present: False`
- [ ] **2.3** 💥 you set `encode_special_tokens = True` and watched a control id disappear from user text
- [ ] **2.4** read; check-yourself run — `12 ids, round-trips=True` then `11 ids, round-trips=False`
- [ ] **2.4** 💥 **break it, watch it go red, fix it:** set `lstrip=True`, watch the round-trip that has
      held since Day 13 return `False`, then set it back and watch it pass

## Section 03 — The embedding matrix

- [ ] **3.1** read; check-yourself run — `(1004, 384)`, `385536` parameters, `1542144` bytes
- [ ] **3.1** you can say why token ids must be small and contiguous, in terms of the table
- [ ] **3.2** read; check-yourself run — `0.3917`, `0.0132`, `0.0336`, `6144 bytes = 0.400%`
- [ ] **3.2** you can state the precondition under which mean-initialisation is sound, and why it does not
      hold on a fresh table
- [ ] **3.3** read; check-yourself run — tied `28,311,552` at `54.00 MiB` bf16, logits `1.50 GiB`
- [ ] **3.3** you can explain why a tied logit is a similarity, without using the word "transpose"
- [ ] **3.4** read; check-yourself run — both widths print `sum(p)=1.000000` and **both print argmax 481**
- [ ] **3.4** 💥 you can name two metrics that would report the broken and correct models as identical

## Section 04 — Chat templates

- [ ] **4.1** read; check-yourself run — `3` messages, `170` characters, `3`/`3` markers, `6` newlines
- [ ] **4.1** you can say where the word "role" physically is in the `(T,)` id vector
- [ ] **4.2** read; check-yourself run — `97 ids` unregistered, `55 ids, 3 starts, 3 ends` registered
- [ ] **4.2** you can say which parts of a ChatML turn are special tokens and which are ordinary text,
      and why the split is where it is
- [ ] **4.3** read; check-yourself run — `170 chars, 55 ids` then `192 chars, 60 ids`
- [ ] **4.3** you can give **both** failure directions for `add_generation_prompt` and what each looks
      like in the output
- [ ] **4.4** 🔍 read; check-yourself run — `jinja2 3.1.6`, `equal=True` in both modes
- [ ] **4.4** 🔍 you can name at least one thing the library does that your nine-line function does not,
      and say whether you need it for your own template (Principle 3)
- [ ] **4.5** read; check-yourself run — `1 in -> 169 chars, 3 turns`, `2 in -> 128 chars, 3 turns`,
      `17 at ids 0 - 16`
- [ ] **4.5** you can name the clause that injects a system message and the exact condition that fires it
- [ ] **4.5** you can give the five questions to ask of any published template, in order

## Section 05 — Template mismatch

- [ ] **5.1** 💥 read; check-yourself run — `55`/`58`, divergence at `15`, `16/55`, `True True` on the
      round-trips
- [ ] **5.1** 💥 you listed the six earlier checks that pass on the broken pair, and said what each one
      actually asserts
- [ ] **5.2** read; check-yourself run — `72176cff468ded09`, `1b43eeb027dd3f9b`, `d87aff271ff8f676`,
      then `True`, `False`, `False`
- [ ] **5.2** you can say, in one sentence, the question the round-trip asks and why it cannot catch drift
- [ ] **5.2** you can name the three ways the fingerprint fails silently, and that all three are the probe
      set

## Build brief

- [ ] `lab/` has `fresh()`, written once and reused by every script
- [ ] `render_by_hand(messages, add_generation_prompt=False)` written **before** `jinja2` was imported (P3)
- [ ] Your hand renderer and your Jinja2 template agree **byte for byte** in both modes
- [ ] `resize(E, n_new, init)` written in plain Python; three initialisations compared by **norm**
- [ ] `fingerprint(template)` written; four templates give four distinct digests
- [ ] `TODO(me)` left **unsolved**: fingerprinting ids rather than the rendered string
- [ ] `TODO(me)` left **unsolved**: your own probe set, with a note on what each new probe distinguishes
- [ ] Nothing written into `akshara/` — the tokenizer becomes a module after Day 17

## Tests

- [ ] `tests/test_special_tokens.py` written and passing
- [ ] `tests/test_chat_template.py` written and passing
- [ ] Every test is CPU-only, offline, and seeds anything random (`random.Random(1337)`, not the global)
- [ ] **Break it, watch it go red, fix it — at least once, deliberately:** move one newline in your
      template, watch the id assertion in `test_chat_template.py` fail, confirm the **round-trip
      assertion still passes**, then put the newline back
- [ ] The tests that assert something does **not** happen are present and you can say why each is there:
      the un-grown head's softmax still sums to 1.0; the two heads share an argmax; the round-trip passes
      on all three templates
- [ ] `uv run python -m pytest -q -m "not gpu"` green
- [ ] `uv run ruff check .` and `uv run ruff format .` clean

## The five silent failures (plan §6)

- [ ] You can name which of the five this day is about — **#2, tokenizer / template mismatch** — and point
      at the five separate traps in the hub's §7 that are all it
- [ ] You can say how you would **detect** #2, and why the round-trip prescribed for it is not sufficient
      on its own
- [ ] You can name the one this day **foreshadows** (#3, the loss that counted padding) and the trap that
      does it (`pad_id == eos_id`, part 2.2)

## Compute budget

- [ ] Tier confirmed **T0**; GPU-minutes used: **0**
- [ ] Longest step recorded, with hardware — nothing today exceeds a fraction of a second
- [ ] You can name the one question this day **cannot** answer (whether vocabulary padding speeds up the
      matmul), and where its `TODO(measure: ...)` lives

## Ledger & commit

- [ ] `docs/PROGRESS.md` row pasted from §11, with the real commit sha
- [ ] `docs/PACKAGES.md` — **two rows**, dated, versions looked up live
- [ ] `docs/MODELS.md` — **two rows**, written before the download, with the revision SHA and both file
      hashes
- [ ] `docs/DATASETS.md` — **confirmed no rows**
- [ ] `docs/RUNS.md` — **confirmed no rows**
- [ ] `pyproject.toml` and `uv.lock` committed together
- [ ] `./m trace` and `./m tracker` re-run; `docs/TRACEABILITY.md` shows TOK-16 and TOK-17 closed on day 16
- [ ] `./m done 16` committed with the message from §11
