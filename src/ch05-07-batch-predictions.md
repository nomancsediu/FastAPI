# Batch Predictions

A batch endpoint processes multiple flowers in one request instead of sending separate HTTP requests for each one.

## The Code

Add to `main.py`:

```python
from schemas import BatchInput, BatchOutput


@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(data: BatchInput):
    """
    Predict species for multiple flowers at once.

    Request:  {"samples": [[...], [...], ...]}
    Response: {"predictions": [...], "count": N}
    """
    results = classifier.predict_batch(data.samples)
    return BatchOutput(predictions=results, count=len(results))
```

## Why Batch?

Compare sending 3 separate requests vs 1 batch request:

**3 separate requests:**
```text
→ POST /predict  [5.1, 3.5, 1.4, 0.2]
← {"species": "setosa"}

→ POST /predict  [6.3, 3.3, 6.0, 2.5]
← {"species": "virginica"}

→ POST /predict  [5.0, 3.4, 1.5, 0.3]
← {"species": "setosa"}

Total: 3 HTTP connections, 3 model calls
```

**1 batch request:**
```text
→ POST /predict/batch
  {"samples": [[5.1, 3.5, 1.4, 0.2],
               [6.3, 3.3, 6.0, 2.5],
               [5.0, 3.4, 1.5, 0.3]]}

← {"predictions": [...], "count": 3}

Total: 1 HTTP connection, 1 model call
```

## The predict_batch Method

In `model.py`:

```python
def predict_batch(self, samples: list) -> list:
    """Predict species for many flowers at once."""
    # Convert list of lists to 2D numpy array
    x = np.array(samples)

    # sklearn processes all samples at once
    class_ids = self.model.predict(x)
    all_probs = self.model.predict_proba(x)

    # Build one result per sample
    results = []
    for i in range(len(class_ids)):
        results.append({
            "species": self.species[class_ids[i]],
            "confidence": float(max(all_probs[i])),
        })
    return results
```

**Why `np.array(samples)`?** sklearn expects a 2D array of shape `(n_samples, n_features)`. A list of lists has the same structure, so we convert it to numpy.

## Testing

### curl

```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"samples": [[5.1, 3.5, 1.4, 0.2], [6.3, 3.3, 6.0, 2.5]]}'
```

Response:
```json
{
  "predictions": [
    {"species": "setosa", "confidence": 1.0},
    {"species": "virginica", "confidence": 0.97}
  ],
  "count": 2
}
```

### pytest

```python
def test_batch_returns_all_predictions():
    """Each input sample gets one prediction."""
    response = client.post("/predict/batch", json={
        "samples": [
            [5.1, 3.5, 1.4, 0.2],
            [6.3, 3.3, 6.0, 2.5],
        ],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["predictions"]) == 2


def test_batch_with_one_item():
    """Batch with a single item should still work."""
    response = client.post("/predict/batch", json={
        "samples": [[5.1, 3.5, 1.4, 0.2]],
    })
    assert response.status_code == 200
    assert response.json()["count"] == 1
```

## When to Use Batch

| Scenario | Use |
|----------|-----|
| Predicting one flower | `POST /predict` (single) |
| Processing many flowers | `POST /predict/batch` (batch) |
| Real-time UI | Single (latency matters) |
| Data pipeline / ETL | Batch (throughput matters) |
