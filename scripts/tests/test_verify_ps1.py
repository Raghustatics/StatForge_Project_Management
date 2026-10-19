"""TC-01.7: verify.ps1 reports each step and names a missing tool instead of crashing.

Runs single steps (-Only) so the test never re-runs the whole suite (no recursion).
Uses Windows PowerShell 5.1 on Windows and pwsh elsewhere (GitHub's Ubuntu runners have it).
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.tc("TC-01.7")

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "verify.ps1"


def _powershell() -> str:
    if sys.platform == "win32":
        system_root = os.environ.get("SYSTEMROOT", r"C:\Windows")
        return str(Path(system_root) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe")
    found = shutil.which("pwsh")
    if found is None:
        pytest.fail("pwsh not installed — verify.ps1 needs PowerShell on this platform")
    return found


def _verify(*args: str, path: str | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    if path is not None:
        env["PATH"] = path
    return subprocess.run(
        [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SCRIPT), *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def test_missing_tool_is_reported_not_crashed() -> None:
    pnpm = shutil.which("pnpm")
    dirs = os.environ["PATH"].split(os.pathsep)
    if pnpm:
        dirs = [d for d in dirs if Path(d).resolve() != Path(pnpm).parent.resolve()]
    result = _verify("-Mode", "Hook", "-Only", "web-lint", path=os.pathsep.join(dirs))
    assert result.returncode == 1, result.stdout + result.stderr
    assert '[FAIL] web-lint: pnpm not found — see README "Setup"' in result.stdout


def test_passing_step_reports_pass() -> None:
    result = _verify("-Mode", "Hook", "-Only", "tc-trace-selftest")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "[PASS] tc-trace-selftest" in result.stdout
    assert "verify: PASS" in result.stdout


def test_failing_step_reports_fail_and_exits_1() -> None:
    result = _verify("-Mode", "Hook", "-Only", "always-fail-selftest")
    assert result.returncode == 1
    assert "[FAIL] always-fail-selftest" in result.stdout
    assert "verify: FAIL" in result.stdout


def test_unknown_step_is_rejected() -> None:
    result = _verify("-Mode", "Hook", "-Only", "no-such-step")
    assert result.returncode == 1
    assert "Unknown step: no-such-step" in result.stdout


def test_hook_mode_lists_the_documented_steps() -> None:
    result = _verify("-Mode", "Hook", "-List")
    assert result.returncode == 0
    listed = result.stdout.split()
    expected = ["ruff-check", "ruff-format", "mypy", "pytest", "web-lint", "web-typecheck"]
    assert listed[: len(expected)] == expected
    assert listed[-2:] == ["web-test", "tc-trace"]


def test_full_mode_adds_coverage_build_scans_and_integration() -> None:
    listed = _verify("-Mode", "Full", "-List").stdout.split()
    for step in (
        "pytest-coverage",
        "web-coverage",
        "web-build",
        "gitleaks",
        "red-green",
        "integration",
        "e2e",
    ):
        assert step in listed
    assert "cold-start" not in listed
    with_cold = _verify("-Mode", "Full", "-IncludeColdStart", "-List").stdout.split()
    assert "cold-start" in with_cold
