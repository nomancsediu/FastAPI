# Testing the API with Auth

Now that our `/predict` and `/predict/batch` endpoints require an API key (from
Chapter 6), our tests must include the `X-API-Key` header.

## Step 1: Install Test Tools

```bash
cd mlapi
pip install pytest httpx
```

## Step 2: Create the Test File

```bash
mkdir -p tests
touch tests/__init__.py tests/test_api.py
```

## Step 3: Write Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

API_KEY = "ml-inference-key-123"  # Must match your .env file
```

### Happy Path — With Valid API Key

```python
def test_predict_setosa():
    """Known setosa features → species='setosa' with high confidence."""
    response = client.post(
        "/predict",
        json={"features": [5.1, 3.5, 1.4, 0.2]},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["species"] == "setosa"
    assert data["confidence"] > 0.9


def test_predict_virginica():
    """Known virginica features → species='virginica'."""
    response = client.post(
        "/predict",
        json={"features": [6.3, 3.3, 6.0, 2.5]},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    assert response.json()["species"] == "virginica"


def test_batch():
    """Batch endpoint returns one prediction per sample."""
    response = client.post(
        "/predict/batch",
        json={
            "samples": [
                [5.1, 3.5, 1.4, 0.2],
                [6.3, 3.3, 6.0, 2.5],
            ],
        },
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["predictions"]) == 2
```

### Auth Tests — Wrong or Missing API Key

```python
def test_predict_without_api_key():
    """No API key → 401."""
    response = client.post(
        "/predict",
        json={"features": [5.1, 3.5, 1.4, 0.2]},
    )
    assert response.status_code == 401


def test_predict_with_wrong_api_key():
    """Wrong API key → 401."""
    response = client.post(
        "/predict",
        json={"features": [5.1, 3.5, 1.4, 0.2]},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
```

### Validation Tests — Bad Input

```python
def test_wrong_number_of_features():
    """4 features required. 3 features → 422."""
    response = client.post(
        "/predict",
        json={"features": [1.0, 2.0, 3.0]},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 422


def test_empty_features():
    """Empty list → 422."""
    response = client.post(
        "/predict",
        json={"features": []},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 422


def test_non_numeric_features():
    """Strings instead of numbers → 422."""
    response = client.post(
        "/predict",
        json={"features": ["a", "b", "c", "d"]},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 422
```

### Public Endpoints — No Auth Required

```python
def test_root():
    """Root endpoint is public."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Health check is public."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

## Step 4: Run Tests

```bash
pytest tests/test_api.py -v
```

Expected output:

```
tests/test_api.py ...........                                       [100%]
11 passed in 0.85s
```

## What Each Test Covers

| Test | What It Protects Against |
|------|-------------------------|
| `test_predict_setosa` | API endpoint broken or schema changed |
| `test_predict_virginica` | Model accuracy regression |
| `test_batch` | Batch endpoint broken |
| `test_predict_without_api_key` | Auth not enforced (security hole) |
| `test_predict_with_wrong_api_key` | Auth bypass with wrong key |
| `test_wrong_number_of_features` | Schema validation missing |
| `test_empty_features` | Edge case — empty list crashes server |
| `test_non_numeric_features` | Type validation broken |
| `test_root` | Root endpoint broken |
| `test_health` | Health check broken |

`TestClient` works just like curl — no server needed, no special setup.
