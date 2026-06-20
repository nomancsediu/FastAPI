# Building the Iris Classification API

We'll build a complete ML project with separate files for training, model logic, schemas, and API routes. Each file has one job — this makes the code easy to understand and maintain.

## Project Structure

```
mlapi/
├── train.py              # Train the model and save to disk (run once)
├── model.py              # Load the saved model and make predictions
├── schemas.py            # Define input/output data formats
├── main.py               # FastAPI app with API endpoints
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_model.py     # Test the model directly
    └── test_api.py       # Test the API endpoints
```

Each file is explained below. Read them in order: train → model → schemas → main.

---

## Step 1: Train the Model

`train.py` loads the iris dataset, trains a Random Forest model, and saves it to disk.

```python
# Import the tools we need
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Load the iris dataset
#    X = feature matrix (150 flowers × 4 measurements)
#    y = target labels (0=setosa, 1=versicolor, 2=virginica)
iris = load_iris()
X = iris.data
y = iris.target

# 2. Split data into training (80%) and testing (20%)
#    The model learns from the training set.
#    We evaluate it on the testing set (which it has never seen).
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train a Random Forest model
#    Random Forest combines many decision trees for better accuracy.
#    n_estimators = number of trees (100 is a good default).
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluate accuracy on the test set
#    This tells us how well the model generalizes to new data.
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# 5. Save the trained model to disk with joblib
#    We load this file later in model.py — no retraining needed.
joblib.dump(model, "iris_model.joblib")
print("Model saved to iris_model.joblib")
```

**Why Random Forest?** It works well without tuning, handles small datasets, and gives probability scores (confidence). Perfect for beginners.

**Why `random_state=42`?** It makes the results reproducible. Every time you run this, you get the same split and same accuracy.

**Why save with joblib?** scikit-learn recommends joblib over pickle. It's faster and handles NumPy arrays better.

### Run it

```bash
pip install scikit-learn joblib
python train.py
```

Output:
```
Accuracy: 0.97
Model saved to iris_model.joblib
```

---

## Step 2: Create the Model Wrapper

`model.py` loads the saved model and provides easy-to-use prediction methods.

```python
import joblib
import numpy as np


class IrisClassifier:
    """
    Wraps the trained sklearn model with clean prediction methods.

    Why a class? It keeps the model loading and prediction logic
    in one place. The API file (main.py) doesn't need to know
    about numpy or joblib — it just calls predict().
    """

    def __init__(self, model_path: str = "iris_model.joblib"):
        # Load the model from disk (happens once when server starts)
        self.model = joblib.load(model_path)
        # The three iris species in order (0, 1, 2)
        self.species = ["setosa", "versicolor", "virginica"]

    def predict(self, features: list) -> dict:
        """
        Predict species for one flower.

        Input:  [5.1, 3.5, 1.4, 0.2]  (4 measurements)
        Output: {"species": "setosa", "confidence": 1.0}
        """
        # Convert list to numpy array and reshape for sklearn
        # reshape(1, -1) means: 1 row, as many columns as needed
        x = np.array(features).reshape(1, -1)

        # Get predicted class (0, 1, or 2)
        class_id = self.model.predict(x)[0]

        # Get probability for each class
        probabilities = self.model.predict_proba(x)[0]

        return {
            "species": self.species[class_id],
            "confidence": float(max(probabilities)),
        }

    def predict_batch(self, samples: list) -> list:
        """
        Predict species for many flowers at once.

        Input:  [[5.1, 3.5, 1.4, 0.2], [6.3, 3.3, 6.0, 2.5]]
        Output: [{"species": "setosa", ...}, {"species": "virginica", ...}]
        """
        x = np.array(samples)
        class_ids = self.model.predict(x)
        all_probs = self.model.predict_proba(x)

        results = []
        for i in range(len(class_ids)):
            results.append({
                "species": self.species[class_ids[i]],
                "confidence": float(max(all_probs[i])),
            })
        return results


# Create a single instance that gets imported by main.py
# This runs once when the server starts, not on every request
classifier = IrisClassifier()
```

**Why `reshape(1, -1)`?** sklearn expects a 2D array (samples × features). A single flower has shape `(4,)`. We reshape it to `(1, 4)` — one sample with four features.

**Why `float(max(probabilities))`?** `predict_proba()` returns NumPy float64 values. We convert to Python float for JSON serialization and take the highest probability as confidence.

**Why create an instance at module level?** The line `classifier = IrisClassifier()` runs when the server imports this file. The model loads once and stays in memory for all future requests.

---

## Step 3: Define the Data Schemas

`schemas.py` defines what data the API accepts and returns.

```python
from pydantic import BaseModel, Field
from typing import List


class IrisInput(BaseModel):
    """
    The client sends exactly 4 flower measurements.
    Pydantic validates this BEFORE the request reaches our code.
    """
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Four measurements: sepal_length, sepal_width, "
                    "petal_length, petal_width",
    )


class IrisOutput(BaseModel):
    """The API returns the predicted species and confidence score."""
    species: str = Field(
        ...,
        description="Predicted iris species name",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0",
    )


class BatchInput(BaseModel):
    """For batch predictions: a list of flower measurements."""
    samples: List[List[float]] = Field(
        ...,
        min_length=1,
        description="List of flower measurement arrays",
    )


class BatchOutput(BaseModel):
    """Batch predictions: one result per input sample."""
    predictions: List[IrisOutput]
    count: int
```

**Why `BaseModel`?** It's Pydantic's base class. It gives us automatic validation, type checking, and JSON schema generation.

**Why `Field(...)`?** The `...` means required. `min_length=4` and `max_length=4` ensure exactly 4 features. If the client sends 3 or 5, FastAPI returns a 422 error before our code runs.

**Why `ge=0.0, le=1.0`?** A confidence score is a probability. These constraints guarantee it's always valid. If our model somehow returns 1.5, FastAPI catches it.

---

## Step 4: Build the API

`main.py` connects everything together with four endpoints.

```python
from fastapi import FastAPI, HTTPException
from schemas import IrisInput, IrisOutput, BatchInput, BatchOutput
from model import classifier

# Create the FastAPI application
# title appears in the Swagger UI at /docs
app = FastAPI(title="Iris Classifier API")


@app.get("/")
def root():
    """Welcome message showing how to use the API."""
    return {
        "message": "Iris Classifier API",
        "endpoints": {
            "POST /predict": "Predict one iris flower",
            "POST /predict/batch": "Predict multiple flowers",
            "GET /health": "Health check",
        },
    }


@app.post("/predict", response_model=IrisOutput)
def predict_iris(data: IrisInput):
    """
    Predict the species of an iris flower.

    Request body: {"features": [5.1, 3.5, 1.4, 0.2]}
    Response: {"species": "setosa", "confidence": 1.0}
    """
    try:
        return classifier.predict(data.features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(data: BatchInput):
    """
    Predict species for multiple flowers at once.

    Request body: {"samples": [[5.1, 3.5, 1.4, 0.2], [6.3, 3.3, 6.0, 2.5]]}
    """
    try:
        results = classifier.predict_batch(data.samples)
        return BatchOutput(predictions=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    """Simple health check for monitoring."""
    return {"status": "ok", "model": "Random Forest"}
```

**Why `response_model=`?** FastAPI uses this to validate the output, filter extra fields, and generate the API documentation automatically.

**Why try/except?** The model could fail (corrupted file, wrong input shape). We catch all exceptions and return a clean 500 error instead of crashing.

**Why four endpoints?**
- `GET /` — welcome/help message
- `POST /predict` — main prediction endpoint
- `POST /predict/batch` — batch predictions
- `GET /health` — monitoring (used by load balancers, Kubernetes, etc.)

---

## Step 5: Run the API

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

| Part | Meaning |
|------|---------|
| `main:app` | File `main.py`, variable `app` |
| `--reload` | Auto-restart when code changes (remove in production) |

Open `http://localhost:8000/docs` in your browser. You'll see the Swagger UI with all four endpoints, their request/response formats, and a "Try it out" button.

---

## Step 6: Test with curl

Open a new terminal and run these commands one by one:

```bash
# 1. Welcome message
curl http://localhost:8000/

# 2. Predict a setosa flower (small petals)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# Response: {"species":"setosa","confidence":1.0}

# 3. Predict a virginica flower (large petals)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [6.3, 3.3, 6.0, 2.5]}'

# Response: {"species":"virginica","confidence":0.97}

# 4. Batch prediction
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"samples": [[5.1, 3.5, 1.4, 0.2], [6.3, 3.3, 6.0, 2.5]]}'

# 5. Health check
curl http://localhost:8000/health

# Response: {"status":"ok","model":"Random Forest"}
```

---

## Step 7: Test with pytest

Create `tests/test_model.py` and `tests/test_api.py`:

### Test the model directly

```python
# tests/test_model.py — tests the ML logic without HTTP
from model import classifier


def test_species_is_string():
    """The prediction should include a species name (string)."""
    result = classifier.predict([5.1, 3.5, 1.4, 0.2])
    assert isinstance(result["species"], str)
    assert isinstance(result["confidence"], float)


def test_confidence_is_valid():
    """Confidence should always be between 0 and 1."""
    result = classifier.predict([6.3, 3.3, 6.0, 2.5])
    assert 0.0 <= result["confidence"] <= 1.0


def test_different_flowers_have_different_species():
    """Setosa and virginica should get different predictions."""
    setosa = classifier.predict([5.1, 3.5, 1.4, 0.2])
    virginica = classifier.predict([6.3, 3.3, 6.0, 2.5])
    assert setosa["species"] != virginica["species"]


def test_batch_returns_all_results():
    """Batch should return one result per input sample."""
    samples = [
        [5.1, 3.5, 1.4, 0.2],
        [6.3, 3.3, 6.0, 2.5],
    ]
    results = classifier.predict_batch(samples)
    assert len(results) == 2
```

### Test the API endpoints

```python
# tests/test_api.py — tests the HTTP layer
from fastapi.testclient import TestClient
from main import app

# TestClient sends fake HTTP requests to our app
# No real server needed — it works in-memory
client = TestClient(app)


def test_predict_setosa():
    """Setosa features → species='setosa' with high confidence."""
    response = client.post("/predict", json={
        "features": [5.1, 3.5, 1.4, 0.2],
    })
    assert response.status_code == 200
    data = response.json()
    assert data["species"] == "setosa"
    assert data["confidence"] > 0.9


def test_predict_virginica():
    """Virginica features → species='virginica'."""
    response = client.post("/predict", json={
        "features": [6.3, 3.3, 6.0, 2.5],
    })
    assert response.status_code == 200
    assert response.json()["species"] == "virginica"


def test_wrong_number_of_features():
    """4 features required. 3 should return 422."""
    response = client.post("/predict", json={
        "features": [1.0, 2.0, 3.0],
    })
    assert response.status_code == 422


def test_empty_features():
    """Empty list should return 422."""
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422


def test_missing_features():
    """Missing 'features' field should return 422."""
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_non_numeric_features():
    """Strings instead of numbers should return 422."""
    response = client.post("/predict", json={
        "features": ["a", "b", "c", "d"],
    })
    assert response.status_code == 422


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
    """Batch with one sample should still work."""
    response = client.post("/predict/batch", json={
        "samples": [[5.1, 3.5, 1.4, 0.2]],
    })
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_root():
    """Root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Health check returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

### Run all tests

```bash
pip install pytest httpx
pytest tests/ -v
```

Expected output:
```
tests/test_model.py ....                                               [ 25%]
tests/test_api.py ............                                         [100%]
16 passed in 1.23s
```

---

## Data Flow Summary

```text
Client                          Server
  │                               │
  │  POST /predict                │
  │  {"features": [5.1, 3.5,     │
  │   1.4, 0.2]}                  │
  │ ─────────────────────────►    │
  │                               │
  │                     main.py receives request
  │                     │
  │                     ▼
  │               schemas.py validates:
  │               - features is a list of 4 floats
  │               - each value is a number
  │                     │
  │                     ▼
  │               model.py:
  │               - loads iris_model.joblib (once at startup)
  │               - calls model.predict(features)
  │               - returns species name + confidence
  │                     │
  │                     ▼
  │               FastAPI converts to JSON
  │               using IrisOutput schema
  │                               │
  │  ◄─────────────────────────   │
  │  Status: 200                  │
  │  {"species": "setosa",        │
  │   "confidence": 1.0}          │
```

## Complete Project

```
mlapi/
├── iris_model.joblib       # Trained model (generated by train.py)
├── train.py                # Run once to create the model
├── model.py                # IrisClassifier class with predict methods
├── schemas.py              # Pydantic input/output schemas
├── main.py                 # FastAPI app with 4 endpoints
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_model.py       # 4 tests for the model directly
    └── test_api.py         # 12 tests for the API endpoints
```
