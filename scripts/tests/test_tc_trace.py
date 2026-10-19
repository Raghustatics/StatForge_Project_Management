"""TC-01.6: tc_trace fails on an unmapped TC and passes when every TC is mapped."""

from pathlib import Path

import pytest
import tc_trace

pytestmark = pytest.mark.tc("TC-01.6")

GATE_LOG = "- **Active gate:** G01: Repository, governance and dev environment (in build)\n"
GATE_MAP = """\
#### G01 · Repository (S)
- **Test cases:**
  - TC-01.1 first thing.
  - TC-01.2 second thing.
- **Owner validation:** see TC-01.1 again.

#### G02 · Data model (M)
  - TC-02.1 not ours.
"""


def _repo(tmp_path: Path, files: dict[str, str]) -> Path:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "GATE_LOG.md").write_text(GATE_LOG, encoding="utf-8")
    (tmp_path / "docs" / "StatForge_Gate_Map_v1.0.md").write_text(GATE_MAP, encoding="utf-8")
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


MARKED_PY = """\
import pytest

@pytest.mark.tc("TC-01.1")
def test_first() -> None:
    assert True
"""

NAMED_PY = """\
def test_tc01_2_second() -> None:
    assert True
"""

VITEST_TS = "it('[TC-01.2] second thing in the UI', () => { expect(1).toBe(1) })\n"


def test_active_gate_parsed(tmp_path: Path) -> None:
    root = _repo(tmp_path, {})
    assert tc_trace.active_gate(root / "docs" / "GATE_LOG.md") == "G01"


def test_gate_test_cases_reads_only_that_section(tmp_path: Path) -> None:
    root = _repo(tmp_path, {})
    gate_map = root / "docs" / "StatForge_Gate_Map_v1.0.md"
    assert tc_trace.gate_test_cases(gate_map, "G01") == ["TC-01.1", "TC-01.2"]


def test_trace_fails_when_tc_unmapped(tmp_path: Path) -> None:
    root = _repo(tmp_path, {"apps/api/tests/test_a.py": MARKED_PY})
    result = tc_trace.trace(root)
    assert result.ok is False
    assert result.unmapped == ["TC-01.2"]
    assert tc_trace.main(["--root", str(root)]) == 1


def test_trace_passes_when_all_mapped_by_marker_and_name(tmp_path: Path) -> None:
    root = _repo(
        tmp_path,
        {"apps/api/tests/test_a.py": MARKED_PY, "scripts/tests/test_b.py": NAMED_PY},
    )
    result = tc_trace.trace(root)
    assert result.ok is True
    assert result.unmapped == []
    assert tc_trace.main(["--root", str(root)]) == 0


def test_trace_passes_with_vitest_title(tmp_path: Path) -> None:
    root = _repo(
        tmp_path,
        {"apps/api/tests/test_a.py": MARKED_PY, "apps/web/src/App.test.tsx": VITEST_TS},
    )
    result = tc_trace.trace(root)
    assert result.ok is True
    assert [ref.path for ref in result.mapped["TC-01.2"]] == ["apps/web/src/App.test.tsx"]


def test_module_pytestmark_maps_every_test(tmp_path: Path) -> None:
    module = (
        "import pytest\n\npytestmark = pytest.mark.tc('TC-01.2')\n\n"
        "def test_x() -> None:\n    assert True\n"
    )
    root = _repo(tmp_path, {"apps/api/tests/test_a.py": MARKED_PY, "tests/test_m.py": module})
    assert tc_trace.trace(root).ok is True


def test_skipped_or_xfail_mapping_fails(tmp_path: Path) -> None:
    skipped_py = (
        "import pytest\n\n@pytest.mark.xfail(reason='x')\n@pytest.mark.tc('TC-01.1')\n"
        "def test_first() -> None:\n    assert True\n"
    )
    skipped_ts = "it.skip('[TC-01.2] second thing', () => {})\n"
    root = _repo(
        tmp_path,
        {"apps/api/tests/test_a.py": skipped_py, "apps/web/e2e/second.spec.ts": skipped_ts},
    )
    result = tc_trace.trace(root)
    assert result.ok is False
    assert sorted(ref.tc for ref in result.disabled) == ["TC-01.1", "TC-01.2"]
    assert tc_trace.main(["--root", str(root)]) == 1


def test_ignores_node_modules(tmp_path: Path) -> None:
    root = _repo(
        tmp_path,
        {
            "apps/api/tests/test_a.py": MARKED_PY,
            "apps/web/node_modules/pkg/x.test.ts": VITEST_TS,
        },
    )
    assert tc_trace.trace(root).unmapped == ["TC-01.2"]


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("apps/api/tests/test_health.py", True),
        ("scripts/tests/test_x.py", True),
        ("tests/repo/thing_test.py", True),
        ("apps/web/src/App.test.tsx", True),
        ("apps/web/e2e/placeholder.spec.ts", True),
        ("apps/api/src/statforge_api/health.py", False),
        ("apps/web/src/App.tsx", False),
    ],
)
def test_is_test_file(path: str, expected: bool) -> None:
    assert tc_trace.is_test_file(path) is expected


def test_tc_ids_in() -> None:
    assert tc_trace.tc_ids_in("RED for TC-01.1 TC-01.10 and TC-02.3") == {
        "TC-01.1",
        "TC-01.10",
        "TC-02.3",
    }
