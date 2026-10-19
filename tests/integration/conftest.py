"""Fixtures for tests that need the running stack (`docker compose up -d --wait`)."""

import os

import pytest
from stack_helpers import get, read_env


@pytest.fixture(scope="session")
def api_base() -> str:
    port = os.environ.get("API_PORT") or read_env().get("API_PORT") or "8000"
    base = f"http://localhost:{port}"
    try:
        get(f"{base}/api/v1/version")
    except OSError:
        pytest.fail("Start the stack first: docker compose up -d --wait")
    return base
