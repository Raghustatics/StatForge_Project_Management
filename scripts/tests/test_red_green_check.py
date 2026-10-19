"""TC-01.10: RED runs and RED commits come before the matching GREEN commits."""

import pytest
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
