from fastapi.testclient import TestClient
from main import app
from config import API_KEY

client = TestClient(app)

VALID_FEATURES = [5.1, 3.5, 1.4, 0.2]
HEADERS = {"X-API-Key": API_KEY}


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_predict_success():
    resp = client.post("/predict", json={"features": VALID_FEATURES}, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert "species" in data
    assert "confidence" in data


def test_predict_without_api_key():
    resp = client.post("/predict", json={"features": VALID_FEATURES})
    assert resp.status_code == 401


def test_predict_wrong_api_key():
    resp = client.post(
        "/predict", json={"features": VALID_FEATURES}, headers={"X-API-Key": "wrong"}
    )
    assert resp.status_code == 401


def test_predict_invalid_input():
    resp = client.post(
        "/predict",
        json={"features": [1.0, 2.0]},
        headers=HEADERS,
    )
    assert resp.status_code == 422


def test_predict_batch():
    resp = client.post(
        "/predict/batch",
        json={"samples": [VALID_FEATURES, [6.2, 3.4, 5.4, 2.3]]},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
    assert len(data["predictions"]) == 2


def test_register_login_flow():
    resp = client.post(
        "/register",
        params={"username": "testuser", "password": "testpass"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "User created"

    resp = client.post(
        "/login",
        params={"username": "testuser", "password": "testpass"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_predict_v2():
    resp = client.post(
        "/register",
        params={"username": API_KEY, "password": "dummy"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "User created"

    resp = client.post(
        "/predict/v2",
        json={"features": VALID_FEATURES},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "species" in data
