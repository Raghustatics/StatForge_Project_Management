"""TC-01.5: a secret scan of the repo finds 0 secrets, and the scanner does catch one."""

import json
import secrets
import shutil
import string
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.tc("TC-01.5")

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".gitleaks.toml"


def _gitleaks() -> str:
    found = shutil.which("gitleaks")
    if found is None:
        pytest.fail("gitleaks not installed — run scripts/install_tools.ps1")
    return found


def _run(*args: str, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [_gitleaks(), *args], cwd=cwd, capture_output=True, text=True, check=False
    )


def test_repo_history_has_zero_secrets(tmp_path: Path) -> None:
    report = tmp_path / "history.json"
    result = _run(
        "git",
        str(ROOT),
        "--config",
        str(CONFIG),
        "--redact",
        "--exit-code",
        "1",
        "--report-format",
        "json",
        "--report-path",
        str(report),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(report.read_text(encoding="utf-8")) == []


def test_working_tree_has_zero_secrets(tmp_path: Path) -> None:
    report = tmp_path / "tree.json"
    result = _run(
        "dir",
        str(ROOT),
        "--config",
        str(CONFIG),
        "--redact",
        "--exit-code",
        "1",
        "--report-format",
        "json",
        "--report-path",
        str(report),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(report.read_text(encoding="utf-8")) == []


def test_planted_secret_is_detected(tmp_path: Path) -> None:
    # D-032b: the token exists only at runtime, inside a throwaway repo outside the project.
    alphabet = string.ascii_letters + string.digits
    token = "ghp_" + "".join(secrets.choice(alphabet) for _ in range(36))
    repo = tmp_path / "planted"
    repo.mkdir()
    (repo / "settings.py").write_text(f'GITHUB_TOKEN = "{token}"\n', encoding="utf-8")
    for cmd in (
        ["git", "init", "-q"],
        ["git", "add", "settings.py"],
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", "x"],
    ):
        subprocess.run(cmd, cwd=repo, check=True, capture_output=True)
    report = tmp_path / "planted.json"
    result = _run(
        "git",
        str(repo),
        "--redact",
        "--exit-code",
        "1",
        "--report-format",
        "json",
        "--report-path",
        str(report),
        cwd=repo,
    )
    assert result.returncode == 1
    findings = json.loads(report.read_text(encoding="utf-8"))
    assert len(findings) >= 1
    assert token not in report.read_text(encoding="utf-8")  # --redact keeps it out of reports
