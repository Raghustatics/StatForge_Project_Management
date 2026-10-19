"""Repository hygiene guard rails (R-07, D-025, D-032d, D-032f)."""

import json
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "docs/StatForge_Development_Guidelines_v1.1.md",
    "docs/StatForge_Gate_Map_v1.0.md",
    "docs/GATE_LOG.md",
    "docs/DECISIONS.md",
    "docs/RISKS.md",
    "docs/PORTING.md",
    "docs/TROUBLESHOOTING.md",
    "docs/OWNER_PROMPTS.md",
    "docs/SKILLS_MAP.md",
    "docs/reference/",
    "docs/sessions/",
    ".claude/agents/",
    ".claude/skills/",
    "sources/88_Templates/Project Phase Template v0.1.xlsx",
]


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False)


@pytest.mark.tc("TC-01.5")
def test_tc01_5_minitab_fixtures_never_tracked() -> None:
    assert _git("ls-files", "sources/Business_Cases_Examples").stdout.strip() == ""
    ignored = _git("check-ignore", "-q", "sources/Business_Cases_Examples/Minitab_Datasets_1.xlsx")
    assert ignored.returncode == 0


def test_env_file_ignored() -> None:
    assert _git("check-ignore", "-q", ".env").returncode == 0


@pytest.mark.parametrize("path", GOVERNANCE_PATHS)
def test_governance_docs_are_tracked(path: str) -> None:
    tracked = _git("ls-files", "--error-unmatch", path)
    assert tracked.returncode == 0, f"{path} is not committed"
    assert _git("check-ignore", "-q", path).returncode == 1, f"{path} is git-ignored"


def test_pnpm_version_pinned() -> None:
    manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    assert isinstance(manifest.get("packageManager"), str)
    assert re.fullmatch(r"pnpm@\d+\.\d+\.\d+", manifest["packageManager"])
