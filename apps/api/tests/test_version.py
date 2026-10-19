"""TC-01.3 (api side): the version endpoint that the placeholder page shows."""

import pytest
from fastapi.testclient import TestClient
from statforge_api.main import create_app


@pytest.mark.tc("TC-01.3")
def test_version_endpoint() -> None:
    response = TestClient(create_app(checks={})).get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"name": "StatForge API", "version": "0.1.0", "api": "v1"}
