"""Dependency health checks. Errors are reported in plain language only: no
connection strings, credentials or exception text reach the response or logs."""

import logging
from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor, wait
from typing import Literal

import boto3
import psycopg
from botocore.config import Config
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CheckResult(BaseModel):
    status: Literal["ok", "down"]
    detail: str | None = None


class HealthResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    components: dict[str, CheckResult]


Check = Callable[[], CheckResult]

DOWN_DETAIL = {
    "db": "The database is not reachable.",
    "s3": "File storage is not reachable.",
}


def run_checks(checks: Mapping[str, Check], timeout_s: float) -> dict[str, CheckResult]:
    """Run every check concurrently; a check still running after `timeout_s` counts as down."""
    pool = ThreadPoolExecutor(max_workers=max(1, len(checks)))
    futures = {name: pool.submit(check) for name, check in checks.items()}
    wait(futures.values(), timeout=timeout_s)
    pool.shutdown(wait=False)
    results: dict[str, CheckResult] = {}
    for name, future in futures.items():
        if future.done() and future.exception() is None:
            results[name] = future.result()
        else:
            logger.warning("health check failed: component=%s error=Timeout", name)
            detail = DOWN_DETAIL.get(name, "This component is not reachable.")
            results[name] = CheckResult(status="down", detail=detail)
    return results


def check_db(database_url: str, timeout_s: float = 2.0) -> CheckResult:
    try:
        with psycopg.connect(
            database_url,
            connect_timeout=max(1, round(timeout_s)),
            options=f"-c statement_timeout={int(timeout_s * 1000)}",
        ) as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        logger.warning("health check failed: component=db error=%s", type(exc).__name__)
        return CheckResult(status="down", detail=DOWN_DETAIL["db"])
    return CheckResult(status="ok")


def check_s3(
    endpoint_url: str, access_key: str, secret_key: str, timeout_s: float = 2.0
) -> CheckResult:
    try:
        client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="us-east-1",
            config=Config(
                connect_timeout=timeout_s,
                read_timeout=timeout_s,
                retries={"total_max_attempts": 1},
            ),
        )
        client.list_buckets()
    except Exception as exc:
        logger.warning("health check failed: component=s3 error=%s", type(exc).__name__)
        return CheckResult(status="down", detail=DOWN_DETAIL["s3"])
    return CheckResult(status="ok")
