"""RED-before-GREEN proof for the active gate (AGENTS.md §4.1.1, TC-01.10).

For every TC of the gate:
  1. a `test(Gxx): RED for … TC-…` commit exists,
  2. a `feat|fix(Gxx): GREEN … TC-…` commit exists,
  3. the earliest RED commit is strictly earlier than the earliest GREEN commit,
  4. a RED evidence file docs/evidence/Gxx/red/<yyyyMMddTHHmmssZ>_<TCs>.txt names
     the TC, is no newer than the earliest RED commit, and shows a failure.

Usage: python scripts/red_green_check.py [--gate G01] [--root .]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from tc_trace import GATE_LOG, GATE_MAP, TC_PATTERN, active_gate, gate_test_cases

_RED = re.compile(r"^test\((?P<gate>G\d{2})\): RED for ")
_GREEN = re.compile(r"^(?:feat|fix)\((?P<gate>G\d{2})\): GREEN ")
_FAILURE = re.compile(r"fail|error", re.IGNORECASE)
_STAMP = re.compile(r"^(\d{8}T\d{6}Z)_")


@dataclass(frozen=True)
class Commit:
    sha: str
    timestamp: int
    subject: str


@dataclass(frozen=True)
class Evidence:
    name: str
    timestamp: int
    tcs: frozenset[str]
    text: str


def evidence_from_file(name: str, text: str) -> Evidence:
    match = _STAMP.match(name)
    if match is None:
        raise ValueError(f"RED evidence file name lacks a UTC timestamp prefix: {name}")
    stamp = datetime.strptime(match.group(1), "%Y%m%dT%H%M%SZ").replace(tzinfo=UTC)
    return Evidence(name, int(stamp.timestamp()), frozenset(TC_PATTERN.findall(name)), text)


def _earliest(
    commits: Sequence[Commit], pattern: re.Pattern[str], gate: str, tc: str
) -> int | None:
    times = [
        c.timestamp
        for c in commits
        if (m := pattern.match(c.subject))
        and m.group("gate") == gate
        and tc in TC_PATTERN.findall(c.subject)
    ]
    return min(times) if times else None


def check(
    commits: Sequence[Commit], evidence: Sequence[Evidence], tcs: Sequence[str], gate: str
) -> list[str]:
    problems: list[str] = []
    for tc in tcs:
        red = _earliest(commits, _RED, gate, tc)
        green = _earliest(commits, _GREEN, gate, tc)
        if red is None:
            problems.append(f"{tc}: no RED commit")
        if green is None:
            problems.append(f"{tc}: no GREEN commit")
        if red is not None and green is not None and not red < green:
            problems.append(f"{tc}: RED commit is not before the GREEN commit")
        if red is not None and not any(
            tc in ev.tcs and ev.timestamp <= red and _FAILURE.search(ev.text) for ev in evidence
        ):
            problems.append(f"{tc}: no RED evidence file showing a failure before the RED commit")
    return problems


def _git_commits(root: Path) -> list[Commit]:
    out = subprocess.run(
        ["git", "log", "--format=%H%x09%ct%x09%s"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    ).stdout
    commits = []
    for line in out.splitlines():
        sha, ts, subject = line.split("\t", 2)
        commits.append(Commit(sha[:7], int(ts), subject))
    return commits


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="RED-before-GREEN check")
    parser.add_argument("--gate")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    gate = args.gate or active_gate(root / GATE_LOG)
    tcs = gate_test_cases(root / GATE_MAP, gate)
    red_dir = root / "docs" / "evidence" / gate / "red"
    evidence = [
        evidence_from_file(p.name, p.read_text(encoding="utf-8", errors="replace"))
        for p in sorted(red_dir.glob("*.txt"))
    ]
    problems = check(_git_commits(root), evidence, tcs, gate)
    for tc in tcs:
        mine = [p for p in problems if p.startswith(f"{tc}:")]
        print(f"{tc:<9} {'OK' if not mine else 'FAIL'}")
        for problem in mine:
            print(f"          - {problem.split(': ', 1)[1]}")
    print(f"red_green_check {gate}: {'PASS' if not problems else 'FAIL'}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
