"""Test-first commit guard (AGENTS.md §4.1.4).

Blocks a commit that changes product code (apps/, packages/, plugins/) when the
touched unit has no tests for the active gate, either staged in the same commit
or already tracked.

Modes:
  --hook       Claude Code PreToolUse hook: reads the tool call JSON on stdin and
               exits 2 (block, reason on stderr) for a guarded `git commit`.
  --precommit  pre-commit hook on the staged index: exits 1 to block.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from tc_trace import GATE_LOG, active_gate, is_test_file, tc_ids_in

PRODUCT_ROOTS = ("apps/", "packages/", "plugins/")

_GIT_COMMIT = re.compile(
    r"(?:^|[\s;&|(])git(?:\s+(?:-[Cc]\s+\S+|--[\w-]+(?:=\S+)?))*\s+commit(?=\s|$)"
)
_VALUE_FLAGS = set("mFcCt")


@dataclass(frozen=True)
class GuardDecision:
    allowed: bool
    reason: str


def is_git_commit(command: str) -> bool:
    return _GIT_COMMIT.search(command) is not None


def uses_all_flag(command: str) -> bool:
    match = _GIT_COMMIT.search(command)
    if match is None:
        return False
    for arg in command[match.end() :].split():
        if arg == "--all":
            return True
        if arg.startswith("-") and not arg.startswith("--"):
            cluster = ""
            for letter in arg[1:]:
                if letter in _VALUE_FLAGS:
                    break
                cluster += letter
            if "a" in cluster:
                return True
    return False


def unit_of(path: str) -> str | None:
    parts = path.replace("\\", "/").split("/")
    if len(parts) < 3 or f"{parts[0]}/" not in PRODUCT_ROOTS:
        return None
    return f"{parts[0]}/{parts[1]}"


def evaluate(staged: Sequence[str], test_files: Mapping[str, str], gate: str) -> GuardDecision:
    prefix = f"TC-{gate[1:]}."
    units = sorted({unit for path in staged if not is_test_file(path) and (unit := unit_of(path))})
    gate_tests = [
        path
        for path, text in test_files.items()
        if is_test_file(path) and any(tc.startswith(prefix) for tc in tc_ids_in(text))
    ]
    missing = [
        unit
        for unit in units
        if not any(p.startswith(f"{unit}/") or p.startswith("tests/") for p in gate_tests)
    ]
    if missing:
        return GuardDecision(
            False,
            f"Blocked by test-first guard: {', '.join(missing)} has no tests for {gate}. "
            "Commit the RED tests first (AGENTS.md §4.1).",
        )
    return GuardDecision(True, "ok")


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True, encoding="utf-8"
    ).stdout


def _lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def _collect(include_unstaged: bool) -> tuple[list[str], dict[str, str]]:
    staged = _lines(_git("diff", "--cached", "--name-only"))
    if include_unstaged:
        staged += [p for p in _lines(_git("diff", "--name-only")) if p not in staged]
    tests: dict[str, str] = {}
    for path in _lines(_git("ls-files")):
        if is_test_file(path):
            show = subprocess.run(
                ["git", "show", f":{path}"], capture_output=True, text=True, encoding="utf-8"
            )
            if show.returncode == 0:
                tests[path] = show.stdout
            elif include_unstaged and Path(path).exists():
                tests[path] = Path(path).read_text(encoding="utf-8")
    return staged, tests


def _decide(include_unstaged: bool) -> GuardDecision:
    root = Path(_git("rev-parse", "--show-toplevel").strip())
    gate_log = root / GATE_LOG
    if not gate_log.exists():
        return GuardDecision(True, "no gate log; guard not applicable")
    staged, tests = _collect(include_unstaged)
    return evaluate(staged, tests, active_gate(gate_log))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Test-first commit guard")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--hook", action="store_true")
    mode.add_argument("--precommit", action="store_true")
    args = parser.parse_args(argv)
    if args.hook:
        payload = json.loads(sys.stdin.read() or "{}")
        command = str(payload.get("tool_input", {}).get("command", ""))
        if not is_git_commit(command):
            return 0
        decision = _decide(include_unstaged=uses_all_flag(command))
        if not decision.allowed:
            print(decision.reason, file=sys.stderr)
            return 2
        return 0
    decision = _decide(include_unstaged=False)
    if not decision.allowed:
        print(decision.reason, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
