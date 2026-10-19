"""TC-01.10: RED runs and RED commits come before the matching GREEN commits."""

import os
import subprocess
from pathlib import Path

import pytest
import red_green_check
from red_green_check import Commit, Evidence, check, evidence_from_file

pytestmark = pytest.mark.tc("TC-01.10")

TCS = ["TC-01.1", "TC-01.2"]
T0 = 1_760_000_000


def _red(ts: int, subject: str = "test(G01): RED for TC-01.1 TC-01.2 thing") -> Commit:
    return Commit("r" * 7, ts, subject)


def _green(ts: int, subject: str = "feat(G01): GREEN TC-01.1 TC-01.2 thing") -> Commit:
    return Commit("g" * 7, ts, subject)


def _ev(ts: int, tcs: tuple[str, ...] = ("TC-01.1", "TC-01.2"), text: str = "1 failed") -> Evidence:
    return Evidence("x.txt", ts, frozenset(tcs), text)


def test_passes_when_red_precedes_green() -> None:
    assert check([_red(T0 + 10), _green(T0 + 20)], [_ev(T0)], TCS, "G01") == []


def test_fails_when_green_before_red() -> None:
    problems = check([_green(T0 + 10), _red(T0 + 20)], [_ev(T0)], TCS, "G01")
    assert any("TC-01.1" in p and "not before" in p for p in problems)


def test_fails_when_red_and_green_same_second() -> None:
    problems = check([_red(T0 + 10), _green(T0 + 10)], [_ev(T0)], TCS, "G01")
    assert problems


def test_fails_without_red_commit() -> None:
    problems = check([_green(T0 + 20)], [_ev(T0)], TCS, "G01")
    assert any("no RED commit" in p for p in problems)


def test_fails_without_green_commit() -> None:
    problems = check([_red(T0 + 20)], [_ev(T0)], TCS, "G01")
    assert any("no GREEN commit" in p for p in problems)


def test_fails_without_evidence_file() -> None:
    problems = check([_red(T0 + 10), _green(T0 + 20)], [], TCS, "G01")
    assert any("no RED evidence" in p for p in problems)


def test_fails_when_evidence_shows_no_failure() -> None:
    problems = check([_red(T0 + 10), _green(T0 + 20)], [_ev(T0, text="4 passed")], TCS, "G01")
    assert any("no RED evidence" in p for p in problems)


def test_fails_when_evidence_newer_than_red_commit() -> None:
    problems = check([_red(T0 + 10), _green(T0 + 20)], [_ev(T0 + 15)], TCS, "G01")
    assert any("no RED evidence" in p for p in problems)


def test_other_gate_commits_ignored() -> None:
    commits = [_red(T0 + 10, "test(G02): RED for TC-01.1"), _green(T0 + 20)]
    problems = check(commits, [_ev(T0)], ["TC-01.1"], "G01")
    assert any("no RED commit" in p for p in problems)


def test_multiple_tcs_in_one_subject_count_for_each() -> None:
    commits = [
        _red(T0 + 10),
        _green(T0 + 20, "feat(G01): GREEN TC-01.1"),
        _green(T0 + 30, "fix(G01): GREEN TC-01.2 follow-up"),
    ]
    assert check(commits, [_ev(T0)], TCS, "G01") == []


def test_evidence_from_filename() -> None:
    evidence = evidence_from_file("20261019T185520Z_TC-01.4_TC-01.9.txt", "Exit code: 1 FAILED")
    assert evidence.tcs == frozenset({"TC-01.4", "TC-01.9"})
    assert evidence.timestamp == 1_792_436_120


def test_main_on_a_real_git_history(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    def git(*args: str, when: str | None = None) -> None:
        env = dict(os.environ)
        if when:
            env.update(GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, env=env)

    (tmp_path / "docs" / "evidence" / "G01" / "red").mkdir(parents=True)
    (tmp_path / "docs" / "GATE_LOG.md").write_text("- **Active gate:** G01: x\n")
    (tmp_path / "docs" / "StatForge_Gate_Map_v1.0.md").write_text(
        "#### G01 · x\n  - TC-01.1 a.\n", encoding="utf-8"
    )
    git("init", "-q")
    git("config", "user.name", "t")
    git("config", "user.email", "t@example.invalid")
    red = tmp_path / "docs" / "evidence" / "G01" / "red" / "20261019T100000Z_TC-01.1.txt"
    red.write_text("1 failed")
    git("add", ".")
    git("commit", "-qm", "test(G01): RED for TC-01.1 x", when="2026-10-19T10:00:05Z")
    assert red_green_check.main(["--root", str(tmp_path)]) == 1
    (tmp_path / "x.py").write_text("X = 1\n")
    git("add", ".")
    git("commit", "-qm", "feat(G01): GREEN TC-01.1 x", when="2026-10-19T10:00:09Z")
    assert red_green_check.main(["--root", str(tmp_path)]) == 0
    assert "red_green_check G01: PASS" in capsys.readouterr().out


def test_evidence_file_without_timestamp_rejected() -> None:
    with pytest.raises(ValueError, match="timestamp"):
        evidence_from_file("TC-01.1.txt", "failed")
