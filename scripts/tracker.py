"""Progress tracker: what is written, at what depth, and what is pending.

Run as `./m tracker` (or `./m status` for the one-line version). Regenerates docs/TRACKER.md.

The part count per day is the point. A day with two parts and four IDs is visible as thin from
this table alone, without opening it (plan §27).
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "docs" / "00_MASTER_PLAN.md"
DAYS = ROOT / "days"
TRACKER = ROOT / "docs" / "TRACKER.md"
PROGRESS = ROOT / "docs" / "PROGRESS.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trace import parse_phases, parse_plan  # noqa: E402


def count_parts(day_dir: Path) -> tuple[int, int]:
    """Return (part files, section folders) for a day."""
    parts = day_dir / "parts"
    if not parts.is_dir():
        return 0, 0
    sections = [p for p in parts.iterdir() if p.is_dir()]
    files = [f for s in sections for f in s.glob("*.md")]
    return len(files), len(sections)


def completed_days() -> set[int]:
    """Days with a row in PROGRESS.md — the only definition of 'finished' (plan §27)."""
    if not PROGRESS.exists():
        return set()
    done: set[int] = set()
    for line in PROGRESS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d{1,3})\s*\|", line)
        if m:
            done.add(int(m.group(1)))
    return done


def main() -> int:
    day_ids, day_title = parse_plan()
    phases = parse_phases()
    done = completed_days()

    on_disk: dict[int, Path] = {}
    if DAYS.is_dir():
        for d in sorted(DAYS.iterdir()):
            m = re.match(r"^day-(\d+)", d.name)
            if d.is_dir() and m:
                on_disk[int(m.group(1))] = d

    total_days = len(day_ids)
    written = len(on_disk)
    total_parts = sum(count_parts(p)[0] for p in on_disk.values())

    if "--summary" in sys.argv:
        nxt = min((d for d in sorted(day_ids) if d not in done), default=None)
        head = f"akshara: {len(done)}/{total_days} days complete · {written} written · {total_parts} parts"
        print(head if nxt is None else f"{head} · next: day {nxt}")
        return 0

    today = date.today().isoformat()
    lines = [
        "# 📊 Tracker — Project Akshara",
        "",
        f"_Generated {today} by `scripts/tracker.py`._ **Do not edit by hand.**",
        "",
        f"**{len(done)} / {total_days} days complete** · {written} written on disk · "
        f"{total_parts} part documents in total.",
        "",
        "`complete` means a row in `docs/PROGRESS.md` (plan §27). `written` means the folder exists",
        "with a `parts/` directory. A day with no `parts/` is not written, whatever the folder looks",
        "like (plan §25.2).",
        "",
        "**Read the parts column.** A day closing three IDs with two parts is thin, and thin is",
        "visible from this table without opening the day.",
        "",
    ]

    for phase, first, last, theme in phases:
        span = list(range(first, last + 1))
        n_done = sum(1 for d in span if d in done)
        mark = "✅" if n_done == len(span) else ("🚧" if any(d in on_disk for d in span) else "⬜")
        lines += [
            f"## {mark} Phase {phase} — {theme}  ({n_done}/{len(span)} complete)",
            "",
            "| Day | Title | IDs | Parts | Sections | Status |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for d in span:
            title = day_title.get(d, "")
            if len(title) > 70:
                title = title[:68] + "…"
            n_ids = len(day_ids.get(d, []))
            if d in on_disk:
                p, s = count_parts(on_disk[d])
                status = "✅ complete" if d in done else "🚧 written"
                link = f"[{d}](../days/{on_disk[d].name}/LESSON.md)"
                thin = " ⚠️ thin" if p and n_ids and p < n_ids * 2 else ""
                lines.append(f"| {link} | {title} | {n_ids} | {p}{thin} | {s} | {status} |")
            else:
                lines.append(f"| {d} | {title} | {n_ids} | — | — | ⬜ pending |")
        lines.append("")

    TRACKER.write_text("\n".join(lines), encoding="utf-8")
    print(f"tracker: {len(done)}/{total_days} complete, {written} written, {total_parts} parts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
