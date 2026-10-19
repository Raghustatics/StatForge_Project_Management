"""TC-01.1: clean-pull cold start of the whole stack from a fresh clone in < 3 min."""

from pathlib import Path

import cold_start
import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.tc("TC-01.1")
def test_tc01_1_clean_pull_cold_start_under_3_minutes(tmp_path: Path) -> None:
    result = cold_start.run_cold_start(ROOT, tmp_path / "clone")
    cold_start.write_evidence(result, ROOT / "docs" / "evidence" / "G01")
    assert result.condition == "clean-pull"
    assert result.absent_before
    assert all(result.absent_before.values())
    assert result.seconds < 180
    assert result.healthy == {"web": True, "api": True, "db": True, "s3": True}
