from fastapi.testclient import TestClient

from backend.main import app


def test_debug_env_endpoint_is_not_exposed() -> None:
    client = TestClient(app)

    response = client.get("/debug/env")

    assert response.status_code == 404
