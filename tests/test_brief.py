"""The brief projects; it never writes (Principles 7 and 8).

`./m brief` exists so a session does not have to read the whole master plan. That is only safe
while every fact it emits is *copied*. This test reads the generated brief back and asserts each
row of it appears verbatim in the plan or the progress ledger. A brief that quietly started
paraphrasing would be a plausible-looking summary of the contract the entire curriculum is
written against — which is the failure Principle 8 exists to prevent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import brief  # noqa: E402  — importable only after the line above puts scripts/ on the path

#: The day shapes the plan actually contains: a day with no IDs, ordinary two-ID days, the
#: single-ID day, the four-ID day, a late day, and the last day of all.
SAMPLE_DAYS = (0, 16, 29, 71, 143, 161)

SOURCE_LINES = {
    line.strip()
    for path in (brief.PLAN, brief.PROGRESS)
    for line in path.read_text(encoding="utf-8").splitlines()
}

#: The brief's own scaffolding — table headers, and the pointers to the sections it deliberately
#: does not project. Neither states a fact about the curriculum.
SCAFFOLD = ("| Day | Title |", "| ID | Concept |", "| Phase | Days |", "| Section | Command |")


def projected_rows(text: str) -> list[str]:
    """Every row of the brief that asserts something, with the scaffolding dropped."""
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or set(line) <= set("| -"):
            continue
        if line.startswith(SCAFFOLD) or "sed -n" in line:
            continue
        rows.append(line.strip())
    return rows


@pytest.mark.parametrize("day", SAMPLE_DAYS)
def test_every_projected_row_is_verbatim(day: int) -> None:
    rows = projected_rows(brief.build(day))
    assert rows, f"day {day} projected no rows at all"
    for row in rows:
        assert row in SOURCE_LINES, f"day {day}: row is not verbatim from a source file: {row}"


@pytest.mark.parametrize("day", SAMPLE_DAYS)
def test_the_brief_carries_every_id_the_day_map_assigns(day: int) -> None:
    day_row, _, _, id_defs = brief.parse_plan(day)
    ids = [i.strip(" `") for i in day_row[2].split(",") if i.strip(" `—-")]
    text = brief.build(day)
    for identifier in ids:
        assert identifier in id_defs, (
            f"day {day} claims {identifier}, which no §7–§23 table defines"
        )
        assert f"| `{identifier}` |" in text, f"day {day}'s brief omits {identifier}"


def test_a_day_the_plan_does_not_have_is_refused() -> None:
    with pytest.raises(SystemExit):
        brief.build(999)
