#!/usr/bin/env bash
# Project Akshara daily driver. Replaces `make` (which is not installed on Windows).
# Written on Day 0; every later day assumes it. See plan §25.9.
set -euo pipefail

DAY="${2:-}"
pad() { printf "%03d" "$1"; }

# A day folder is days/day-NNN-<slug>/ (plan §25.2). The number is the identity and the slug is a
# label on it, so resolve by number and accept whatever slug follows - that is what lets a folder be
# renamed to a better slug without breaking any of this. Three digits, because the plan runs to 161.
daydir() {
  local n d
  n="$1"
  for d in "days/day-$(pad "$n")-"*; do
    [ -d "$d" ] && { echo "$d"; return; }
  done
  if [ -d "days/day-$(pad "$n")" ]; then echo "days/day-$(pad "$n")"
  else echo ""; fi
}

case "${1:-help}" in
  start)
    [ -z "$DAY" ] && { echo "usage: ./m start <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no day $DAY yet - see docs/TRACKER.md for what is written"; exit 1; }
    if [ -f "$D/LESSON.md" ] && [ -d "$D/parts" ]; then
      echo "-> open $D/LESSON.md   (the hub - read its §2 map, then the parts in order)"
      find "$D/parts" -name '*.md' | sort | sed "s|^$D/|     |"
    else
      echo "day $DAY has no hub + parts/ - it is not written (plan §25.2)"; exit 1
    fi
    ;;

  parts)
    [ -z "$DAY" ] && { echo "usage: ./m parts <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -d "$D/parts" ] || { echo "day $DAY has no parts/ - not written (plan §25.2)"; exit 1; }
    find "$D/parts" -name '*.md' | sort | sed "s|^$D/parts/||"
    ;;

  depth)
    if [ -n "$DAY" ]; then uv run python scripts/depth_check.py "$DAY"
    else uv run python scripts/depth_check.py; fi
    ;;

  scaffold)
    [ -z "$DAY" ] && { echo "usage: ./m scaffold <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no day $DAY yet - the day is written before its lab"; exit 1; }
    mkdir -p "$D/lab"
    echo "-> created $D/lab   (your scratch code)"
    ;;

  trace)
    uv run python scripts/trace.py
    ;;

  tracker)
    uv run python scripts/tracker.py
    ;;

  status)
    uv run python scripts/tracker.py --summary
    ;;

  check)
    uv run ruff check .
    uv run ruff format --check .
    # pytest exits 5 for "no tests collected". Before the first test day there are none, and an
    # empty suite is not a failure - so 0 and 5 pass and everything else stops the gate.
    # -m "not gpu": the gate must run on a laptop with no CUDA (CLAUDE.md).
    uv run python -m pytest -q -m "not gpu" || [ $? -eq 5 ]

    # -- Day 1 / OPS-02, part 2.1: a credential-shaped string in a TRACKED file stops the gate.
    # Tracked, not modified: untracked files are not the risk, committed ones are.
    #
    # Owned false positive (Day 0 part 5.2 - a check whose false positives are undocumented is a
    # check people switch off). Teaching material has to be able to *show* the shape of a token:
    # Day 1 part 2.3 builds its whole leak demo around one fabricated `hf_` string. That literal
    # is allowlisted here BY VALUE rather than by exempting days/, so a new fake token in a future
    # day goes red and has to be added on purpose instead of slipping through a directory hole.
    FAKE_TOKENS='hf_ABCDEFGHIJKLMNOPQRSTUVWXYZ012345'
    CRED_RE="hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    creds="$(git ls-files -z | xargs -0 grep -nE "$CRED_RE" 2>/dev/null | grep -vF "$FAKE_TOKENS" || true)"
    if [ -n "$creds" ]; then
      echo "FAIL credential-shaped string in a tracked file"
      echo "$creds"
      echo "     ROTATE the credential first, then clean the repo - in that order. Rotation is what"
      echo "     makes the copies worthless; cleaning never reaches the clones anyone already made."
      exit 1
    fi

    # -- Day 1 / OPS-01, part 1.2: the dependency arrow points one way. Tooling knows about the
    # project; the project knows nothing about its tooling. If depth_check.py needed akshara to
    # import, it would stop working exactly when the repository is broken - which is when it is
    # needed. Anchored at line start: a mention inside a docstring is not an import.
    if grep -rn '^from akshara\|^import akshara' scripts/ >/dev/null 2>&1; then
      echo "FAIL scripts/ imports akshara - the arrow points one way (Day 1 part 1.2)"
      grep -rn '^from akshara\|^import akshara' scripts/
      exit 1
    fi

    # -- Day 1 / OPS-03, part 3.4: a generated ledger must never be stale or hand-edited.
    # Snapshot the on-disk copies, regenerate, compare. An edit applied to one of these three
    # is overwritten by the next `./m check` with no warning at all - that silence is the whole
    # failure part 3.4 demonstrates, and this makes it loud.
    #
    # Compared against the copy on disk, NOT against HEAD. `./m done N` runs this gate BEFORE it
    # commits, and finishing a day legitimately changes TRACKER.md; a HEAD diff would refuse every
    # completed day. The question here is "is the file what the generators produce?", not "does it
    # equal the last commit?".
    GEN="docs/TRACEABILITY.md docs/CURRICULUM_INDEX.md docs/TRACKER.md"
    SNAP="$(mktemp -d)"
    for f in $GEN; do
      if [ -f "$f" ]; then cp "$f" "$SNAP/$(basename "$f")"; fi
    done
    uv run python scripts/depth_check.py
    uv run python scripts/trace.py
    uv run python scripts/tracker.py
    STALE=""
    for f in $GEN; do
      b="$SNAP/$(basename "$f")"
      if [ ! -f "$b" ]; then STALE="$STALE $f(was missing)"
      elif ! cmp -s "$b" "$f"; then STALE="$STALE $f"
      fi
    done
    rm -rf "$SNAP"
    if [ -n "$STALE" ]; then
      echo "FAIL a generated ledger was stale or hand-edited:$STALE"
      echo "     It has been regenerated in place. Read the diff, then fix the INPUT - plan §24.2"
      echo "     or the day hub's \`ids:\` frontmatter - never the generated file. Re-run the gate."
      exit 1
    fi

    echo "OK all green"
    ;;

  done)
    [ -z "$DAY" ] && { echo "usage: ./m done <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no day folder for $DAY"; exit 1; }
    C="$D/CHECKLIST.md"
    # A MISSING checklist fails rather than passing vacuously: the naive version greps a file that
    # is not there, finds no unticked boxes, and concludes everything is ticked. Absence must never
    # read as success.
    [ -f "$C" ] || { echo "FAIL no $C"; exit 1; }
    # Principle 9: never commit weights or data. A staged checkpoint is a hard stop, and it is
    # tested FIRST - before the checklist - because it is the only refusal here guarding a mistake
    # you cannot take back. An unticked box costs you a re-run; a committed 400MB checkpoint is in
    # the history of every clone forever (Day 0 part 3.2).
    if git diff --cached --name-only 2>/dev/null | grep -Eq '\.(safetensors|gguf|bin|pt|pth|ckpt|npy)$|^data/|^checkpoints/'; then
      echo "FAIL a weight/dataset file is staged - Principle 9: the repo holds what reproduces a model, never the model"
      git diff --cached --name-only | grep -E '\.(safetensors|gguf|bin|pt|pth|ckpt|npy)$|^data/|^checkpoints/'
      exit 1
    fi
    # The anchor ^ matters: without it a line *describing* a checkbox inside a code sample counts
    # as an unticked box, and the gate refuses forever for a reason nobody can find.
    if grep -q '^- \[ \]' "$C"; then
      echo "FAIL unticked boxes remain in $C"; grep -n '^- \[ \]' "$C"; exit 1
    fi
    "$0" check
    uv run python scripts/tracker.py
    git add -A && git commit -m "day-$(pad "$DAY"): complete"
    echo "OK day $DAY committed"
    ;;

  *)
    cat <<'USAGE'
usage: ./m <command> [day]

  status         one line: how many days are written / complete
  tracker        regenerate docs/TRACKER.md
  trace          regenerate docs/TRACEABILITY.md + CURRICULUM_INDEX.md from the hubs vs plan §24
  start N        point at day N's hub and list its parts/
  parts N        list day N's sub-topic documents
  depth [N]      check day N (or every written day) against plan §25, the depth contract
  scaffold N     create days/day-NNN-<slug>/lab/
  check          ruff + ruff format + CPU-only pytest + depth contract + traceability
  done N         refuse unless the checklist is ticked, no weights are staged, and checks are
                 green - then commit
USAGE
    ;;
esac
