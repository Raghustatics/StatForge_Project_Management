"""TC-01.2 against the real stack: 503 when db (or s3) is stopped, then recovery."""

import pytest
from stack_helpers import compose, get, health, read_env, wait_for

pytestmark = [pytest.mark.integration]


def _component(body: dict[str, object], name: str) -> object:
    components = body["components"]
    assert isinstance(components, dict)
    return components[name]


def test_live_health_ok(api_base: str) -> None:
    status, body = health(api_base)
    assert status == 200
    assert _component(body, "db") == {"status": "ok", "detail": None}
    assert _component(body, "s3") == {"status": "ok", "detail": None}


@pytest.mark.parametrize(
    ("service", "detail"),
    [("db", "The database is not reachable."), ("s3", "File storage is not reachable.")],
)
def test_live_health_503_when_component_stopped(api_base: str, service: str, detail: str) -> None:
    other = "s3" if service == "db" else "db"
    compose("stop", service)
    try:
        assert wait_for(lambda: health(api_base)[0] == 503, timeout_s=10)
        status, body = health(api_base)
        assert status == 503
        assert body["status"] == "unavailable"
        assert _component(body, service) == {"status": "down", "detail": detail}
        assert _component(body, other) == {"status": "ok", "detail": None}
        raw = get(f"{api_base}/health")[1]
        assert "postgresql://" not in raw
        password = read_env().get("POSTGRES_PASSWORD", "")
        assert not password or password not in raw
    finally:
        compose("start", service)
    assert wait_for(lambda: health(api_base)[0] == 200, timeout_s=60), "no recovery"
