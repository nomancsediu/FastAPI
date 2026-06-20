# Testing the ML API

We write two kinds of tests:
1. **Model tests** — test the ML logic (no HTTP)
2. **API tests** — test the HTTP endpoints

Both use the real model (it's only a few KB). No mocking needed.

## Setup

```bash
cd mlapi
pip install pytest httpx
mkdir tests
touch tests/__init__.py
```

---

## Test 1: The Model (tests/test_model.py)

These tests call `classifier.predict()` directly, without going through HTTP.

```python
# tests/test_model.py
from model import classifier


def test_species_is_string():
    """
    The prediction must include a species name.
    If this fails, something is wrong with the model loading.
    """
    result = classifier.predict([5.1, 3.5, 1.4, 0.2])
    assert isinstance(result["species"], str)
    assert isinstance(result["confidence"], float)


def test_confidence_is_between_0_and_1():
    """
    Confidence is a probability, so it must be between 0 and 1.
    If sklearn returns something outside this range, our code has a bug.
    """
    result = classifier.predict([6.3, 3.3, 6.0, 2.5])
    assert 0.0 <= result["confidence"] <= 1.0


def test_different_flowers_have_different_species():
    """
    A setosa flower and a virginica flower should NOT get the same prediction.
    If they do, the model isn't learning anything useful.
    """
    setosa = classifier.predict([5.1, 3.5, 1.4, 0.2])
    virginica = classifier.predict([6.3, 3.3, 6.0, 2.5])
    assert setosa["species"] != virginica["species"]


def test_batch_returns_all_results():
    """
    Batch prediction must return one result per input sample.
    Losing or duplicating results would be a serious bug.
    """
    samples = [
        [5.1, 3.5, 1.4, 0.2],
        [6.3, 3.3, 6.0, 2.5],
    ]
    results = classifier.predict_batch(samples)
    assert len(results) == 2
```

**Why test the model directly?** If a test fails, we know immediately whether the bug is in the model logic or the API layer. It's faster than debugging through HTTP.

---

## Test 2: The API (tests/test_api.py)

These tests send HTTP requests through FastAPI's `TestClient` and check the responses.

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

# TestClient simulates HTTP requests without a real server
client = TestClient(app)
```

### Happy Path — The API Works Correctly

```python
def test_predict_setosa():
    """
    Given the measurements of a setosa flower,
    the API should return species='setosa' with high confidence.
    """
    response = client.post("/predict", json={
        "features": [5.1, 3.5, 1.4, 0.2],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["species"] == "setosa"
    assert data["confidence"] > 0.9


def test_predict_virginica():
    """
    Given the measurements of a virginica flower,
    the API should return species='virginica'.
    """
    response = client.post("/predict", json={
        "features": [6.3, 3.3, 6.0, 2.5],
    })
    assert response.status_code == 200
    assert response.json()["species"] == "virginica"
```

### Error Handling — The API Rejects Bad Input

```python
def test_wrong_number_of_features():
    """4 features required. Sending 3 should return 422."""
    response = client.post("/predict", json={
        "features": [1.0, 2.0, 3.0],
    })
    assert response.status_code == 422


def test_empty_features():
    """Empty list should return 422."""
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422


def test_missing_features():
    """Missing 'features' key should return 422."""
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_non_numeric_features():
    """String values where numbers are expected should return 422."""
    response = client.post("/predict", json={
        "features": ["a", "b", "c", "d"],
    })
    assert response.status_code == 422
```

**Why test 422 errors?** Validation is your first line of defense. Bad input should never reach your model. If our schema has a bug (like forgetting `min_length=4`), these tests catch it.

### Batch Endpoint

```python
def test_batch():
    """Batch endpoint returns one prediction per sample."""
    response = client.post("/predict/batch", json={
        "samples": [
            [5.1, 3.5, 1.4, 0.2],
            [6.3, 3.3, 6.0, 2.5],
            [5.0, 3.4, 1.5, 0.3],
        ],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 3
    assert len(data["predictions"]) == 3


def test_batch_single_item():
    """Batch with one sample should still work (edge case)."""
    response = client.post("/predict/batch", json={
        "samples": [[5.1, 3.5, 1.4, 0.2]],
    })
    assert response.status_code == 200
    assert response.json()["count"] == 1
```

### Utility Endpoints

```python
def test_root():
    """Root endpoint returns welcome message with endpoints listing."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Health check returns ok — used by monitoring systems."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

---

## Run All Tests

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_model.py ....                                               [ 25%]
tests/test_api.py ............                                         [100%]
16 passed in 1.23s
```

### What Each Test Covers

| Test | What It Protects Against |
|------|-------------------------|
| `test_species_is_string` | Model loading failed, returned wrong type |
| `test_confidence_is_between_0_and_1` | sklearn API change or numpy type bug |
| `test_different_flowers_have_different_species` | Model not learning (always same prediction) |
| `test_batch_returns_all_results` | Batch logic losing or mixing up results |
| `test_predict_setosa` | API endpoint not working or schema changed |
| `test_predict_virginica` | Model accuracy regression |
| `test_wrong_number_of_features` | Schema validation not enforcing constraints |
| `test_empty_features` | Edge case: empty list |
| `test_missing_features` | Edge case: missing required field |
| `test_non_numeric_features` | Type validation not working |
| `test_batch` | Batch endpoint broken |
| `test_batch_single_item` | Edge case: single item in batch |
| `test_root` | Root endpoint broken |
| `test_health` | Health check broken |

## Testing Approach Summary

| Aspect | Model Tests | API Tests |
|--------|-------------|-----------|
| What they test | ML logic | HTTP layer |
| How they call | `classifier.predict()` | `client.post("/predict", ...)` |
| Speed | <1ms per test | <5ms per test |
| Fail if | Model is wrong | API is wrong |

Run both. If a test fails, you know exactly where the bug is.
