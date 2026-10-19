"""TC-01.7 / TC-01.8 wiring: Claude Code hooks, and /gate-close's independent re-verify."""

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _settings() -> dict[str, Any]:
    data = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _commands(entries: list[dict[str, Any]]) -> list[str]:
    return [hook["command"] for entry in entries for hook in entry["hooks"]]


@pytest.mark.tc("TC-01.7")
def test_stop_hook_wired() -> None:
    stop = _settings()["hooks"]["Stop"]
    commands = _commands(stop)
    assert len(commands) == 1
    assert "scripts/stop_hook.py" in commands[0]
    assert stop[0]["hooks"][0]["timeout"] >= 600


@pytest.mark.tc("TC-01.8")
def test_commit_guard_wired_for_bash_and_powershell() -> None:
    pre = _settings()["hooks"]["PreToolUse"]
    guard = [
        e
        for e in pre
        if any("scripts/commit_guard.py" in c and c.endswith("--hook") for c in _commands([e]))
    ]
    assert len(guard) == 1
    assert set(guard[0]["matcher"].split("|")) == {"Bash", "PowerShell"}


def test_destructive_git_commands_denied() -> None:
    deny = set(_settings()["permissions"]["deny"])
    for tool in ("Bash", "PowerShell"):
        assert f"{tool}(git push --force:*)" in deny
        assert f"{tool}(git reset --hard:*)" in deny


@pytest.mark.tc("TC-01.7")
def test_gate_close_reruns_verify_independently() -> None:
    text = (ROOT / ".claude" / "skills" / "gate-close" / "SKILL.md").read_text(encoding="utf-8")
    preconditions = text.split("## Steps")[0]
    assert "scripts/verify.ps1 -Mode Full" in preconditions
    assert "run it yourself" in preconditions
    assert "even if the Stop hook released" in preconditions
    assert "no merge, no tag, no push" in preconditions
    assert "D-031" in preconditions
