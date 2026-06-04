import crawler.area_dataset_builder as area_dataset_builder
import crawler.price_crawler_common as price_crawler_common
import model.experiment_tracker as experiment_tracker
from fastapi.testclient import TestClient

from backend.main import app


def test_debug_env_endpoint_is_not_exposed() -> None:
    client = TestClient(app)

    response = client.get("/debug/env")

    assert response.status_code == 404
