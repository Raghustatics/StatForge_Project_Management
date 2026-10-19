"""TC-01.8: the test-first commit guard blocks product code without tests for the gate."""

import io
import json
import subprocess
import sys
from pathlib import Path

import commit_guard
import pytest

pytestmark = pytest.mark.tc("TC-01.8")

SCRIPT = Path(__file__).resolve().parents[1] / "commit_guard.py"
G01_TEST = 'import pytest\n\n@pytest.mark.tc("TC-01.2")\ndef test_x() -> None:\n    assert True\n'
G02_TEST = 'import pytest\n\n@pytest.mark.tc("TC-02.1")\ndef test_x() -> None:\n    assert True\n'


def test_blocks_product_code_without_tests() -> None:
    decision = commit_guard.evaluate(["apps/api/src/statforge_api/new.py"], {}, "G01")
    assert decision.allowed is False
    assert "apps/api" in decision.reason
    assert "G01" in decision.reason
    assert "test-first guard" in decision.reason


def test_allows_tests_first_then_code() -> None:
    first = commit_guard.evaluate(
        ["apps/api/tests/test_new.py"], {"apps/api/tests/test_new.py": G01_TEST}, "G01"
    )
    assert first.allowed is True
    second = commit_guard.evaluate(
        ["apps/api/src/statforge_api/new.py"], {"apps/api/tests/test_new.py": G01_TEST}, "G01"
    )
    assert second.allowed is True


def test_root_tests_count_for_any_unit() -> None:
    decision = commit_guard.evaluate(
        ["packages/engine/src/statforge_engine/x.py"], {"tests/repo/test_a.py": G01_TEST}, "G01"
    )
    assert decision.allowed is True


def test_docs_only_commit_allowed() -> None:
    assert commit_guard.evaluate(["docs/DECISIONS.md", "README.md"], {}, "G01").allowed is True


def test_tests_for_other_gate_do_not_count() -> None:
    decision = commit_guard.evaluate(
        ["apps/api/src/statforge_api/new.py"], {"apps/api/tests/test_new.py": G02_TEST}, "G01"
    )
    assert decision.allowed is False


def test_tests_in_another_unit_do_not_count() -> None:
    decision = commit_guard.evaluate(
        ["plugins/foo/plugin.py"], {"apps/api/tests/test_new.py": G01_TEST}, "G01"
    )
    assert decision.allowed is False
    assert "plugins/foo" in decision.reason


@pytest.mark.parametrize(
    ("path", "unit"),
    [
        ("apps/api/src/x.py", "apps/api"),
        ("apps/web/src/App.tsx", "apps/web"),
        ("packages/engine/src/statforge_engine/a.py", "packages/engine"),
        ("plugins/foo/x.py", "plugins/foo"),
        ("docs/x.md", None),
        ("scripts/x.py", None),
    ],
)
def test_unit_of(path: str, unit: str | None) -> None:
    assert commit_guard.unit_of(path) == unit


@pytest.mark.parametrize(
    "command",
    [
        "git commit -m x",
        "git commit -am x",
        "git -C repo commit",
        "git -c user.name=a commit -m x",
        "cd repo && git commit -m 'x'",
        "git commit -m @'\nmsg\n'@",
    ],
)
def test_is_git_commit_true(command: str) -> None:
    assert commit_guard.is_git_commit(command) is True


@pytest.mark.parametrize(
    "command", ["git status", "git log --grep commit", "echo commit", "git commit-tree abc"]
)
def test_is_git_commit_false(command: str) -> None:
    assert commit_guard.is_git_commit(command) is False


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("git commit -a -m x", True),
        ("git commit -am x", True),
        ("git commit --all -m x", True),
        ("git commit -m x", False),
        ("git commit --amend -m x", False),
    ],
)
def test_uses_all_flag(command: str, expected: bool) -> None:
    assert commit_guard.uses_all_flag(command) is expected


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.name", "t")
    _git(tmp_path, "config", "user.email", "t@example.invalid")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "GATE_LOG.md").write_text("- **Active gate:** G01: x\n")
    _git(tmp_path, "add", "docs")
    _git(tmp_path, "commit", "-qm", "base")
    return tmp_path


def _hook(repo: Path, command: str) -> subprocess.CompletedProcess[str]:
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--hook"],
        input=payload,
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )


def test_hook_mode_end_to_end(repo: Path) -> None:
    code = repo / "apps" / "api" / "src" / "demo.py"
    code.parent.mkdir(parents=True)
    code.write_text("X = 1\n")
    _git(repo, "add", "apps")
    blocked = _hook(repo, "git commit -m demo")
    assert blocked.returncode == 2
    assert "test-first guard" in blocked.stderr

    test = repo / "apps" / "api" / "tests" / "test_demo.py"
    test.parent.mkdir(parents=True)
    test.write_text(G01_TEST)
    _git(repo, "add", "apps")
    assert _hook(repo, "git commit -m demo").returncode == 0


def test_hook_ignores_non_commit_commands(repo: Path) -> None:
    code = repo / "apps" / "api" / "src" / "demo.py"
    code.parent.mkdir(parents=True)
    code.write_text("X = 1\n")
    _git(repo, "add", "apps")
    assert _hook(repo, "git status").returncode == 0


def test_all_flag_includes_unstaged_changes(repo: Path) -> None:
    code = repo / "apps" / "api" / "src" / "demo.py"
    test = repo / "apps" / "api" / "tests" / "test_demo.py"
    code.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    code.write_text("X = 1\n")
    test.write_text(G02_TEST)
    _git(repo, "add", "apps")
    _git(repo, "commit", "-qm", "seed")
    code.write_text("X = 2\n")  # tracked, modified, NOT staged
    assert _hook(repo, "git commit -m x").returncode == 0  # nothing staged
    assert _hook(repo, "git commit -am x").returncode == 2  # -a stages it


def test_precommit_mode(repo: Path) -> None:
    code = repo / "apps" / "web" / "src" / "x.ts"
    code.parent.mkdir(parents=True)
    code.write_text("export const x = 1;\n")
    _git(repo, "add", "apps")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--precommit"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "apps/web" in result.stderr


def _main_in(repo: Path, monkeypatch: pytest.MonkeyPatch, argv: list[str], stdin: str = "") -> int:
    monkeypatch.chdir(repo)
    monkeypatch.setattr(sys, "stdin", io.StringIO(stdin))
    return commit_guard.main(argv)


def test_main_in_process_hook_and_precommit(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    code = repo / "apps" / "api" / "src" / "demo.py"
    code.parent.mkdir(parents=True)
    code.write_text("X = 1\n")
    _git(repo, "add", "apps")
    commit = json.dumps({"tool_input": {"command": "git commit -m x"}})
    assert _main_in(repo, monkeypatch, ["--hook"], commit) == 2
    assert "test-first guard" in capsys.readouterr().err
    assert _main_in(repo, monkeypatch, ["--hook"], json.dumps({"tool_input": {}})) == 0
    assert _main_in(repo, monkeypatch, ["--precommit"]) == 1
    test = repo / "apps" / "api" / "tests" / "test_demo.py"
    test.parent.mkdir(parents=True)
    test.write_text(G01_TEST)
    _git(repo, "add", "apps")
    assert _main_in(repo, monkeypatch, ["--hook"], commit) == 0
    assert _main_in(repo, monkeypatch, ["--precommit"]) == 0


def test_main_allows_outside_a_gated_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _git(tmp_path, "init", "-q")
    commit = json.dumps({"tool_input": {"command": "git commit -m x"}})
    assert _main_in(tmp_path, monkeypatch, ["--hook"], commit) == 0


def test_hook_from_a_subdirectory_uses_repo_root_paths(repo: Path) -> None:
    code = repo / "apps" / "api" / "src" / "demo.py"
    test = repo / "apps" / "api" / "tests" / "test_demo.py"
    code.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    code.write_text("X = 1\n")
    test.write_text(G01_TEST)
    _git(repo, "add", "apps")
    assert _hook(repo / "apps" / "api", "git commit -m demo").returncode == 0
