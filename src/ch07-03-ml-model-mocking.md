# ML Model Mocking

## Why Mock ML Models in Tests?

Running actual ML model inference in tests is slow and can produce non-deterministic results (especially for models with random elements). Mocking allows you to replace the real model with a lightweight fake that returns predetermined responses, making tests fast, deterministic, and independent of the model's availability.

## Mock ML Demo

```python
# test_with_mock.py
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_predict_with_mocked_model():
    mock_result = {
        "prediction": "setosa",
        "confidence": 0.99,
        "class_probabilities": {"setosa": 0.99, "versicolor": 0.01, "virginica": 0.0},
        "inference_time_ms": 1.5
    }

    with patch("predict.predictor.predict", return_value=mock_result):
        response = client.post("/predict", json={
            "features": [5.1, 3.5, 1.4, 0.2]
        })

    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "setosa"
    assert data["confidence"] == 0.99

def test_model_loading_failure():
    with patch("predict.IrisPredictor", side_effect=FileNotFoundError("Model not found")):
        response = client.get("/health")
        assert response.status_code in [200, 503]
```
