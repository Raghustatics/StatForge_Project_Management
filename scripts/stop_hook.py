"""Claude Code Stop hook: refuse to end a turn while `verify.ps1 -Mode Hook` fails.

Exit 2 blocks the stop and feeds stderr back to Claude. After `max_blocks`
consecutive blocks the stop is let through with a visible "NOT done" warning, so
an unfixable failure cannot trap the session; `/gate-close` re-runs verify itself
regardless (D-031, D-032e).
"""

from __future__ import annotations

import io
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".claude" / ".stop_hook_state.json"
RELEASE_MESSAGE = (
    "verify.ps1 is FAILING after {n} attempts — the work is NOT done. "
    "Report the failures to the owner."
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    summary: str


@dataclass(frozen=True)
class HookOutcome:
    exit_code: int
    stderr: str
    stdout: str


def _blocks(state_path: Path) -> int:
    try:
        value = json.loads(state_path.read_text(encoding="utf-8")).get("blocks", 0)
        return int(value)
    except OSError, ValueError, AttributeError:
        return 0


def _save(state_path: Path, blocks: int) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps({"blocks": blocks}), encoding="utf-8")


def run_hook(
    payload: Mapping[str, object],
    verify: Callable[[], VerifyResult],
    state_path: Path,
    max_blocks: int = 3,
) -> HookOutcome:
    del payload  # stop_hook_active is not trusted: the block count is ours
    result = verify()
    if result.ok:
        _save(state_path, 0)
        return HookOutcome(0, "", "")
    blocks = _blocks(state_path)
    if blocks >= max_blocks:
        _save(state_path, 0)
        message = RELEASE_MESSAGE.format(n=max_blocks)
        return HookOutcome(0, "", json.dumps({"systemMessage": message}))
    _save(state_path, blocks + 1)
    stderr = (
        "verify.ps1 is failing — the work is not done. Fix these before stopping:\n"
        + result.summary
    )
    return HookOutcome(2, stderr, "")


def _powershell() -> str:
    if sys.platform == "win32":
        system_root = os.environ.get("SYSTEMROOT", r"C:\Windows")
        return str(Path(system_root) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe")
    return shutil.which("pwsh") or "pwsh"


def _verify() -> VerifyResult:
    script = ROOT / "scripts" / "verify.ps1"
    command = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)]
    completed = subprocess.run(
        [*command, "-Mode", "Hook"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    lines = (completed.stdout + completed.stderr).splitlines()
    return VerifyResult(completed.returncode == 0, "\n".join(lines[-40:]))


def _utf8_streams() -> None:
    """Hook output is read as UTF-8; Windows would otherwise pipe it as cp1252."""
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")


def main() -> int:
    _utf8_streams()
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    outcome = run_hook(payload, _verify, STATE)
    if outcome.stdout:
        print(outcome.stdout)
    if outcome.stderr:
        print(outcome.stderr, file=sys.stderr)
    return outcome.exit_code


if __name__ == "__main__":
    sys.exit(main())
