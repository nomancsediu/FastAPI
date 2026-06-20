# Best Practices

A few small additions that make a big difference when your ML API hits production.

---

## 1. Add Logging

Log every prediction request so you can debug issues and audit usage.

Open `mlapi/main.py` and add at the **top** (before anything else):

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Then log inside your prediction routes:

```python
@app.post("/predict", response_model=IrisOutput)
def predict_iris(
    data: IrisInput,
    api_key: str = Depends(verify_api_key),
):
    logger.info(f"Predict: {data.features}")           # ← add this
    try:
        result = classifier.predict(data.features)
        logger.info(f"Result: {result}")               # ← add this
        return result
    except Exception as e:
        logger.error(f"Prediction failed: {e}")         # ← add this
        raise HTTPException(status_code=500, detail=str(e))
```

Every prediction is now logged with input and output:

```
INFO: Predict: [5.1, 3.5, 1.4, 0.2]
INFO: Result: {'species': 'setosa', 'confidence': 1.0}
```

---

## 2. Use Correct HTTP Status Codes

| Situation | Code | Meaning |
|-----------|------|---------|
| Prediction successful | `200` | OK |
| Prediction created resource | `201` | Created |
| Bad input (wrong feature count) | `422` | Unprocessable Entity |
| Invalid API key or JWT token | `401` | Unauthorized |
| Model crashed or not loaded | `500` | Internal Server Error |

FastAPI sets most of these automatically (Pydantic validation → 422, auth failures → 401).
The `try/except` around model calls returns a clean 500 instead of crashing.

---

## 3. Model-Specific Best Practices

| Practice | Why |
|----------|-----|
| Load model once at startup | The `classifier = IrisClassifier()` line runs on import — model stays in memory |
| Catch model exceptions | `try/except` returns 500 with a message instead of crashing the server |
| Validate input before model | Pydantic schemas reject bad data before it reaches your model |
| Log input and output | Audit trail for debugging incorrect predictions |
| Keep model path in env vars | Swap models without redeploying code |

---

## 4. One File = One Responsibility

```
main.py           → Routes and app setup
model.py          → ML model loading and prediction logic
schemas.py        → Input/output data validation
auth.py           → Authentication (API key + JWT)
database.py       → Database connection (for user storage)
models.py         → Database table definitions
config.py         → Environment variables
```

Need to change the model? Touch only `model.py`. Need to change auth? Only `auth.py`.

---

## Your Final Project

```
mlapi/
├── train.py              # Train iris model
├── model.py              # IrisClassifier — model path from config
├── schemas.py            # Pydantic input/output schemas
├── database.py           # SQLAlchemy engine + session
├── models.py             # UserDB table
├── auth.py               # API key + JWT auth
├── config.py             # Environment variables
├── .env                  # Secrets (git-ignored)
├── main.py               # App with CORS, auth, logging, 4 endpoints
├── iris_model.joblib     # Trained model
├── users.db              # SQLite database (auto-created)
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_model.py
    └── test_api.py
```

Run it:

```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` to test every endpoint with Swagger UI.

In the next chapter, you'll learn how to **test** everything with pytest.
