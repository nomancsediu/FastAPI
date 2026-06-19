# Serving ML Models

## Architecture Overview

Serving an ML model through FastAPI involves several components working together:

```text
  +----------+
  |  Client  |
  +----+-----+
       | HTTP POST + JSON Body
       v
  +----+-------------+
  |  FastAPI         |
  |  Endpoint        |
  +----+-------------+
       |
       v
  +----+-------------+
  |  Pydantic        |
  |  Input Validation|
  +----+----+--------+
       |    |
     Valid  Invalid
       |    |
       v    v
  +--------+  +------------------+
  | Input  |  | 422 Validation   |
  | Preproc|  | Error            |
  +----+---+  +------------------+
       |
       v
  +----+-------------+
  |  ML Model        |
  |  Inference       |
  +----+-------------+
       |
       v
  +----+-------------+
  |  Output          |
  |  Postprocessing  |
  +----+-------------+
       |
       v
  +----+-------------+
  |  Pydantic        |
  |  Response Model  |
  +----+-------------+
       | JSON Response
       v
  +----+-----+
  |  Client  |
  +----------+
```

1. **Model loading**: Load the serialized model into memory when the API starts.
2. **Input preprocessing**: Transform the incoming API request into the format the model expects.
3. **Model inference**: Run the model on the preprocessed input to get predictions.
4. **Output postprocessing**: Transform the model's output into the API response format.
5. **Response**: Return the prediction and metadata to the client.

## train.py — Training the Model

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.4f}")

# Save model
joblib.dump(model, "iris_model.joblib")
print("Model saved to iris_model.joblib")
```

## predict.py — Prediction Logic

```python
import joblib
import numpy as np
import time

class IrisPredictor:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.class_names = ["setosa", "versicolor", "virginica"]

    def predict(self, features: list) -> dict:
        start_time = time.time()
        input_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(input_array)[0]
        probabilities = self.model.predict_proba(input_array)[0]
        confidence = float(probabilities.max())
        inference_time = (time.time() - start_time) * 1000

        return {
            "prediction": self.class_names[prediction],
            "confidence": confidence,
            "class_probabilities": {
                name: float(prob)
                for name, prob in zip(self.class_names, probabilities)
            },
            "inference_time_ms": round(inference_time, 2)
        }

# Singleton instance
predictor = IrisPredictor("iris_model.joblib")
```

## main.py — The FastAPI Application

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import predict

app = FastAPI(
    title="Iris Classification API",
    description="A production-ready API for iris flower classification",
    version="1.0"
)

class IrisInput(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Sepal length, sepal width, petal length, petal width"
    )

class IrisOutput(BaseModel):
    prediction: str
    confidence: float
    class_probabilities: dict
    inference_time_ms: float

@app.post("/predict", response_model=IrisOutput)
def predict_iris(input_data: IrisInput):
    try:
        result = predict.predictor.predict(input_data.features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": predict.predictor.model is not None}
```
