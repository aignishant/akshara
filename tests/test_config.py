import os
from pathlib import Path

from akshara.config import device, load_env


def test_load_env_uses_file_values_without_overwriting_environment(
    tmp_path: Path, monkeypatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "FROM_FILE=one\nEXISTING=from-file\nEMPTY=\nexport EXPORTED=two\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("EXISTING", "from-environment")

    assert load_env(env_file) == 2
    assert os.environ["FROM_FILE"] == "one"
    assert os.environ["EXISTING"] == "from-environment"
    assert os.environ["EXPORTED"] == "two"
    assert "EMPTY" not in os.environ


def test_device_can_be_forced_to_cpu(monkeypatch) -> None:
    monkeypatch.setenv("AKSHARA_FORCE_CPU", "1")

    assert device() == "cpu"
