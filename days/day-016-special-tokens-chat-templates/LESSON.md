---
day: 16
phase: 2
phase_name: "Text becomes numbers"
title: "Special tokens & chat templates — BOS/EOS/PAD/UNK, resizing an embedding, and Silent Failure #2"
ids: ["TOK-16", "TOK-17"]
principles: [1, 2, 3, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 20]
kind: build
plan_version: "v1.3.0"
parts: 19
compute_tier: T0
generated: "2026-08-29"
status: written
lab_scaffolded: true
commit: ""
---

# Day 16 — Special tokens & chat templates

> **Yesterday** three tokenizer families disagreed about how to build a vocabulary, and exactly three
> of nine were both lossless and complete.
> **Today** the vocabulary gains four entries that are not text at all, the model gains four rows to
> hold them, and one newline in a template quietly changes 39 of 55 token positions.
> **Tomorrow** the failure lab: numbers, whitespace, code, multilingual inflation, token healing, and
> how large a vocabulary should actually be.

---

## §1 Where we are

Seven days have built a machine that turns text into integers and integers back into text, losslessly, for
any string in any script. It is finished, and it cannot say a single thing that is not text.

It cannot say *stop*. It cannot say *this position is empty*. It cannot say *a new document begins here*.
Those are not sentences the machine is bad at — they are outside what it represents at all, in the same way
that a tape measure has no way to express *the wall is missing*.

Think of a stack of exam booklets. The answers are written in blue ink on ruled lines. So is the roll number
at the top, so is the word *END* under the last answer, and so are the diagonal lines through the pages
nobody used. Four marks that are not answers, in the same ink, on the same lines — and the whole system
works only because everyone in the hall was told the same four marks, and because *END* is not a word
anybody would write as part of an answer.

Today puts those four marks in the vocabulary. Then it does the arithmetic they cost: four more rows in a
table the model looks tokens up in, and four more columns in the table it produces answers from — and shows
what happens when you grow one and forget the other, which is nothing, no error, ever, and a model that can
never stop talking.

Then a harder thing. A conversation is a list of turns; a model reads one flat string. Something has to
flatten it, and that something is a convention nobody enforces. Change one character of it between the day
you train and the day you serve and everything still works: the strings round-trip, the ids decode, the
model answers fluently. It is simply reading a format it has never seen. That is Silent Failure #2, it has
its home here, and today is where you build the check that catches it — after watching six checks you
already trusted go green on the broken pair.

---

## §2 The map

Nineteen parts across five sections. Sections 1, 2 and 3 close `TOK-16`; section 4 closes `TOK-17`; section
5 is where the two meet, which is where the day's headline failure lives.

### 01 — The tokens themselves (`TOK-16`)

*What a special token is, and what "special" does and does not buy.*

| Part | Title | Level |
| --- | --- | --- |
| 1.1 | [Four jobs, four tokens](parts/01-special-tokens/1.1-four-jobs-four-tokens.md) | foundation |
| 1.2 | [A special token has to be one token](parts/01-special-tokens/1.2-a-special-token-has-to-be-one-token.md) | working |
| 1.3 | [Added tokens sit above the vocabulary](parts/01-special-tokens/1.3-added-tokens-sit-above-the-vocabulary.md) | working |
| 1.4 | ["Special" means exactly one thing: decode drops it](parts/01-special-tokens/1.4-special-means-decode-drops-it.md) | working |

### 02 — Attaching them (`TOK-16`)

*Where the markers actually get placed, and the two ways that goes wrong on purpose.*

| Part | Title | Level |
| --- | --- | --- |
| 2.1 | [The post-processor is where BOS and EOS come from](parts/02-attaching-them/2.1-the-post-processor-adds-bos-and-eos.md) | working |
| 2.2 | [The pad token that is also the end token](parts/02-attaching-them/2.2-the-pad-token-that-is-also-the-end-token.md) | production |
| 2.3 | 💥 [The library that did not raise](parts/02-attaching-them/2.3-the-library-that-did-not-raise.md) | production |
| 2.4 | 💥 [`lstrip`, and the space that never came back](parts/02-attaching-them/2.4-lstrip-and-the-space-that-never-came-back.md) | production |

### 03 — The embedding matrix (`TOK-16`)

*Where a token id becomes a row, what growing the table costs, and the resize that half-happens.*

| Part | Title | Level |
| --- | --- | --- |
| 3.1 | [One row per id](parts/03-the-embedding-matrix/3.1-one-row-per-id.md) | foundation |
| 3.2 | [Growing the table, and what goes in the new rows](parts/03-the-embedding-matrix/3.2-growing-the-table.md) | working |
| 3.3 | [The second matrix, and weight tying](parts/03-the-embedding-matrix/3.3-the-second-matrix.md) | working |
| 3.4 | 💥 [The head that was never grown](parts/03-the-embedding-matrix/3.4-the-head-that-was-never-grown.md) | production |

### 04 — Chat templates (`TOK-17`)

*Build the template by hand, then open the library, then read one you did not write.*

| Part | Title | Level |
| --- | --- | --- |
| 4.1 | [A list of messages becomes one string](parts/04-chat-templates/4.1-a-list-becomes-one-string.md) | foundation |
| 4.2 | [Roles as markers, built by hand](parts/04-chat-templates/4.2-roles-as-markers.md) | working |
| 4.3 | [The generation prompt — the turn you open and do not close](parts/04-chat-templates/4.3-the-generation-prompt.md) | working |
| 4.4 | 🔍 [The same template, as a template](parts/04-chat-templates/4.4-the-same-template-as-a-template.md) | working |
| 4.5 | [A published template, read line by line](parts/04-chat-templates/4.5-a-published-template-read-line-by-line.md) | production |

### 05 — Template mismatch (`TOK-16` + `TOK-17`)

*Silent Failure #2, measured — and the check that catches it, which is not the one you were told.*

| Part | Title | Level |
| --- | --- | --- |
| 5.1 | 💥 [One character, three tokens, a different model](parts/05-template-mismatch/5.1-one-character-three-tokens-a-different-model.md) | production |
| 5.2 | [The check the round-trip cannot make](parts/05-template-mismatch/5.2-the-check-the-round-trip-cannot-make.md) | production |

---

## §3 Setup — run this

Sections 1, 2 and 3 need only `tokenizers==0.23.1`, already pinned on Day 14. Sections 4 and 5 add one
package — the engine every published chat template is written in — with its version looked up live on PyPI
on 2026-08-29 (Principle 6):

```bash
uv add "jinja2==3.1.6"
uv run python -c "import jinja2, tokenizers; print(jinja2.__version__, tokenizers.__version__)"
```

Expected: `3.1.6 0.23.1`. `markupsafe==3.0.3` arrives as a transitive dependency.

**Licence, read from the installed distribution rather than recalled**, because `jinja2`'s metadata has no
`License-Expression` field and PyPI's JSON returns `null`:

```bash
grep -i "^Classifier: License" .venv/Lib/site-packages/jinja2-3.1.6.dist-info/METADATA
head -1 .venv/Lib/site-packages/jinja2-3.1.6.dist-info/licenses/LICENSE.txt
```

Expected: `Classifier: License :: OSI Approved :: BSD License`, then `Copyright 2007 Pallets`.

**Two files are downloaded today, and both are JSON — no weights, no pickle** (Principle 13). Write the
`docs/MODELS.md` rows from §11 **before** running this:

```bash
mkdir -p days/day-016-special-tokens-chat-templates/lab
cd days/day-016-special-tokens-chat-templates/lab
REV=12fd25f77366fa6b3b4b768ec3050bf629380bac
REPO=https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct/resolve/$REV
curl -sL "$REPO/tokenizer_config.json" -o tokenizer_config.json
curl -sL "$REPO/config.json" -o config.json
sha256sum tokenizer_config.json config.json
cd -
```

Expected hashes, observed 2026-08-29:

```text
4ec77d44f62efeb38d7e044a1db318f6a939438425312dfa333b8382dbad98df  tokenizer_config.json
8eb740e8bbe4cff95ea7b4588d17a2432deb16e8075bc5828ff7ba9be94d982a  config.json
```

**If you have no network**, sections 1, 2, 3 and parts 4.1 to 4.4 run in full — everything is trained
locally from this repo's own plan. Only part 4.5, and the "published" row of part 5.2's fingerprint table,
need the two downloads.

The corpus is `docs/00_MASTER_PLAN.md`, sha256 `9760f2b6d4340b97`, 113,283 bytes, 110,837 code points — the
same corpus and the same byte-level BPE settings as Days 14 and 15, so every count today is comparable with
theirs.

---

## §4 Build brief

Principle 3 twice over: the chat template is hand-rolled before Jinja2 is imported, and the embedding
resize is hand-rolled in plain Python before any framework's helper is discussed.

In `lab/`, produce:

1. **`fresh()`** — the byte-level BPE tokenizer at `V = 1000`, trained on the plan. Every part reuses it;
   write it once.
2. **`render_by_hand(messages, add_generation_prompt=False)`** — part 4.2 and 4.3's template, in nine
   lines, before you open `jinja2`. It must agree **byte for byte** with the Jinja2 version in part 4.4.
   Mine agreed in both modes.
3. **`resize(E, n_new, init)`** — grow a `(V, C)` list-of-lists by `n_new` rows. Compare three
   initialisations by the **norm** of the new row against the mean row norm of the table, as part 3.2 does.
4. **`fingerprint(template)`** — part 5.2's probe-set hash. Then `TODO(me)`: extend it to fingerprint the
   **ids** rather than the rendered string, so one value pins the tokenizer and the template together. Part
   5.2's *In production* says why that is the version worth shipping and deliberately does not write it.
5. **`TODO(me)`: your own probe set.** Part 5.2 lists three ways the check fails silently and all three are
   the probes. Add the shapes this day's six do not cover — a role the template does not know, content
   containing a marker, a conversation ending on a system message — and record what each new probe
   distinguishes.

Do **not** write anything into `akshara/`. The tokenizer becomes a committed module after Day 17, once the
vocabulary size has been chosen with the pathologies of TOK-18 to TOK-20 in view rather than before them.

---

## §5 The eval that must be able to fail

`tests/test_special_tokens.py` and `tests/test_chat_template.py`, CPU-only, deterministic, offline.

| Change | Test that must fail |
| --- | --- |
| Call `add_tokens` instead of `add_special_tokens` (1.4) | `decode()` keeps the marker; the double space never appears |
| Size the model from `get_vocab_size(with_added_tokens=False)` (1.3) | the config check reports 1000 rows against id 1003 |
| Drop the post-processor (2.1) | `num_special_tokens_to_add` returns 0 and the context budget is wrong by 2 |
| Mask the loss by `id == pad_id` when pad is eos (2.2) | positions found by id and by mask disagree |
| Leave `encode_special_tokens` at its default on user text (2.3) | a control id appears in a user string |
| `AddedToken(..., lstrip=True)` (2.4) | the round-trip that has held since Day 13 returns `False` |
| Grow the embedding and not the head (3.4) | **nothing fails** — assert that softmax still sums to 1.0, and that both heads share an argmax |
| Initialise new rows with the mean of a fresh table (3.2) | the norm band check rejects 0.0132 against a floor of 0.1959 |
| Render without `StrictUndefined` and misspell a keyword (4.4) | 22 characters come back and no exception |
| Move one newline in the template (5.1) | ids differ; **and the round-trip still passes** — assert both |
| Change the generation prompt's last character (5.1) | lengths match, one id differs, every length check passes |
| Fingerprint two behaviourally different templates (5.2) | four templates must give four distinct digests |

**Three of those assert that something does *not* fail**, and one asserts that a check you trust reports
green on a broken pair. By Day 16 that should be the normal shape of a test: a property is only pinned once
you have pinned what it cannot see.

---

## §6 Compute budget

**Tier: T0 — laptop CPU. GPU-minutes: 0.**

Measured on this machine (11th Gen Intel Core i3-1115G4, 4 logical CPUs, 11.7 GiB RAM, Windows 11),
2026-08-29:

| Step | Cost |
| --- | --- |
| `uv add jinja2` | one-off; `jinja2` plus `markupsafe`, both pure-Python wheels |
| Two config downloads | 3,764 bytes and one config; no weights |
| Train BPE, `V = 1000` | 0.068 s |
| `add_special_tokens` for three tokens | 0.00005 s |
| 100 × `encode` of 5,000 characters | 0.257 s |
| Every embedding measurement in section 3 | plain Python, `V = 1004`, `C = 384`; under a second each |
| Every render and fingerprint in sections 4 and 5 | string operations; unmeasurably fast |

Nothing today trains a model, so nothing today is slow. That is itself the point of the day: every decision
made here is cheap to make and expensive to revisit, because the run that depends on it is Day 67's.

**The question this day cannot answer:** whether padding a vocabulary to a round multiple — the `49152 = 48
× 1024` measured in part 3.2 — actually speeds up the matmul. That needs a GPU and a timed benchmark. It is
T2 🅿️ here, the memory arithmetic is worked in part 3.2, and the exact command that would measure it is
left in that part as a `TODO(measure: ...)` rather than a guess.

---

## §7 Traps

| # | Trap | Where |
| --- | --- | --- |
| 1 | `<\|endoftext\|>` as plain text is **8 tokens**, and `end` and `ext` occur in ordinary prose | 1.2 |
| 2 | `get_vocab_size()` has two correct answers, 1000 and 1004, and the smaller one looks like the default | 1.3 |
| 3 | `E[-1]` does not raise — a negative id silently reads the last row | 1.3, 3.1 |
| 4 | `special=True` buys **only** decode-time removal; the encoder is unaffected | 1.4 |
| 5 | `special_tokens_mask` comes from the **post-processor**, not from `special=True` | 1.4, 2.1 |
| 6 | `decode()` defaults to `skip_special_tokens=True` and leaves a **double space** | 1.4 |
| 7 | `TemplateProcessing` ignores the vocabulary; every literal must be in `special_tokens=` | 2.1 |
| 8 | `pad_token_id == eos_token_id` on a real model — an id-based loss mask destroys every real EOS | 2.2 |
| 9 | `encode_special_tokens` is inverted: `True` means *do not* treat them as special | 2.3 |
| 10 | `lstrip=True` eats the preceding whitespace and breaks the round-trip, silently | 2.4 |
| 11 | Mean-initialisation on a **fresh** table gives a row 3.4% the length of a typical one | 3.2 |
| 12 | Grow the embedding, forget the head: softmax still sums to 1.0 and the argmax is unchanged | 3.4 |
| 13 | Jinja2's default `Undefined` renders a whole conversation as 22 characters | 4.4 |
| 14 | A published template injects a system message you did not write — 1 message in, 3 turns out | 4.5 |
| 15 | One newline moved: 55 ids become 58, diverging at position 15, **16 of 55 still matching** | 5.1 |
| 16 | A space instead of a newline: same length, one id different, at the last position | 5.1 |
| 17 | The round-trip check passes on **all three** templates | 5.1, 5.2 |

**Named silent failure: #2 — tokenizer / template mismatch** (plan §6). It has its home on this day. Traps
8, 12, 15, 16 and 17 are all it, arriving from five different directions, and part 5.2 is the check that
sees them. Trap 8 also foreshadows Silent Failure #3 — *the loss that counted padding* — which lands on Day
57.

---

## §8 Verify before you code

Principle 7. Everything below was checked against the installed package or the pinned file on 2026-08-29,
at the version actually used.

| Symbol or fact | How it was verified |
| --- | --- |
| `jinja2.__version__` | imported and printed: `3.1.6`; resolved live from `https://pypi.org/pypi/jinja2/json` |
| `jinja2` licence | `Classifier: License :: OSI Approved :: BSD License` from the installed `METADATA`; `Copyright 2007 Pallets` from `LICENSE.txt`. There is **no** `License-Expression` field |
| `Tokenizer.add_special_tokens` | docstring read from the installed `tokenizers` 0.23.1; returns the count created |
| `Tokenizer.decode(skip_special_tokens=)` | docstring read: defaults to `True`. Confirmed by measuring the double space |
| `Tokenizer.encode_special_tokens` | **probed, not read.** The docstring says *"Whether to use the special tokens or not"*, which does not disambiguate; the measurement in part 2.3 establishes that `True` means *do not parse them* |
| `Tokenizer.get_added_tokens_decoder()` | called; returns `{id: AddedToken}` with all five flags visible |
| `AddedToken(lstrip=, rstrip=, single_word=, normalized=, special=)` | docstring read, then `lstrip=True` exercised and the round-trip watched to fail |
| `processors.TemplateProcessing(single=, special_tokens=)` | constructed; the failure path probed — it raises `ValueError: Missing SpecialToken(s) with id(s)` naming *every* undeclared literal, including one that is in the vocabulary |
| `Tokenizer.num_special_tokens_to_add(False)` | called before and after installing the post-processor: `0` then `2` |
| `jinja2.StrictUndefined` | exercised both ways: raises `UndefinedError: 'messages' is undefined`; without it the same input renders 22 characters |
| `hashlib.sha256` | stdlib; used with an explicit `utf-8` encode and a NUL separator |
| model revision `12fd25f7…` | read from `https://huggingface.co/api/models/HuggingFaceTB/SmolLM2-135M-Instruct`, together with `license: apache-2.0` and the presence of `model.safetensors` |
| the chat template itself | read from `tokenizer_config.json` **at that revision**, sha256 `4ec77d44…`, and rendered rather than paraphrased |

Three honesty notes. **`encode_special_tokens`'s docstring does not answer the question its name raises** —
the behaviour in part 2.3 came from probing, and the part says so. **`TemplateProcessing` reported `<|eos|>`
as missing when it was in the vocabulary**, which was surprising until the rule became clear: the
`special_tokens=` argument is the only place it looks. And **the published template does not raise on an
empty message list** — this document expected it to, wrote that it would, and was wrong; the measurement is
in part 4.5 and the corrected finding is that it renders a bare generation prompt instead.

`torch` and `transformers` are **not** pinned in this repository, so no claim is made about
`resize_token_embeddings` or about any CUDA error text. Parts 3.2 and 3.3 leave the exact lookup commands
instead (Principle 8).

---

## §9 Say it in an interview

**"What is a special token?"** An ordinary vocabulary entry with a control meaning, and the only thing the
`special` flag actually buys is that `decode` drops it by default. Encoding is identical either way — same
id, same token count, and the `special_tokens_mask` is all zeros in both cases, because that mask comes from
the post-processor rather than from the flag. What makes the token usable is that it is matched **before**
the merge loop runs, so nothing can split it: measured, `<|endoftext|>` is 8 tokens as text and 1 as a
registered marker.

**"You add four special tokens to a pretrained model and it stops working. What happened?"** Almost certainly
the vocabulary size. `get_vocab_size(with_added_tokens=False)` still returns the trained size, so anything
sized from it is short by exactly the number you added. If it threw an `IndexError` you were lucky. If it did
not, the head was never grown — and then the softmax over the smaller width is a perfectly valid
distribution that sums to 1.0, the argmax is unchanged, and the four new tokens are not unlikely, they are
outside the sample space. Tied weights make that structurally impossible, which is a better argument for
tying than the memory saving.

**"How do you initialise new embedding rows?"** The common advice is the mean of the existing rows, and the
precondition matters more than the advice: on a freshly initialised zero-centred table I measured the mean
row at norm 0.0132 against a typical row's 0.3917 — 3.4%, essentially a zero row. On a *trained* table the
rows are not zero-centred and the mean genuinely points somewhere. Either way I check the new row's norm
against the existing mean, which is one line.

**"What is a chat template mismatch?"** One tokenizer, byte-identical, two templates differing by a single
newline: 55 ids becomes 58, they diverge at position 15 of 55, and only 16 shared positions still match.
Both round-trip. Both decode cleanly. Nothing raises. And the variant where I changed the generation
prompt's last character from a newline to a space produced sequences of *identical length* differing in one
id — at the last position, which is the one that conditions the model's first output token.

**"So how do you catch it?"** Not with a round-trip: it passed on all three of my templates, because it asks
whether the tokenizer preserves a string and only ever sees one. The check is a fingerprint — render a fixed
probe set through the template, hash the output, record it in the run config, verify it at service startup.
Mine gave `72176cff` for the training template and `1b43eeb0` for the one-newline variant. The hard part is
the probe set: it has to contain the input shapes that turn each of the template's clauses on, or two
behaviourally different templates fingerprint the same.

**"Anything surprising in a real template?"** The one I pinned injects a default system message when your
conversation does not start with one. One 21-character user message renders as three turns and 169
characters. If your training data was built by your own renderer and your serving path uses the model's, the
model sees 98 characters of instructions at inference that were never in a single training example.

---

## §10 Done when

- `CHECKLIST.md` is fully ticked.
- `./m depth 16` is green.
- Your `render_by_hand` agrees byte for byte with your Jinja2 template, in both modes.
- Your `fingerprint` gives four different digests for the four templates in part 5.2.
- You have watched the un-grown head produce a softmax that sums to exactly 1.0, and can say why that is
  worse than one that does not.
- You can name the six checks from earlier in this day that pass on part 5.1's broken pair, and say what
  each one actually asserts.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append verbatim, with your real commit sha:

```text
| 16 | 2026-08-29 | TOK-16, TOK-17 | 19 | T0 | <commit sha> | ✅ |
```

**`docs/PACKAGES.md`** — one row:

```text
| `jinja2` | 3.1.6 | 2026-08-29 | 16 | The engine every published chat template is written in (TOK-17). Added after the hand-rolled renderer exists (P3); part 4.4 asserts the two agree byte for byte. Version read live from PyPI on 2026-08-29; licence BSD-3-Clause read from the installed distribution's classifier and LICENSE.txt, since the METADATA carries no License-Expression. |
| `markupsafe` | 3.0.3 | 2026-08-29 | 16 | Transitive dependency of `jinja2`. Not pinned directly; resolved by `uv`. Licence `BSD-3-Clause` read from the installed distribution METADATA. |
```

**`docs/MODELS.md`** — two rows, written **before** the download (Principle 13):

```text
| `SmolLM2-135M-Instruct` tokenizer config | `huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct` | `12fd25f77366fa6b3b4b768ec3050bf629380bac` (file sha256 `4ec77d44f62efeb38d7e044a1db318f6a939438425312dfa333b8382dbad98df`) | Apache-2.0 | JSON | n/a — config only | 2026-08-29 | 16 | The published chat template read verbatim in part 4.5, and the `bos`/`eos`/`pad` token strings measured in part 2.2. **Not a pickle** (P13); no weights downloaded. |
| `SmolLM2-135M-Instruct` model config | `huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct` | `12fd25f77366fa6b3b4b768ec3050bf629380bac` (file sha256 `8eb740e8bbe4cff95ea7b4588d17a2432deb16e8075bc5828ff7ba9be94d982a`) | Apache-2.0 | JSON | n/a — config only | 2026-08-29 | 16 | `vocab_size: 49152`, `hidden_size: 576`, `tie_word_embeddings: True`, `pad_token_id == eos_token_id == 2` — the measured numbers behind parts 2.2, 3.2 and 3.3. Repo offers `model.safetensors`; no weights are downloaded today. |
```

**`docs/DATASETS.md`** — no rows. The corpus is this repo's own plan.

**`docs/RUNS.md`** — no rows. Nothing was trained that produces weights.

**Commit:**

```text
day 016: special tokens and chat templates — closes TOK-16, TOK-17
```
