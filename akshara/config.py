"""Environment and device configuration.

Written on Day 1 (OPS-02, OPS-04). Two functions, no dependency: `load_env` because a
`.env` parser is forty lines of somebody else's code sitting on the one path in this
project that handles a credential (part 2.2), and `device` because the compute tier has
to be a property of the code rather than of a comment (part 4.1).
"""

import os
from pathlib import Path


def load_env(path: str | Path = ".env") -> int:
    """Load NAME=value pairs from `path` into os.environ. Returns how many were set.

    An existing environment variable always wins: the file is a fallback, not an
    authority. That is what lets the same code work on a notebook where the token
    arrives by another route (Day 67).
    """
    p = Path(path)
    if not p.exists():
        return 0
    loaded = 0
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        name, _, value = line.partition("=")
        name, value = name.strip(), value.strip().strip("\"'")
        if not name or not value or name in os.environ:
            continue
        os.environ[name] = value
        loaded += 1
    return loaded


def device() -> str:
    """Return the device to run on: 'cuda' when available and not overridden, else 'cpu'.

    AKSHARA_FORCE_CPU=1 forces CPU even on a GPU machine. That switch exists so the T0
    path can be exercised deliberately on hardware that would otherwise hide it -
    a CPU path that is never run is a CPU path that has quietly rotted.
    """
    if os.environ.get("AKSHARA_FORCE_CPU") == "1":
        return "cpu"
    try:
        import torch
    except ImportError:
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"
