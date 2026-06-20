# Testing the Model Directly

Model tests call the `IrisClassifier` directly — no HTTP, no auth headers needed.
These are pure unit tests that verify the ML logic itself.

## Setup

```bash
cd mlapi
pip install pytest
```

---

## Test File: `tests/test_model.py`

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

**Why test the model directly?** If a test fails, you know immediately whether the
bug is in the model logic or the API layer. It's faster than debugging through HTTP.

---

## Run All Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_model.py ....                                               [ 26%]
tests/test_api.py ...........                                          [100%]
15 passed in 1.10s
```

| Aspect | Model Tests | API Tests |
|--------|-------------|-----------|
| What they test | ML logic | HTTP layer + auth |
| How they call | `classifier.predict()` | `client.post("/predict", headers={"X-API-Key": ...})` |
| Auth needed | No | Yes |
| Speed | <1ms per test | <5ms per test |
| Fail if | Model is wrong | API / auth is wrong |

Run both. If a test fails, you know exactly where the bug is.
