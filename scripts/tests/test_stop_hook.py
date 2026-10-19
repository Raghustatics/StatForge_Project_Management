"""TC-01.7: the Stop hook blocks "done" while verify.ps1 fails."""

import json
from pathlib import Path

import pytest
from stop_hook import HookOutcome, VerifyResult, run_hook

pytestmark = pytest.mark.tc("TC-01.7")

FAILING = VerifyResult(ok=False, summary="[PASS] ruff-check\n[FAIL] pytest: 1 failed")
PASSING = VerifyResult(ok=True, summary="[PASS] pytest")


def _run(state: Path, result: VerifyResult, active: bool = False) -> HookOutcome:
    return run_hook({"stop_hook_active": active}, lambda: result, state)


def test_blocks_stop_when_verify_fails(tmp_path: Path) -> None:
    outcome = _run(tmp_path / "state.json", FAILING)
    assert outcome.exit_code == 2
    assert "the work is not done" in outcome.stderr
    assert "[FAIL] pytest" in outcome.stderr


def test_allows_stop_when_verify_passes(tmp_path: Path) -> None:
    outcome = _run(tmp_path / "state.json", PASSING)
    assert outcome.exit_code == 0
    assert outcome.stderr == ""


def test_releases_after_three_blocks_with_warning(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    codes = [_run(state, FAILING, active=i > 0).exit_code for i in range(3)]
    assert codes == [2, 2, 2]
    released = _run(state, FAILING, active=True)
    assert released.exit_code == 0
    message = json.loads(released.stdout)["systemMessage"]
    assert "FAILING" in message
    assert "NOT done" in message
    assert _run(state, FAILING).exit_code == 2  # the count starts again


def test_state_resets_after_pass(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    _run(state, FAILING)
    _run(state, FAILING)
    assert _run(state, PASSING).exit_code == 0
    codes = [_run(state, FAILING).exit_code for _ in range(3)]
    assert codes == [2, 2, 2]


def test_corrupt_state_file_is_treated_as_zero(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    state.write_text("{not json")
    assert _run(state, FAILING).exit_code == 2
