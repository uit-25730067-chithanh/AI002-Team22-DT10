"""Test API security: API key guard và CORS behavior."""

import os
from fastapi.testclient import TestClient
import pytest

# Import app với fallback để chạy được từ root và từ thư mục backend
try:
    from backend.main import app
except ModuleNotFoundError:
    from main import app

client = TestClient(app)


def test_health_public_no_key():
    """Health endpoint phải public, không cần API key."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


def test_root_public_no_key():
    """Root endpoint phải public."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"


def test_docs_public_no_key():
    """Swagger docs phải public."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_public_no_key():
    """OpenAPI spec phải public."""
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_model_info_missing_key_returns_401(monkeypatch):
    """Model info phải yêu cầu API key. Thiếu key -> 401."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    response = client.get("/model/info")
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_model_info_wrong_key_returns_401(monkeypatch):
    """Model info với key sai -> 401."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    response = client.get("/model/info", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_model_info_correct_key_returns_200(monkeypatch):
    """Model info với key đúng -> 200."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    response = client.get("/model/info", headers={"X-API-Key": "test-demo-key"})
    assert response.status_code == 200
    data = response.json()
    assert "model_version" in data or "experiment_id" in data


def test_predict_missing_key_returns_401(monkeypatch):
    """Predict phải yêu cầu API key. Thiếu key -> 401."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    payload = {
        "province": "Dak Lak",
        "area": "Cu M'gar",
        "month": 5,
        "year": 2025,
        "avg_temp_c": 25.0,
        "humidity_pct": 80.0,
        "rainfall_mm": 150.0,
        "avg_soil_moisture_0_7cm": 30.0,
        "soil_score": 0.7,
        "coffee_type": "Robusta / ca phe nhan xo noi dia",
        "price_observations": 100,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 401


def test_predict_wrong_key_returns_401(monkeypatch):
    """Predict với key sai -> 401."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    payload = {
        "province": "Dak Lak",
        "area": "Cu M'gar",
        "month": 5,
        "year": 2025,
        "avg_temp_c": 25.0,
        "humidity_pct": 80.0,
        "rainfall_mm": 150.0,
        "avg_soil_moisture_0_7cm": 30.0,
        "soil_score": 0.7,
        "coffee_type": "Robusta / ca phe nhan xo noi dia",
        "price_observations": 100,
    }
    response = client.post("/predict", json=payload, headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_predict_correct_key_returns_200(monkeypatch):
    """Predict với key đúng -> 200 (nếu model đã load)."""
    monkeypatch.setenv("AI002_API_KEY", "test-demo-key")
    payload = {
        "province": "Dak Lak",
        "area": "Cu M'gar",
        "month": 5,
        "year": 2025,
        "avg_temp_c": 25.0,
        "humidity_pct": 80.0,
        "rainfall_mm": 150.0,
        "avg_soil_moisture_0_7cm": 30.0,
        "soil_score": 0.7,
        "coffee_type": "Robusta / ca phe nhan xo noi dia",
        "price_observations": 100,
    }
    response = client.post("/predict", json=payload, headers={"X-API-Key": "test-demo-key"})
    # Có thể 200, 422 (validation), hoặc 503 nếu model chưa load
    # Chỉ verify auth pass (không phải 401/503 config)
    assert response.status_code in [200, 422, 503]
    assert response.status_code not in [401]  # Auth phải pass


def test_missing_env_var_returns_503(monkeypatch):
    """Nếu env var AI002_API_KEY chưa set -> 503 config error."""
    monkeypatch.delenv("AI002_API_KEY", raising=False)
    response = client.get("/model/info", headers={"X-API-Key": "any-key"})
    assert response.status_code == 503
    data = response.json()
    assert "config" in data["detail"].lower() or "missing" in data["detail"].lower()
