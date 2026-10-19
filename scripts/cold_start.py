"""TC-01.1 cold start: fresh clone → clean pull → `docker compose up` → all healthy, timed.

Condition "clean-pull" (D-032c): before the timer starts, the project's images and
volumes and every base/service image are absent, so the timed run pulls everything
and builds with --no-cache. "cached" is informational only. Never prunes globally.

Usage: python scripts/cold_start.py [--cached]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

BASE_IMAGES: tuple[str, ...] = (
    "postgres:18-alpine",
    "chrislusf/seaweedfs:4.48",
    "python:3.14-slim",
    "ghcr.io/astral-sh/uv:0.10.1",
    "node:24-alpine",
    "nginx:1-alpine",
)
SERVICES = ("web", "api", "db", "s3")
DEFAULT_PORTS: Mapping[str, int] = {"API_PORT": 18000, "WEB_PORT": 18080}

Condition = Literal["clean-pull", "cached"]
Runner = Callable[[Sequence[str], Path], "subprocess.CompletedProcess[str]"]


class ColdStartError(RuntimeError):
    pass


class ColdStartPreconditionError(ColdStartError):
    pass


@dataclass
class ColdStartResult:
    condition: Condition
    seconds: float
    healthy: dict[str, bool]
    absent_before: dict[str, bool] = field(default_factory=dict)


def _run(cmd: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, check=False)


def _must(result: subprocess.CompletedProcess[str], what: str) -> subprocess.CompletedProcess[str]:
    if result.returncode != 0:
        tail = "\n".join((result.stderr or result.stdout or "").splitlines()[-20:])
        raise ColdStartError(f"{what} failed (exit {result.returncode}):\n{tail}")
    return result


def ensure_clean_pull(runner: Runner, cwd: Path) -> dict[str, bool]:
    for image in BASE_IMAGES:
        runner(["docker", "image", "rm", image], cwd)
    absent = {
        image: runner(["docker", "image", "inspect", image], cwd).returncode != 0
        for image in BASE_IMAGES
    }
    for image, gone in absent.items():
        if not gone:
            raise ColdStartPreconditionError(
                f"{image} is still present (in use by another container?) "
                "— stop that container and retry"
            )
    return absent


def _write_env(workdir: Path, ports: Mapping[str, int]) -> None:
    lines = []
    for line in (workdir / ".env.example").read_text(encoding="utf-8").splitlines():
        key = line.partition("=")[0].strip()
        lines.append(f"{key}={ports[key]}" if key in ports else line)
    (workdir / ".env").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _health(ps_output: str) -> dict[str, bool]:
    text = ps_output.strip()
    rows = json.loads(text) if text.startswith("[") else [json.loads(x) for x in text.splitlines()]
    by_service = {row["Service"]: row.get("Health") == "healthy" for row in rows}
    return {service: by_service.get(service, False) for service in SERVICES}


def run_cold_start(
    repo: Path,
    workdir: Path,
    project: str = "statforge-coldstart",
    ports: Mapping[str, int] = DEFAULT_PORTS,
    limit_s: float = 180.0,
    condition: Condition = "clean-pull",
    runner: Runner = _run,
    clock: Callable[[], float] = time.monotonic,
) -> ColdStartResult:
    _must(runner(["git", "clone", "--no-hardlinks", str(repo), str(workdir)], repo), "git clone")
    _write_env(workdir, ports)
    compose = ["docker", "compose", "-p", project]
    try:
        runner([*compose, "down", "-v", "--rmi", "all"], workdir)
        absent = ensure_clean_pull(runner, workdir) if condition == "clean-pull" else {}
        build = ["build", "--no-cache", "--pull"] if condition == "clean-pull" else ["build"]
        started = clock()
        _must(runner([*compose, *build], workdir), "docker compose build")
        up = ["up", "-d", "--wait", "--wait-timeout", str(int(limit_s))]
        _must(runner([*compose, *up], workdir), "docker compose up")
        seconds = clock() - started
        ps = _must(runner([*compose, "ps", "--format", "json"], workdir), "docker compose ps")
        return ColdStartResult(condition, round(seconds, 1), _health(ps.stdout), absent)
    finally:
        runner([*compose, "down", "-v", "--rmi", "local"], workdir)


def write_evidence(result: ColdStartResult, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = directory / f"cold_start_{result.condition}_{stamp}.json"
    payload = {"limit_seconds": 180, **asdict(result)}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Timed cold start of the compose stack")
    parser.add_argument("--cached", action="store_true", help="informational cached run")
    args = parser.parse_args(argv)
    repo = Path(__file__).resolve().parents[1]
    condition: Condition = "cached" if args.cached else "clean-pull"
    tmp = Path(tempfile.mkdtemp(prefix="statforge-coldstart-"))
    try:
        result = run_cold_start(repo, tmp / "clone", condition=condition)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    path = write_evidence(result, repo / "docs" / "evidence" / "G01")
    print(json.dumps(asdict(result), indent=2))
    print(f"evidence: {path}")
    return 0 if result.seconds < 180 and all(result.healthy.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
