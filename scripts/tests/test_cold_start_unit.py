"""TC-01.1: the cold-start procedure itself (no Docker; the runner is faked)."""

import re
import subprocess
from collections.abc import Sequence
from pathlib import Path

import cold_start
import pytest

pytestmark = pytest.mark.tc("TC-01.1")

ROOT = Path(__file__).resolve().parents[2]
PS_JSON = "\n".join(
    f'{{"Service": "{s}", "State": "running", "Health": "healthy"}}'
    for s in ("web", "api", "db", "s3")
)
STEP_LABELS = (
    "git clone",
    "down -v --rmi all",
    "image rm",
    "image inspect",
    "build --no-cache --pull",
    "build",
    "up -d --wait",
    "ps --format json",
    "down -v --rmi local",
)


class FakeRunner:
    def __init__(self, fail_on: str | None = None, present: frozenset[str] = frozenset()) -> None:
        self.calls: list[list[str]] = []
        self.fail_on = fail_on
        self.present = present

    def __call__(self, cmd: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        self.calls.append(list(cmd))
        if list(cmd[:2]) == ["git", "clone"]:
            target = Path(cmd[-1])
            target.mkdir(parents=True)
            (target / ".env.example").write_text("API_PORT=8000\nWEB_PORT=8080\n")
        if self.fail_on and self.fail_on in " ".join(cmd):
            return subprocess.CompletedProcess(list(cmd), 1, "", "boom")
        if list(cmd[1:3]) == ["image", "inspect"]:
            return subprocess.CompletedProcess(list(cmd), 0 if cmd[3] in self.present else 1)
        out = PS_JSON if "ps" in cmd else ""
        return subprocess.CompletedProcess(list(cmd), 0, out, "")


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        self.now += 30.0
        return self.now


def _steps(calls: list[list[str]]) -> list[str]:
    labels = []
    for cmd in calls:
        text = " ".join(cmd)
        labels.append(next(label for label in STEP_LABELS if label in text))
    return labels


def test_command_sequence(tmp_path: Path) -> None:
    runner = FakeRunner()
    result = cold_start.run_cold_start(ROOT, tmp_path / "c", runner=runner, clock=Clock())
    n = len(cold_start.BASE_IMAGES)
    assert _steps(runner.calls) == (
        ["git clone", "down -v --rmi all"]
        + ["image rm"] * n
        + ["image inspect"] * n
        + ["build --no-cache --pull", "up -d --wait", "ps --format json", "down -v --rmi local"]
    )
    assert result.condition == "clean-pull"
    assert result.seconds == 30.0
    assert result.healthy == {"web": True, "api": True, "db": True, "s3": True}
    assert all(result.absent_before.values())
    env = (tmp_path / "c" / ".env").read_text()
    assert "API_PORT=18000" in env
    assert "WEB_PORT=18080" in env


def test_cached_condition_skips_image_removal(tmp_path: Path) -> None:
    runner = FakeRunner()
    result = cold_start.run_cold_start(
        ROOT, tmp_path / "c", condition="cached", runner=runner, clock=Clock()
    )
    assert "image rm" not in _steps(runner.calls)
    assert result.condition == "cached"
    assert result.absent_before == {}


def test_down_runs_even_when_up_fails(tmp_path: Path) -> None:
    runner = FakeRunner(fail_on="up -d")
    with pytest.raises(cold_start.ColdStartError, match="boom"):
        cold_start.run_cold_start(ROOT, tmp_path / "c", runner=runner, clock=Clock())
    assert _steps(runner.calls)[-1] == "down -v --rmi local"


def test_never_prunes(tmp_path: Path) -> None:
    runner = FakeRunner()
    cold_start.run_cold_start(ROOT, tmp_path / "c", runner=runner, clock=Clock())
    assert not any("prune" in cmd for cmd in runner.calls)  # token, not substring of paths


def test_precondition_fails_when_base_image_remains(tmp_path: Path) -> None:
    runner = FakeRunner(present=frozenset({"node:24-alpine"}))
    with pytest.raises(cold_start.ColdStartPreconditionError, match="node:24-alpine"):
        cold_start.run_cold_start(ROOT, tmp_path / "c", runner=runner, clock=Clock())
    assert "build --no-cache --pull" not in _steps(runner.calls)


def test_write_evidence(tmp_path: Path) -> None:
    result = cold_start.ColdStartResult("clean-pull", 42.5, {"api": True}, {"x:1": True})
    path = cold_start.write_evidence(result, tmp_path)
    assert path.name.startswith("cold_start_clean-pull_")
    assert '"seconds": 42.5' in path.read_text(encoding="utf-8")


def test_base_images_match_dockerfiles_and_compose() -> None:
    found: set[str] = set()
    for dockerfile in ("apps/api/Dockerfile", "apps/web/Dockerfile"):
        text = (ROOT / dockerfile).read_text(encoding="utf-8")
        found.update(re.findall(r"^FROM\s+(\S+)", text, re.MULTILINE))
        found.update(re.findall(r"COPY --from=(\S+:\S+)", text))
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    found.update(re.findall(r"^\s+image:\s*(\S+)", compose, re.MULTILINE))
    assert {image for image in found if ":" in image} == set(cold_start.BASE_IMAGES)
