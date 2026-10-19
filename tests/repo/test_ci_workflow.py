"""TC-01.4 / TC-01.9 (static half): the CI workflow runs the gates that must turn a PR red.

The live half (deliberately failing ci-check branches on GitHub) is recorded in
docs/evidence/G01/ci/runs.md.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


def _workflow() -> dict[Any, Any]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _triggers(workflow: dict[Any, Any]) -> dict[str, Any]:
    # PyYAML (YAML 1.1) reads the bare key `on` as the boolean True.
    triggers = workflow.get("on", workflow.get(True))
    assert isinstance(triggers, dict)
    return triggers


def _job_text(workflow: dict[Any, Any], job: str) -> str:
    steps = workflow["jobs"][job]["steps"]
    return "\n".join(str(step.get("run", "")) for step in steps)


@pytest.mark.tc("TC-01.4")
def test_ci_runs_lint_and_tests_on_push_and_pr() -> None:
    workflow = _workflow()
    triggers = _triggers(workflow)
    assert "push" in triggers
    assert set(triggers["pull_request"]["branches"]) >= {"main", "ci-check/**"}
    python = _job_text(workflow, "python")
    assert "ruff check" in python
    assert "ruff format --check" in python
    assert "mypy" in python
    assert "pytest" in python
    web = _job_text(workflow, "web")
    assert "lint" in web
    assert "typecheck" in web
    assert "test:coverage" in web
    assert "build" in web


@pytest.mark.tc("TC-01.9")
def test_ci_enforces_coverage_and_trace() -> None:
    workflow = _workflow()
    assert "pull_request" in _triggers(workflow)
    assert "--cov-fail-under=85" in _job_text(workflow, "python")
    trace = _job_text(workflow, "trace")
    assert "scripts/tc_trace.py" in trace
    assert "scripts/red_green_check.py" in trace
    assert "gitleaks git" in _job_text(workflow, "secrets")
    compose = _job_text(workflow, "compose")
    assert "docker compose up" in compose
    assert "integration and not slow" in compose


def test_ci_jobs_have_timeouts_and_readonly_permissions() -> None:
    workflow = _workflow()
    assert workflow["permissions"] == {"contents": "read"}
    assert set(workflow["jobs"]) == {"python", "web", "trace", "secrets", "compose"}
    for name, job in workflow["jobs"].items():
        assert job["timeout-minutes"] <= 20, name
        assert job["runs-on"] == "ubuntu-latest", name


def test_ci_history_jobs_fetch_full_depth() -> None:
    workflow = _workflow()
    for name in ("trace", "secrets"):
        checkout = workflow["jobs"][name]["steps"][0]
        assert checkout["uses"].startswith("actions/checkout@")
        assert checkout["with"]["fetch-depth"] == 0, name
