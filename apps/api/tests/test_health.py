"""TC-01.2: /health reports db and s3 status and returns 503 when a component is down."""

import logging
import socket
import threading
import time
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from statforge_api.health import CheckResult, check_db, check_s3
from statforge_api.main import create_app

OK = CheckResult(status="ok")
DB_DOWN = CheckResult(status="down", detail="The database is not reachable.")
S3_DOWN = CheckResult(status="down", detail="File storage is not reachable.")


def _client(db: CheckResult, s3: CheckResult) -> TestClient:
    return TestClient(create_app(checks={"db": lambda: db, "s3": lambda: s3}))


@pytest.mark.tc("TC-01.2")
def test_health_ok_when_all_components_ok() -> None:
    response = _client(OK, OK).get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "components": {
            "db": {"status": "ok", "detail": None},
            "s3": {"status": "ok", "detail": None},
        },
    }


@pytest.mark.tc("TC-01.2")
def test_health_503_when_db_down() -> None:
    response = _client(DB_DOWN, OK).get("/health")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "unavailable"
    assert body["components"]["db"] == {
        "status": "down",
        "detail": "The database is not reachable.",
    }
    assert body["components"]["s3"]["status"] == "ok"


@pytest.mark.tc("TC-01.2")
def test_health_503_when_s3_down() -> None:
    response = _client(OK, S3_DOWN).get("/health")
    assert response.status_code == 503
    assert response.json()["components"]["s3"]["status"] == "down"


@pytest.mark.tc("TC-01.2")
def test_check_db_hides_connection_details(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    result = check_db("postgresql://u:s3cretpw@127.0.0.1:1/x", timeout_s=0.5)
    assert result.status == "down"
    assert result.detail == "The database is not reachable."
    for text in (result.detail or "", caplog.text):
        assert "s3cretpw" not in text
        assert "postgresql://" not in text


@pytest.fixture
def silent_server() -> Iterator[int]:
    """A TCP server that accepts connections and never answers."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen()
    held: list[socket.socket] = []
    stop = threading.Event()

    def accept() -> None:
        server.settimeout(0.2)
        while not stop.is_set():
            try:
                conn, _ = server.accept()
                held.append(conn)
            except TimeoutError:
                continue

    thread = threading.Thread(target=accept, daemon=True)
    thread.start()
    yield int(server.getsockname()[1])
    stop.set()
    thread.join()
    for conn in held:
        conn.close()
    server.close()


@pytest.mark.tc("TC-01.2")
def test_check_db_times_out_on_silent_server(silent_server: int) -> None:
    started = time.monotonic()
    result = check_db(f"postgresql://u:p@127.0.0.1:{silent_server}/x", timeout_s=1.0)
    assert result.status == "down"
    assert time.monotonic() - started < 3.0


@pytest.mark.tc("TC-01.2")
def test_health_is_bounded_when_a_check_hangs() -> None:
    def hangs() -> CheckResult:
        time.sleep(5)
        return OK

    app = create_app(checks={"db": hangs, "s3": lambda: OK}, check_timeout_s=0.5)
    started = time.monotonic()
    response = TestClient(app).get("/health")
    assert time.monotonic() - started < 2.0
    assert response.status_code == 503
    assert response.json()["components"]["db"] == {
        "status": "down",
        "detail": "The database is not reachable.",
    }
    assert response.json()["components"]["s3"]["status"] == "ok"


@pytest.mark.tc("TC-01.2")
def test_check_s3_down_when_unreachable(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    result = check_s3("http://127.0.0.1:1", "key-id", "s3cretkey", timeout_s=0.5)
    assert result == CheckResult(status="down", detail="File storage is not reachable.")
    assert "s3cretkey" not in caplog.text


@pytest.mark.tc("TC-01.2")
def test_default_checks_read_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@127.0.0.1:1/x")
    monkeypatch.setenv("S3_ENDPOINT_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("S3_ACCESS_KEY", "a")
    monkeypatch.setenv("S3_SECRET_KEY", "b")
    response = TestClient(create_app()).get("/health")
    assert response.status_code == 503
    assert {c["status"] for c in response.json()["components"].values()} == {"down"}
