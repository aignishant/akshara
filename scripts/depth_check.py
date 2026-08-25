"""The machine-readable half of the depth contract (master plan §25).

Run as `./m depth [N]`. Checks every written day, or one day, against the structural rules
of plan §25. What it cannot check is whether an explanation is any good — that is §25.8, and
it is reviewed by reading.

Exit code 0 = green, 1 = at least one failure.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAYS = ROOT / "days"

# --- the contract (§25.4) ------------------------------------------------------------------

#: H2 headings every part carries, in this order. Frontmatter is checked separately and is
#: the ninth unconditional section.
REQUIRED_SECTIONS: tuple[str, ...] = (
    "One-line answer",
    "The story",
    "The idea in plain language",
    "Why Akshara needs it",
    "The mechanism",
    "When it breaks",
    "In production",
    "Check yourself",
)

#: Conditional sections. `Shapes` is required when the part introduces or transforms a tensor
#: (§25.4, Principle 20) and sits between `The mechanism` and `When it breaks`.
SHAPES_SECTION = "Shapes"
SHAPES_AFTER = "The mechanism"
SHAPES_BEFORE = "When it breaks"

#: A `kind: paper` part carries two more unconditional sections (§25.10.2, Principle 21).
#: `What the paper showed` sits before `When it breaks`; `What came after` sits between
#: `When it breaks` and `In production`.
PAPER_SECTIONS: tuple[tuple[str, str, str], ...] = (
    # (section, must come after, must come before)
    ("The paper in one small project", "The mechanism", "What the paper showed"),
    ("What the paper showed", "The mechanism", "When it breaks"),
    ("What came after", "When it breaks", "In production"),
)

#: The small project must actually be a project (§25.10.2 section 9). A section with no code block
#: in it is a description of a demo, which is what this rule exists to prevent.
PAPER_PROJECT_SECTION = "The paper in one small project"
PAPER_FRONTMATTER = ("paper_title", "paper_year")
PAPER_IDENTIFIERS = ("paper_arxiv", "paper_venue")

LEVELS = frozenset({"foundation", "working", "production"})

#: Reader-directed pace and duration phrasing (§25.9, Principle 17).
#:
#: NOT banned: measured wall-clock ("the run took 43 min on a T4"), GPU-minutes in a compute
#: budget, latency figures, tokens/s. Those are data (Principle 8), not a clock telling the
#: reader how fast to go. The ban is on estimates aimed at the reader's schedule.
CLOCK_PATTERNS: tuple[tuple[str, str], ...] = (
    # An estimate has a value. Requiring a colon, an equals or a digit distinguishes a real
    # field ("estimated_hours: 2") from prose that discusses the ban ("an estimated-time field
    # authorises the trim"). Without this narrowing, §25 could not describe its own rule.
    (r"estimated[ _-]?(hours|time|duration)\s*[:=]", "an estimated-time field"),
    (r"estimated[ _-]?(hours|time|duration)\s+(of\s+)?~?\d", "an estimated-time value"),
    (r"time[ _-]estimate\s*[:=]", "a time-estimate field"),
    (r"^\s*(duration|time_required|est_hours|hours)\s*:", "a duration field in frontmatter"),
    (
        r"(should|will|might|may|can)\s+take\s+(you\s+)?(about\s+|around\s+|~\s*)?\d",
        "a 'should take N' estimate",
    ),
    (
        r"(takes|lasts)\s+(about|around|roughly|~)\s*\d+\s*(min|hour|hr|day|week)",
        "a 'takes about N' estimate",
    ),
    (
        r"\ballow\s+(about\s+|around\s+)?\d+\s*(minutes|mins|hours|hrs)\b",
        "an 'allow N minutes' estimate",
    ),
    (
        r"\bin\s+(just\s+)?(under\s+)?\d+\s*(minutes|mins|hours|hrs)\s+you('ll| will| can)",
        "a reader-directed pace",
    ),
    (r"\b(a\s+)?(quick|short|brief)\s+(detour|aside|note|read|section|day)\b", "a pace adjective"),
    (r"\bat\s+(a\s+)?(comfortable|steady|brisk)\s+pace\b", "a suggested pace"),
    (r"\bsuggested\s+pace\b", "a suggested pace"),
    (r"\bper\s+(day|week)\s+pace\b", "a suggested pace"),
)

#: A code block is exempt from needing a `**Line by line:**` walkthrough when it is a diagram,
#: pure output, or a bare command (§25.4 / §28.3 rule 7).
EXEMPT_LANGS = frozenset(
    {"mermaid", "text", "txt", "", "output", "console", "traceback", "diff", "json5"}
)

#: Signals that a code block is doing tensor work, which makes `## Shapes` mandatory.
TENSOR_SIGNALS = re.compile(
    r"""(
      \#\s*\(\s*B\s*,          # a shape comment like  # (B, T, C)
    # (?<!\\) — a backslash before the dot means this is regex *source* being quoted
    # (r"\.shape\b"), not an attribute access. Narrowed after a real false positive on the
    # very part that documents these patterns. See part 5.2 on owning your false positives.
    | (?<!\\)\.shape\b
    | (?<!\\)\.view\(
    | (?<!\\)\.reshape\(
    | (?<!\\)\.permute\(
    | (?<!\\)\.transpose\(
    | (?<!\\)\.unsqueeze\(
    | (?<!\\)\.squeeze\(
    | torch\.(zeros|ones|randn|arange|cat|stack|einsum|matmul|tril|triu)\(
    | np\.(zeros|ones|random\.randn|arange|concatenate|stack|einsum|matmul)\(
    | @\s*(w|W|k|q|v|K|Q|V)\b   # an explicit matmul against a weight/projection
    )""",
    re.VERBOSE,
)

CODE_BLOCK = re.compile(r"^```([A-Za-z0-9_+-]*)\s*$", re.MULTILINE)

PART_FILENAME = re.compile(r"^(\d+)\.(\d+)-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
SECTION_DIRNAME = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
DAY_DIRNAME = re.compile(r"^day-(\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")


@dataclass
class Report:
    """Collected failures for one `./m depth` invocation."""

    failures: list[str] = field(default_factory=list)
    days_checked: int = 0
    parts_checked: int = 0
    paper_parts_checked: int = 0

    def fail(self, where: Path | str, message: str) -> None:
        rel = where.relative_to(ROOT) if isinstance(where, Path) else where
        self.failures.append(f"{rel}: {message}")


# --- helpers -------------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). Frontmatter is '' when the file has none."""
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def frontmatter_value(fm: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}\s*:\s*(.*)$", fm, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip("\"'")


def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks so prose checks don't fire on code."""
    return re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)


def iter_code_blocks(body: str) -> list[tuple[str, int, int]]:
    """Yield (lang, start_index, end_index_of_closing_fence) for each fenced block."""
    blocks: list[tuple[str, int, int]] = []
    fences = list(CODE_BLOCK.finditer(body))
    i = 0
    while i + 1 < len(fences):
        opening, closing = fences[i], fences[i + 1]
        blocks.append((opening.group(1).lower(), opening.end(), closing.start()))
        i += 2
    return blocks


def section_body(body: str, heading: str) -> str:
    """Return the text under one H2 heading, up to the next H2 (or end of file)."""
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$", body, re.MULTILINE)
    if not m:
        return ""
    nxt = re.search(r"^##\s+", body[m.end() :], re.MULTILINE)
    return body[m.end() : m.end() + nxt.start()] if nxt else body[m.end() :]


def section_has_code(body: str, heading: str) -> bool:
    return "```" in section_body(body, heading)


def h2_headings(body: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*$", body, re.MULTILINE)]


def blank_quoted(text: str) -> str:
    """Blank out fenced blocks and inline code, preserving line numbers.

    Clock rules (Principle 17) are about prose aimed at the reader. A part that *teaches* the
    rule must be able to quote it — the checker's own patterns, a console transcript of it
    firing — and a document forced to mangle its examples to satisfy the checker would be a
    document optimised for the linter, which is the failure part 5.2 warns about. Newlines are
    preserved so failure messages still point at the right line.
    """

    def _blank(m: re.Match[str]) -> str:
        return "\n" * m.group(0).count("\n")

    text = re.sub(r"^```.*?^```", _blank, text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def check_clocks(path: Path, text: str, rep: Report) -> None:
    """Principle 17 — no reader-directed time estimate anywhere in a day folder."""
    prose = blank_quoted(text)
    for pattern, description in CLOCK_PATTERNS:
        m = re.search(pattern, prose, re.IGNORECASE | re.MULTILINE)
        if m:
            line = prose[: m.start()].count("\n") + 1
            rep.fail(path, f"line {line}: {description} — {m.group(0)!r} (Principle 17)")


# --- part checks ---------------------------------------------------------------------------


def frontmatter_list(fm: str, key: str) -> list[str] | None:
    """Read a YAML list in either inline (`k: ["a", "b"]`) or block (`k:\\n  - a`) form.

    Returns None when the key is absent, [] when it is present and empty. That distinction is
    the point for `papers:` — an empty list is a decision, a missing key is an oversight (§25.5).
    """
    m = re.search(rf"^{re.escape(key)}\s*:\s*(.*)$", fm, re.MULTILINE)
    if not m:
        return None
    inline = m.group(1).strip()
    if inline.startswith("["):
        return re.findall(r"['\"]([^'\"]+)['\"]", inline) or (
            [] if inline.replace(" ", "") == "[]" else [inline]
        )
    if inline:
        return [inline.strip("\"'")]
    items: list[str] = []
    for line in fm[m.end() :].splitlines():
        if re.match(r"^\s*-\s+", line):
            items.append(re.sub(r"^\s*-\s+", "", line).strip().strip("\"'"))
        elif line.strip() and not line.startswith((" ", "\t")):
            break
    return items


def check_part(path: Path, section_no: int, rep: Report) -> bool:
    """Check one part. Returns True when it is a `kind: paper` part."""
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    rep.parts_checked += 1

    check_clocks(path, text, rep)

    if not fm:
        rep.fail(path, "no YAML frontmatter (§25.4 section 1)")
        return False

    is_paper = (frontmatter_value(fm, "kind") or "").lower() == "paper"

    for key in ("day", "part", "title", "ids", "level", "prerequisites", "prev", "next"):
        if frontmatter_value(fm, key) is None:
            rep.fail(path, f"frontmatter is missing `{key}` (§25.4 section 1)")

    level = frontmatter_value(fm, "level")
    if level is not None and level not in LEVELS:
        rep.fail(path, f"level {level!r} is not one of {sorted(LEVELS)} (§25.6)")

    part_no = frontmatter_value(fm, "part")
    expected = f"{section_no}."
    if part_no is not None and not part_no.startswith(expected):
        rep.fail(
            path, f"frontmatter part {part_no!r} does not start with section {section_no} (§25.2)"
        )

    # --- required H2 sections, in contract order
    headings = h2_headings(body)
    present = [h for h in headings if h in REQUIRED_SECTIONS]
    missing = [s for s in REQUIRED_SECTIONS if s not in headings]
    if missing:
        rep.fail(path, f"missing required section(s): {', '.join(missing)} (§25.4)")
    if present != [s for s in REQUIRED_SECTIONS if s in present]:
        rep.fail(path, f"sections are out of contract order: {present} (§25.4)")

    # --- code blocks need a walkthrough
    blocks = iter_code_blocks(body)
    needs_shapes = False
    for lang, start, end in blocks:
        code = body[start:end]
        if TENSOR_SIGNALS.search(code):
            needs_shapes = True
        if lang in EXEMPT_LANGS:
            continue
        following = body[end : end + 600]
        if "**Line by line:**" not in following:
            line = body[:start].count("\n") + 1
            rep.fail(
                path,
                f"line ~{line}: a `{lang}` code block is not followed by `**Line by line:**` "
                "(§25.4 section 8 — an unexplained line is a bug in the doc)",
            )

    # --- Shapes is mandatory when tensors are involved (Principle 20)
    if needs_shapes and SHAPES_SECTION not in headings:
        rep.fail(
            path,
            f"code transforms tensors but there is no `## {SHAPES_SECTION}` section "
            "(§25.4 section 7 · Principle 20)",
        )
    order = {h: i for i, h in enumerate(headings)}
    if SHAPES_SECTION in headings:
        if SHAPES_AFTER in order and order[SHAPES_SECTION] < order[SHAPES_AFTER]:
            rep.fail(path, f"`## {SHAPES_SECTION}` must come after `## {SHAPES_AFTER}` (§25.4)")
        if SHAPES_BEFORE in order and order[SHAPES_SECTION] > order[SHAPES_BEFORE]:
            rep.fail(path, f"`## {SHAPES_SECTION}` must come before `## {SHAPES_BEFORE}` (§25.4)")

    # --- a paper part carries two more unconditional sections (§25.10.2, Principle 21)
    if is_paper:
        for key in PAPER_FRONTMATTER:
            if frontmatter_value(fm, key) is None:
                rep.fail(path, f"a `kind: paper` part must declare `{key}` (§25.10.2)")
        if not any(frontmatter_value(fm, k) for k in PAPER_IDENTIFIERS):
            rep.fail(
                path,
                "a `kind: paper` part must declare `paper_arxiv` or `paper_venue` — resolved live, "
                "never from memory (§25.10.3 rule 2 · Principle 8)",
            )
        for section, after, before in PAPER_SECTIONS:
            if section not in headings:
                rep.fail(path, f"a `kind: paper` part is missing `## {section}` (§25.10.2)")
                continue
            if after in order and order[section] < order[after]:
                rep.fail(path, f"`## {section}` must come after `## {after}` (§25.10.2)")
            if before in order and order[section] > order[before]:
                rep.fail(path, f"`## {section}` must come before `## {before}` (§25.10.2)")

        if PAPER_PROJECT_SECTION in headings and not section_has_code(body, PAPER_PROJECT_SECTION):
            rep.fail(
                path,
                f"`## {PAPER_PROJECT_SECTION}` contains no code block — a project you cannot run is "
                "a description (§25.10.2 section 9)",
            )
    else:
        for section, _, _ in PAPER_SECTIONS:
            if section in headings:
                rep.fail(
                    path,
                    f"carries `## {section}` but is not declared `kind: paper` in its frontmatter "
                    "(§25.10.2)",
                )

    return is_paper


# --- hub checks ----------------------------------------------------------------------------


def check_hub(hub: Path, part_paths: list[str], paper_parts: int, rep: Report) -> None:
    text = hub.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)

    check_clocks(hub, text, rep)

    if not fm:
        rep.fail(hub, "no YAML frontmatter (§25.5)")
        return

    for key in (
        "day",
        "phase",
        "phase_name",
        "title",
        "ids",
        "principles",
        "kind",
        "plan_version",
        "parts",
        "compute_tier",
        "generated",
        "status",
    ):
        if frontmatter_value(fm, key) is None:
            rep.fail(hub, f"frontmatter is missing `{key}` (§25.5)")

    declared = frontmatter_value(fm, "parts")
    if declared is not None and declared.isdigit() and int(declared) != len(part_paths):
        rep.fail(
            hub,
            f"frontmatter says parts: {declared} but {len(part_paths)} part file(s) are on disk (§25.9)",
        )

    # `papers:` is required, and `papers: []` is the answer when a day rests on none — an empty
    # list is a decision, a missing key is an oversight (§25.5 · Principle 21).
    papers = frontmatter_list(fm, "papers")
    if papers is None:
        rep.fail(
            hub,
            "frontmatter is missing `papers` — use `papers: []` when the day rests on none. "
            "An empty list is a decision; a missing key is an oversight (§25.5 · Principle 21)",
        )
    elif len(papers) != paper_parts:
        rep.fail(
            hub,
            f"frontmatter declares {len(papers)} paper(s) but {paper_parts} `kind: paper` part(s) "
            "are on disk — one paper, one part (§25.10.3 rule 1)",
        )

    for n in range(1, 12):
        if not re.search(rf"^##\s*§{n}\s+", body, re.MULTILINE):
            rep.fail(hub, f"missing hub section `## §{n}` (§25.5)")

    # The hub never teaches (§25.5).
    if "**Line by line:**" in body:
        rep.fail(
            hub,
            "the hub carries a `**Line by line:**` walkthrough — that belongs in a part (§25.5)",
        )
    if re.search(r"^##\s+Shapes\s*$", body, re.MULTILINE):
        rep.fail(hub, "the hub carries a `## Shapes` table — that belongs in a part (§25.5)")

    # §2 The map must link every part on disk.
    for rel in part_paths:
        if rel not in body:
            rep.fail(hub, f"the §2 map does not link `{rel}` (§25.9)")


# --- day checks ----------------------------------------------------------------------------


def check_day(day_dir: Path, rep: Report) -> None:
    rep.days_checked += 1

    if not DAY_DIRNAME.match(day_dir.name):
        rep.fail(
            day_dir,
            "day folder must be `day-NNN-<slug>` with a three-digit number and a kebab-case slug (§25.2)",
        )

    hub = day_dir / "LESSON.md"
    checklist = day_dir / "CHECKLIST.md"
    parts_dir = day_dir / "parts"

    if not hub.exists():
        rep.fail(day_dir, "no LESSON.md — the day has no hub (§25.2)")
    if not checklist.exists():
        rep.fail(day_dir, "no CHECKLIST.md (§25.9)")
    else:
        check_clocks(checklist, checklist.read_text(encoding="utf-8"), rep)

    if not parts_dir.is_dir():
        rep.fail(day_dir, "no parts/ directory — by definition this day is not written (§25.2)")
        return

    for loose in sorted(parts_dir.glob("*.md")):
        rep.fail(loose, "a part is loose in parts/ instead of inside a section folder (§25.2)")

    section_dirs = sorted(p for p in parts_dir.iterdir() if p.is_dir())
    if not section_dirs:
        rep.fail(parts_dir, "parts/ contains no section folders (§25.2)")
        return

    seen_sections: list[int] = []
    part_rel_paths: list[str] = []
    paper_parts = 0

    for sec in section_dirs:
        m = SECTION_DIRNAME.match(sec.name)
        if not m:
            rep.fail(
                sec,
                "section folder must be `NN-<slug>`, two zero-padded digits then a slug (§25.2)",
            )
            continue
        sec_no = int(m.group(1))
        seen_sections.append(sec_no)

        files = sorted(sec.glob("*.md"))
        if not files:
            rep.fail(sec, "section folder contains no part documents (§25.2)")
            continue

        subtopics: list[int] = []
        for f in files:
            fm_ = PART_FILENAME.match(f.name)
            if not fm_:
                rep.fail(f, "filename must be `<section>.<subtopic>-<kebab-slug>.md` (§25.9)")
                continue
            file_sec, file_sub = int(fm_.group(1)), int(fm_.group(2))
            if file_sec != sec_no:
                rep.fail(
                    f,
                    f"lives in section folder {sec_no:02d} but its filename says section {file_sec} (§25.2)",
                )
                continue
            subtopics.append(file_sub)
            part_rel_paths.append(f"parts/{sec.name}/{f.name}")
            if check_part(f, sec_no, rep):
                paper_parts += 1
                rep.paper_parts_checked += 1

        subtopics.sort()
        if subtopics and subtopics != list(range(1, len(subtopics) + 1)):
            rep.fail(
                sec, f"subtopic numbering must start at 1 with no gaps, got {subtopics} (§25.3)"
            )

    seen_sections.sort()
    if seen_sections and seen_sections != list(range(1, len(seen_sections) + 1)):
        rep.fail(
            parts_dir,
            f"section numbering must start at 1 with no gaps, got {seen_sections} (§25.3)",
        )

    if hub.exists():
        check_hub(hub, part_rel_paths, paper_parts, rep)


# --- entry point ---------------------------------------------------------------------------


def day_dirs(only: int | None) -> list[Path]:
    if not DAYS.is_dir():
        return []
    found = []
    for p in sorted(DAYS.iterdir()):
        if not p.is_dir():
            continue
        m = re.match(r"^day-(\d+)", p.name)
        if not m:
            continue
        if only is None or int(m.group(1)) == only:
            found.append(p)
    return found


def main(argv: list[str]) -> int:
    only: int | None = None
    if len(argv) > 1:
        try:
            only = int(argv[1])
        except ValueError:
            print(f"usage: depth_check.py [day-number]  (got {argv[1]!r})")
            return 2

    dirs = day_dirs(only)
    if only is not None and not dirs:
        print(f"depth: no day {only} on disk")
        return 1
    if not dirs:
        print("depth: no days written yet — nothing to check")
        return 0

    rep = Report()
    for d in dirs:
        check_day(d, rep)

    if rep.failures:
        print(f"depth: FAIL — {len(rep.failures)} problem(s) across {rep.days_checked} day(s)\n")
        for f in rep.failures:
            print(f"  {f}")
        print("\nPlan §25 is the contract. Never hand-wave past a depth failure.")
        return 1

    print(
        f"depth: OK — {rep.days_checked} day(s), {rep.parts_checked} part(s), "
        f"{rep.paper_parts_checked} paper part(s), contract green"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
