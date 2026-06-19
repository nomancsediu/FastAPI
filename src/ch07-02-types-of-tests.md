# Types of Tests

## Unit Tests

Unit tests verify that individual functions and methods work correctly in isolation. For ML APIs, unit tests cover functions like data preprocessing, feature engineering, and output formatting:

```python
# test_unit.py
import pytest
from schemas import PredictionInput, IrisInput

def test_prediction_input_valid():
    data = {"features": [5.1, 3.5, 1.4, 0.2], "model_name": "random_forest"}
    parsed = PredictionInput(**data)
    assert len(parsed.features) == 4

def test_prediction_input_invalid_length():
    with pytest.raises(Exception):
        PredictionInput(features=[1.0, 2.0])

def test_prediction_input_invalid_range():
    with pytest.raises(Exception):
        PredictionInput(features=[5.1, 3.5, 1.4, 100.0])
```

## Integration Tests

Integration tests verify that multiple components work together correctly:

```python
# test_integration.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post("/predict", json={
        "features": [5.1, 3.5, 1.4, 0.2]
    })
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0

def test_invalid_input():
    response = client.post("/predict", json={
        "features": [5.1, 3.5]
    })
    assert response.status_code == 422
```
