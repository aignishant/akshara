---
name: day-akshara
description: Generate the hub, the parts/ sub-documents, the lab scaffold and the checklist for a given day of the Akshara plan
argument-hint: [day-number]
---

# Generate Day $ARGUMENTS of the Akshara plan (v1.1.0 — hub + `parts/` + paper parts)

> **Read `docs/00_MASTER_PLAN.md` §25 before writing a single line, and §6 before writing a single
> line of code.** §25 is the depth contract this skill implements; §6 is the five silent failures
> that make generative work go wrong quietly. This skill is the procedure; the plan is the standard.

## The five commitments (§25.1 + §25.10 — everything below follows from these)

1. **One idea per document.** If it needs "also" to introduce its second half, it is two documents.
2. **No clocks.** Never write a time estimate, a duration, an "estimated hours" field, or a pace —
   not in frontmatter, not in prose, not in the checklist. **Never trim an explanation because the
   day is getting long — split it into another part instead.**
3. **Zero to production, in one document.** Open where a reader who has never heard of the idea can
   stand. End where a professional stands: the real-system version, what breaks at scale, what a
   research engineer writes instead, what a reviewer says, what an interviewer probes.
4. **Every number has a provenance.** Measured here — with hardware, seed and date — or cited with
   an arXiv id and section. **Never recalled.** This is the rule you are most likely to break.
5. **A paper the field rests on is taught, not cited** (Principle 21). It gets its own part, and
   that part contains **the smallest runnable project that implements the paper and nothing else**,
   with the A/B that switches its idea off. Naming a paper and moving on is the citation equivalent
   of an unexplained line of code.

---

## Step 1 — gather

1. Read the plan: **§2** (the twenty-one principles), **§4** (the compute tiers), **§6** (the five
   silent failures), **§24** (the day map — the authoritative ID list for day $ARGUMENTS, and
   **§24.3 the paper roster**), **§25** (the depth contract, and **§25.10 the paper-part
   contract**), **§28** (the style guide). Collect every ID slotted to day $ARGUMENTS, the
   phase theme, and the gate that phase feeds.
2. Read `docs/PROGRESS.md`. **Confirm $ARGUMENTS is exactly one more than the last row.** If it is
   not, say so and stop — do not generate out of order (plan §26: never skip, merge or reorder a day
   without an ADR).
3. Read `docs/TRACEABILITY.md`. Any open ID from a completed phase is a bug — report it, don't paper
   over it.
4. Read the previous day's `days/day-NNN-<slug>/LESSON.md` and `CHECKLIST.md`. If the checklist has
   unticked boxes, warn me and ask before proceeding. **Build on the code the previous days told the
   learner to write in `akshara/` — never duplicate it, never rewrite it.** By Day 39 there is a
   working model; by Day 67 there is a checkpoint. A day that re-derives what already exists has
   wasted the learner's typing.
5. Read the ledgers that bind this day: `docs/PACKAGES.md` for what is already pinned,
   `docs/DATASETS.md` and `docs/MODELS.md` for what is already downloaded, `docs/RUNS.md` for what
   has already been trained (a day that fine-tunes must know which checkpoint it starts from).

## Step 2 — verify reality before you write (Principles 6, 7, 8, 14)

6. **Never invent an API.** For every library symbol the day will use, read the live docs **for the
   version pinned in `pyproject.toml`** — or the source, which is more reliable. Note the URL or the
   file path and the date. The part that uses the symbol states what was checked. If the live docs
   disagree with the plan, **stop and propose an amendment** — do not silently adapt.
7. **Never invent a version.** For every package the day installs, read the version live
   (`curl -s https://pypi.org/pypi/<pkg>/json`, or `uv pip compile` for a resolved answer). Record
   package, version and date in `docs/PACKAGES.md`. If a lookup fails, leave a
   `TODO(<exact command>)` — never a guess.
8. **Never invent a number.** This is the one that matters most here.
   - A hyperparameter ("LoRA rank is usually 8–64"), a benchmark score, a model's parameter count, a
     paper's result, a "typical" loss value, a speedup factor — **none of these may be written from
     memory.**
   - Either **measure it** in the day (and the part says: hardware, seed, date), or **cite it**
     (arXiv id + section, and you fetched the abstract to confirm the claim), or leave
     `TODO(measure: <the exact command>)`.
   - If you catch yourself writing "typically", "usually", "around", or "on the order of" in front of
     a number, stop: that is a rumour with a hedge in front of it.
9. **Never invent a model or dataset.** Any day that downloads one resolves the **revision SHA**
   from the hub API, checks the licence on the card, confirms it is available in **safetensors**
   (Principle 13 — never a pickle), and writes the row in `docs/MODELS.md` / `docs/DATASETS.md`
   **before** the download step appears in the doc.
10. **Confirm the compute tier.** Decide whether the day is T0 (CPU), T1 (one free notebook GPU
    session) or contains T2 🅿️ material. If any step needs a GPU, **the day must also show what runs
    on CPU and say what the CPU version proves.** A day that silently requires hardware the learner
    may not have is a broken day.

## Step 3 — plan the split (do this before writing prose)

11. List the day's subtopics. Group them into **sections** that share one mental model — usually one
    section per curriculum ID, per forward-pass stage, or per phase of a mechanism. State the
    grouping; an unexplained numbering is a bug.
12. Split by **idea boundaries, never by length or pace** (§25.7). There is no target part count.
    Five parts if the subject needs five; twenty-four if it needs twenty-four.
    - `math` days: one definition → one derivation → one implementation → one failure of intuition
    - `build` days: mechanism → shapes → behaviour → edge case → failure mode → production use
    - `compare` 🔍 days: one dimension of difference per part
    - `run` days: config → launch → watch → interpret → what went wrong
    - `concept` days: one claim per part, each with its evidence
    - `gate` days: one acceptance criterion per part
13. **Every day gets at least one part whose subject is a deliberate failure** — usually at
    `production` level, where breaking the thing on purpose is the whole point of the document.
14. Assign each part a `level` — `foundation` (knows what it is), `working` (can implement it on
    their own problem), `production` (knows what changes in a real system, and can defend it with
    arithmetic). A day should climb. A day that is all `foundation` is a tutorial.
15. Apply the **one-idea test**, the **standalone test**, the **no-shortcut test** and the
    **provenance test** to each planned part *before* writing.
16. **Print the planned part list to me before writing.** If it looks thin, I will say so.

## Step 4 — write the parts (`days/day-NNN-<slug>/parts/<NN>-<slug>/<section>.<sub>-<slug>.md`)

> **Name the day folder `days/day-NNN-<slug>/`** — the number **zero-padded to three digits**
> (the plan runs to 161), then a kebab-case slug of 1–4 words taken from the hub's `title` with
> articles dropped: `days/day-030-scaled-dot-product/`. A number alone is an address, not an answer.
> The number stays the identity — `./m`, `depth_check.py`, `tracker.py` and `trace.py` all resolve a
> day by number and accept any slug — so a folder can be renamed to a better slug at any time.
> `./m depth` rejects a bare `days/day-030/` and rejects a two-digit `day-30-…`.

17. **One folder per section**, two zero-padded digits **then a kebab-case slug of 1–3 words saying
    what the section is about** — `parts/01-soft-lookup/`, `parts/03-causal-mask/`. Take the slug
    from the section's heading in the hub's §2 map. A bare `parts/01/` is rejected by `./m depth`.
    Every part lives inside its section's folder; none is ever loose in `parts/`, and the folder
    number must match the number before the dot in the filename.
18. One file per subtopic, named `<section>.<subtopic>-<kebab-slug>.md`. The slug says what the part
    *teaches*, never where it sits. Numbering starts at `1` and has no gaps.
19. **Links are relative to the part's own folder**: a sibling in the same section is
    `1.2-<slug>.md`; a part in another section is `../01-<slug>/1.5-<slug>.md`; the hub is
    `../../LESSON.md`. `prev` and `next` in the frontmatter use the same form. The hub's §2 map
    links the full path from the day folder: `parts/01-<slug>/1.1-<slug>.md`.
20. Every part carries all eleven sections of §25.4, **in this order** (two are conditional):
    - **frontmatter** — `day`, `part`, `title`, `ids`, `level`, `prerequisites`, `prev`, `next`.
      **No duration field of any kind.**
    - **One-line answer** — the claim in one sentence, before anything else.
    - **The story** — a concrete scene first: a person, a machine, a failure, a decision. **No
      jargon at all** in this section. This is the hook the definition hangs on.
    - **The idea in plain language** — the concept assuming zero prior knowledge; every term defined
      on first use, **including terms from earlier days**, with a link to the part that introduced
      them. No code.
    - **Why Akshara needs it** — the concrete later day that breaks without this. Never "this is
      important".
    - **The mechanism** — how it actually works: runnable code, the derivation written out, or the
      diagram. Nothing skipped as "obvious".
    - **Shapes** ⟵ *required whenever a tensor is introduced or transformed.* A table: tensor name ·
      symbolic shape `(B, T, C)` · the concrete numbers used in this part · **what each axis means**.
      Symbols are curriculum-wide: `B` batch · `T` sequence · `C` channels/`d_model` · `H` heads ·
      `hs` head size · `V` vocabulary. A new symbol must be defined where it is introduced. Omit the
      section only if the part genuinely has no tensors.
    - **Line by line** — a `**Line by line:**` list **immediately after each code block**: every
      non-obvious token, and *why that line and not another*. Omit only if the part has no code
      needing a walkthrough.
    - **When it breaks** — the **real** error text verbatim, what it means, the smallest fix. And
      for this field: **the silent version too** — what the wrong-but-running output looks like, and
      the check that catches it (§6).
    - **In production** — the real-system version: what a research engineer writes instead of the
      teaching version, what degrades at scale, the failure that only shows with real data, the
      review comment, and the interview question that finds out whether you have actually used it.
      **Not optional. This is the section that makes the document professional rather than
      introductory.**
    - **Check yourself** — one command to run now **that prints a number, not just a pass**, and one
      question to answer out loud.
21. Apply **Akshara's five additional part rules** (§25.4.1): name the doc page or source file
    checked for the pinned version · state the verified version or a `TODO` with the lookup command ·
    every number measured-here or cited · **name the silent failure** the part is avoiding and how
    the reader detects it · **state the compute tier** and what the T0 version proves.
22. Mermaid diagram whenever the concept is spatial, sequential, or a state machine — attention
    flow, the diffusion forward/reverse process, the RLHF pipeline, a request through a batching
    scheduler, the KV cache growing.
23. **Shape comments in every code block**: `x = tok_emb + pos_emb  # (B, T, C)` on every line that
    changes a shape. The `Shapes` table is the summary; the comments are the working.

## Step 4b — write the paper parts (Principle 21 · §25.10)

> Do this **after** the teaching parts exist. The mechanism is taught first, in plain language and
> running code, so that the reader opens the paper already understanding the idea and reads it for
> *how it was argued and what it cost*. A reader sent to the paper first learns to be intimidated by
> papers.

24. **Look the day up in the plan's §24.3 roster.** It lists the papers this day rests on, **by title
    and year only** — deliberately, because an arXiv id is a number and Principle 8 forbids writing
    one from memory. The roster is the **floor**: a day may add a paper it turns out to need (a
    `docs/PAPERS.md` row and a part, no amendment); removing one *is* an amendment.
    If §24.3 lists none, the hub gets `papers: []` and you skip to Step 5. **`papers: []` is an
    explicit statement that you checked**, and 74 of the 162 days legitimately have it.
25. **Resolve each identifier live and write `docs/PAPERS.md` first.** Fetch the arXiv abstract page
    (or the venue page where there is no arXiv id), confirm the exact title and year, and write the
    row — paper, year, identifier, day, part path, demo path, `taught`, the URL you fetched, and the
    date — **before** you write a word of the part.
26. **Read the actual paper.** A paper part written from an abstract, a blog summary or memory is
    worse than none: it launders unreliability through the appearance of a citation. Note which
    sections matter and which the reader can skip — you will say so in the part.
27. **One paper, one part**, in a dedicated section **last in the day**: `parts/NN-the-papers/`
    (or `NN-the-paper/` when there is one). Each part declares `kind: paper`, `paper_title`,
    `paper_year`, and `paper_arxiv` **or** `paper_venue`.
28. Each paper part carries the nine unconditional sections **plus three**, in this order —
    `The mechanism` → **`The paper in one small project`** → **`What the paper showed`** →
    `When it breaks` → **`What came after`** → `In production`:
    - **The story is the world before the paper** — what people were actually doing and what it cost
      them, told from inside the year it was written, with no hindsight and no jargon.
    - **The mechanism reads the equation symbol by symbol.** `Line by line`, applied to mathematics:
      an unexplained symbol is a bug in the doc. The `Shapes` table maps the paper's notation onto
      the curriculum's (`B`, `T`, `C`, `H`, `hs`, `V`).
    - **`The paper in one small project`** — see step 29, which is the hard one.
    - **`What the paper showed`** — the evidence, cited to its table or section (`Table 3`, `§5.2`),
      numbers **as reported**, then what the evidence does *and does not* support: the ablation not
      run, the baseline not tuned, the single seed. **Compare your demo's number to theirs here**,
      out loud, including why they differ.
    - **`What came after`** — corrections, superseding work, failed reproductions, what the community
      quietly stopped doing. A paper taught as the final word is taught wrong.
    - **`Check yourself` must send the reader into the paper**: *"read §3.2.1 and say out loud what
      breaks if the scaling is removed."* They open the PDF at least once per paper part.
29. **Write the small project.** This is the section that makes a paper part worth reading, and it is
    the hardest thing in this skill to get right.
    - **The smallest end-to-end runnable project that implements the paper's contribution and
      nothing else.** Not a snippet — a project: starts from nothing, runs with one command, prints
      a result. No surrounding model, no other features, no scaffolding the paper did not introduce.
    - **The isolation is the pedagogy.** Stripping an idea to the smallest thing that still
      demonstrates it is the proof you understood what the paper actually added. **If you cannot
      isolate it, you have not understood it** — that is a signal to re-read, never a signal to
      write a bigger demo. The one genuine exception is a paper whose contribution *is* a
      system-level property (continuous batching, FSDP): there the project simulates the mechanism —
      a queue of fake requests, a fake device mesh — and says so plainly.
    - **T0 only.** Laptop CPU, seconds to a couple of minutes, synthetic or tiny data. A paper part
      the learner cannot run is a paper part they will not run.
    - **The A/B is mandatory.** The same project with the paper's idea switched off, printed side by
      side. A demo that only shows *it runs* demonstrates nothing — **the ablation is the demo.**
    - **State what it does not show.** A 500-step run on synthetic data reproduces the *mechanism*
      and the *direction* of the effect, never the paper. Say which, in words. **A demo presented as
      a reproduction is Silent Failure #4 wearing a lab coat.**
    - It lives at `days/day-NNN-<slug>/papers/<paper-slug>/` — the day's own `papers/` directory,
      a **sibling of `lab/`, never inside it**. `lab/` is the learner's scratch space; `papers/`
      holds finished demonstrations a part references and anyone can run. Each holds `demo.py` plus
      a `README.md` saying what it shows and what it does not. It is printed in full in the part and
      carries its `Line by line` and, if it touches tensors, its `Shapes`.
    - **A parked 🅿️ paper still gets its small project.** 🅿️ means "not built into Akshara", never
      "not built at all": you can build a fifty-line selective scan on a toy sequence without
      building a Mamba.
30. **Label every number**: `[reported: Table 3]` versus `[measured here: CPU, seed 1337,
    2026-08-25]`. Mixing the two is how a curriculum starts lying to itself.

## Step 5 — write the hub (`days/day-NNN-<slug>/LESSON.md`)

31. The hub orients and assembles; **it never teaches**. No `Line by line:` and no `Shapes` table in
    the hub. Required sections, in order (§25.5):
    - YAML frontmatter (`day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
      `plan_version: "v1.1.0"`, `parts`, `papers` (the list from §24.3 — **`papers: []` when the
      day rests on none**), `compute_tier`, `generated`, `status`, `lab_scaffolded`, `commit`)
    - a **yesterday / today / tomorrow** blockquote — no time estimate
    - `## §1 Where we are` — a scene and an analogy, plain language, NO code, NO jargon
    - `## §2 The map` — a table of every part: number, linked title
      (`parts/01-<slug>/1.1-<slug>.md`), what it answers, `level`, grouped by section with one line
      saying what each *section* means. **The paper section is listed like any other.**
      **No minutes column, ever.**
    - `## §3 Setup — run this` — every `mkdir`, `touch`, `uv add` the day needs, pinned; plus the
      notebook link if the day is T1
    - `## §4 Build brief` — files to create, with `TODO(me)` markers left unsolved
    - `## §5 The eval that must be able to fail` — the check that is RED before the TODOs are done
    - `## §6 Compute budget` — the tier (T0/T1/T2); for T1, GPU-minutes and session count. `0` is an
      answer; state it.
    - `## §7 Traps` — the mistakes that eat an evening, including the named Silent Failure (§6)
    - `## §8 Verify before you code` — the live URLs actually fetched, **every paper's arXiv page
      with the date you opened it**, the model/dataset cards read. Never from memory.
    - `## §9 Say it in an interview` — one paragraph, spoken voice, tied to a number you measured
    - `## §10 Done when` — pointer to `CHECKLIST.md`, defined by understanding and green checks
    - `## §11 Ledger & commit` — the verbatim `PROGRESS.md` row, any `PACKAGES.md`, `DATASETS.md`,
      `MODELS.md`, `RUNS.md` and `PAPERS.md` rows, and the commit message
      `day NNN: <title> — closes <IDs>`. **The hub ends here.**

## Step 6 — the checklist (`days/day-NNN-<slug>/CHECKLIST.md`)

32. Demo command, setup boxes, **one box per part document** (read it, run its check-yourself,
    answer its out-loud question), build-brief boxes, a test box per test **including at least one
    "break it, watch it go red, fix it"**, the compute budget, the ledger rows pasted, and the commit
    box. No time estimates.
33. **On any day with papers, the checklist must include, per paper:**
    - [ ] Opened the actual paper — not an abstract, not a summary — and the `docs/PAPERS.md` row
          records the URL and the date it was opened
    - [ ] Typed and ran the small project; can state the number it printed
    - [ ] Ran the **A/B** and watched the paper's effect appear and disappear
    - [ ] Can say what the demo does **not** show, and why the paper's number differs from yours
    - [ ] Read the section named in *Check yourself* and answered its question out loud

34. **On any day that trains something, the checklist must include:**
    - [ ] Overfit one batch first — loss reached ~0 on 16 examples before the real run (P12)
    - [ ] The `docs/RUNS.md` row is written: seed, config hash, hardware, steps, final loss, outcome
    - [ ] Which of the five silent failures (§6) this run could have hit, and how you ruled it out

## Step 7 — verify

35. Run `./m depth $ARGUMENTS`. **Fix every failure; never hand-wave past one.**
36. Run `./m trace` — the day's IDs must match §24 exactly, no more and no fewer.
37. Run `./m tracker`.
38. Finish by printing: today's IDs, the part count, the demo command, the compute tier and budget,
    and the doc URLs / arXiv ids you actually fetched.

---

## Always

- Honor `CLAUDE.md`: exact pins · doc-first · **build first, compare after** · read-only by default ·
  at least one check that can go red · CPU-first code · seeds everywhere.
- Do **not** solve the `TODO(me)` sections, and do **not** write project code. The learner types
  every line of `akshara/`. Teach; don't do the reps.
- **Do not commit weights, checkpoints or datasets**, and do not write a day that tells the learner
  to (Principle 9).
- Never name a person, instructor, author, channel, academy, bootcamp or training company anywhere
  in the output. The plan is self-contained and cites no external course; do not invent a lineage
  for it. Tool and library names are required and fine; **citing a paper by arXiv id and title is
  required** — that is provenance, not a brand.
- The failures this format exists to prevent (§25.8): splitting without deepening · summary in place
  of explanation · **stopping at the toy example** · assuming the previous day · code without
  failure · **numbers without provenance** · **shapes left to the reader** · **trimming to fit** ·
  solved reps. If a part has no story, no shapes, no failure text and no production section, it is
  not done.

## The self-check before you say a day is finished

Answer these out loud. If any answer is no, the day is not written.

1. Could a reader who has never heard of today's topic start at part 1.1 and stand up?
2. Does every part end somewhere a professional would recognise — scale, memory, review, interview?
3. Does every number in the day have a provenance line next to it?
4. Does every tensor in the day have a shape, in code *and* in a table?
5. Is there a part whose whole subject is something breaking?
6. Does the day name which of the five silent failures it touches, and how to detect it?
7. Does every step run on a laptop, or does the day say explicitly what needs a GPU and what the CPU
   version proves?
8. Does every paper the day rests on have its own part — with a small project that runs on a CPU,
   an A/B that switches the paper's idea off, and an honest note about what it does not show?
9. Is every number in a paper part labelled `[reported: …]` or `[measured here: …]`?
10. Did `./m depth $ARGUMENTS` pass without you arguing with it?
