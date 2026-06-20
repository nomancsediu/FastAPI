# Machine Learning API

We build a separate project: an API that classifies iris flowers using a real sklearn model.

```
mlapi/
├── train.py          # Train model on iris data, save with joblib
├── main.py           # FastAPI app (loads model, serves predictions)
├── requirements.txt
```

| Section | What You'll Learn |
|---------|------------------|
| 5.1 | What model serialization means |
| 5.2 | Pickle / Joblib with iris examples |
| 5.3 | Input/output schemas for ML |
| 5.4 | Building the iris classification API |
| 5.5 | Batch predictions |
