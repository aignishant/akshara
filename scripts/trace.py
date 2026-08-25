"""ID-level traceability: the day map (plan §24) vs what the day hubs actually claim.

Run as `./m trace`. Reads §24 out of the master plan, reads the `ids:` frontmatter of every
written day hub, and regenerates two ledgers:

  docs/TRACEABILITY.md    — every ID, its planned day, and whether that day is written
  docs/CURRICULUM_INDEX.md — the reverse lookup: "where do I learn ARCH-28?"

An open ID in a completed phase is a bug (plan §26). Exit code 0 = green, 1 = problems.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "docs" / "00_MASTER_PLAN.md"
DAYS = ROOT / "days"
TRACEABILITY = ROOT / "docs" / "TRACEABILITY.md"
INDEX = ROOT / "docs" / "CURRICULUM_INDEX.md"

PREFIXES = (
    "MATH",
    "TOK",
    "EMB",
    "ARCH",
    "TRAIN",
    "SCALE",
    "INFER",
    "EFF",
    "POST",
    "REASON",
    "RAG",
    "EVAL",
    "MM",
    "GEN",
    "SAFE",
    "SERVE",
    "OPS",
)

CURRICULUM_NAMES = {
    "MATH": "Foundations",
    "TOK": "Tokenization",
    "EMB": "Representation",
    "ARCH": "Architecture",
    "TRAIN": "Training",
    "SCALE": "Scaling",
    "INFER": "Inference",
    "EFF": "Efficiency",
    "POST": "Post-training",
    "REASON": "Reasoning",
    "RAG": "Retrieval",
    "EVAL": "Evaluation",
    "MM": "Multimodal",
    "GEN": "Generative families",
    "SAFE": "Safety",
    "SERVE": "Serving",
    "OPS": "Operations",
}

ID_RE = re.compile(r"\b((?:" + "|".join(PREFIXES) + r")-\d{2})\b")
MAP_ROW = re.compile(r"^\|\s*(\d{1,3})\s*\|(.+?)\|\s*(.+?)\s*\|\s*$")


def parse_plan() -> tuple[dict[int, list[str]], dict[int, str]]:
    """Return (day -> [ids], day -> title) read from plan §24."""
    text = PLAN.read_text(encoding="utf-8")
    # Slice §24.2 exactly, not all of §24. §24.1 (phases) and §24.3 (the paper roster) are also
    # tables keyed by a day number, and parsing them as day-map rows silently clobbers real ID
    # assignments with empty lists.
    start = text.index("### 24.2 The map")
    end = text.index("### 24.3 The Paper Roster")
    body = text[start:end]

    day_ids: dict[int, list[str]] = {}
    day_title: dict[int, str] = {}
    for line in body.splitlines():
        m = MAP_ROW.match(line)
        if not m:
            continue
        day = int(m.group(1))
        title = m.group(2).strip()
        ids_cell = m.group(3).strip()
        # Skip the §24.1 phase-summary table, whose second column is a day *range* rather than a
        # title. Test for that shape exactly: a title cell that is only digits and a dash. Do NOT
        # test for a dash anywhere in the cell — real day titles contain en-dashes in compound
        # words ("Encoder–decoder", "Vision–language"), and that heuristic silently drops them.
        if re.fullmatch(r"\*{0,2}\d{1,3}(\s*[–-]\s*\d{1,3})?\*{0,2}", title):
            continue
        day_title[day] = title
        day_ids[day] = [] if ids_cell in {"—", "-", ""} else ID_RE.findall(ids_cell)
    return day_ids, day_title


def parse_phases() -> list[tuple[int, int, int, str]]:
    """Return [(phase, first_day, last_day, theme)] from the plan's §24.1 table."""
    text = PLAN.read_text(encoding="utf-8")
    start = text.index("### 24.1 The 22 phases")
    end = text.index("### 24.2 The map")
    phases: list[tuple[int, int, int, str]] = []
    for line in text[start:end].splitlines():
        m = re.match(
            r"^\|\s*\*{0,2}(\d+)\*{0,2}\s*\|\s*\*{0,2}([\d–-]+)\*{0,2}\s*\|\s*(.+?)\s*\|", line
        )
        if not m:
            continue
        phase = int(m.group(1))
        span = m.group(2).replace("–", "-")
        first, _, last = span.partition("-")
        phases.append((phase, int(first), int(last or first), m.group(3).strip("* ")))
    return phases


def written_days() -> dict[int, tuple[Path, list[str]]]:
    """Return day -> (hub path, ids claimed in its frontmatter) for every day on disk."""
    out: dict[int, tuple[Path, list[str]]] = {}
    if not DAYS.is_dir():
        return out
    for d in sorted(DAYS.iterdir()):
        m = re.match(r"^day-(\d+)", d.name)
        if not d.is_dir() or not m:
            continue
        hub = d / "LESSON.md"
        if not hub.exists():
            continue
        text = hub.read_text(encoding="utf-8")
        fm = text[4 : text.find("\n---\n", 4)] if text.startswith("---\n") else ""
        ids_line = re.search(r"^ids\s*:\s*(.*)$", fm, re.MULTILINE)
        claimed = ID_RE.findall(ids_line.group(1)) if ids_line else []
        out[int(m.group(1))] = (hub, claimed)
    return out


def day_link(day: int) -> str:
    for d in sorted(DAYS.iterdir()) if DAYS.is_dir() else []:
        if d.is_dir() and re.match(rf"^day-0*{day}(-|$)", d.name):
            return f"[{day}](../days/{d.name}/LESSON.md)"
    return str(day)


def main() -> int:
    day_ids, day_title = parse_plan()
    phases = parse_phases()
    on_disk = written_days()

    planned: dict[str, int] = {}
    problems: list[str] = []

    dupes = Counter(i for ids in day_ids.values() for i in ids)
    for i, c in dupes.items():
        if c > 1:
            problems.append(f"plan §24 assigns {i} to {c} days — an ID belongs to exactly one day")
    for day, ids in day_ids.items():
        for i in ids:
            planned[i] = day

    # A written day must claim exactly the IDs §24 gives it (plan §26, no more no fewer).
    for day, (hub, claimed) in sorted(on_disk.items()):
        expected = set(day_ids.get(day, []))
        got = set(claimed)
        rel = hub.relative_to(ROOT)
        for extra in sorted(got - expected):
            problems.append(f"{rel}: claims {extra}, which plan §24 does not assign to day {day}")
        for missing in sorted(expected - got):
            problems.append(
                f"{rel}: plan §24 assigns {missing} to day {day} but the hub does not claim it"
            )

    closed = {i for day, (_, claimed) in on_disk.items() for i in claimed if planned.get(i) == day}

    # Phase-level check: an open ID in a phase whose days are all written is a bug.
    for phase, first, last, theme in phases:
        phase_days = [d for d in range(first, last + 1)]
        if not all(d in on_disk for d in phase_days):
            continue
        open_ids = [i for d in phase_days for i in day_ids.get(d, []) if i not in closed]
        if open_ids:
            problems.append(
                f"phase {phase} ({theme}) is fully written but leaves open: {', '.join(open_ids)}"
            )

    total = len(planned)
    today = date.today().isoformat()

    # --- TRACEABILITY.md
    lines = [
        "# 🧵 Traceability — Project Akshara",
        "",
        f"_Generated {today} by `scripts/trace.py` from the master plan's §24 and the day hubs._",
        "**Do not edit by hand** — the next `./m check` overwrites it.",
        "",
        f"**{len(closed)} / {total} IDs closed** across {len(on_disk)} written day(s) of {len(day_ids)} planned.",
        "",
        "An ID is *closed* when the day the plan assigns it exists on disk and its hub claims it.",
        "**An open ID in a fully written phase is a bug** (plan §26).",
        "",
    ]
    if problems:
        lines += ["## ⚠️ Problems", ""]
        lines += [f"- {p}" for p in problems]
        lines += [""]
    else:
        lines += [
            "## ✅ No problems",
            "",
            "Every written day claims exactly the IDs §24 assigns it.",
            "",
        ]

    lines += [
        "## By phase",
        "",
        "| Phase | Days | Theme | Written | IDs closed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for phase, first, last, theme in phases:
        span = list(range(first, last + 1))
        w = sum(1 for d in span if d in on_disk)
        ids_here = [i for d in span for i in day_ids.get(d, [])]
        c = sum(1 for i in ids_here if i in closed)
        mark = "✅" if w == len(span) else ("…" if w else "—")
        lines.append(
            f"| {phase} | {first}–{last} | {theme} | {mark} {w}/{len(span)} | {c}/{len(ids_here)} |"
        )
    lines.append("")

    lines += ["## By curriculum", "", "| Curriculum | Closed | Total |", "| --- | --- | --- |"]
    for p in PREFIXES:
        ids_here = [i for i in planned if i.startswith(p + "-")]
        lines.append(
            f"| `{p}` — {CURRICULUM_NAMES[p]} | {sum(1 for i in ids_here if i in closed)} | {len(ids_here)} |"
        )
    lines.append("")

    TRACEABILITY.write_text("\n".join(lines), encoding="utf-8")

    # --- CURRICULUM_INDEX.md
    by_prefix: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for i, d in planned.items():
        by_prefix[i.split("-")[0]].append((i, d))

    idx = [
        "# 📇 Curriculum index — Project Akshara",
        "",
        f"_Generated {today} by `scripts/trace.py` from the master plan's §24._",
        "**Do not edit by hand.**",
        "",
        "§24 answers *what does day 88 teach?* This file answers the reverse — *where do I learn",
        "`ARCH-28`?* — which is the question you have when a later day cites an ID you no longer",
        "remember. Every ID appears exactly once; a duplicate or a missing ID is a plan bug.",
        "",
    ]
    for p in PREFIXES:
        rows = sorted(by_prefix[p], key=lambda r: int(r[0].split("-")[1]))
        idx += [
            f"## `{p}` — {CURRICULUM_NAMES[p]} ({len(rows)} IDs)",
            "",
            "| ID | Day | Day title |",
            "| --- | --- | --- |",
        ]
        for i, d in rows:
            title = day_title.get(d, "")
            if len(title) > 90:
                title = title[:88] + "…"
            idx.append(f"| `{i}` | {day_link(d)} | {title} |")
        idx.append("")
    INDEX.write_text("\n".join(idx), encoding="utf-8")

    print(f"traceability: {len(closed)}/{total} closed, {len(problems)} problem(s)")
    for p in problems:
        print(f"  ! {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
