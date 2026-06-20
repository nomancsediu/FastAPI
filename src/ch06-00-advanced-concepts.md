# Making Your ML API Production-Ready

Your `mlapi/` project from Chapter 5 has a working prediction endpoint. Now we'll
add real-world features every production ML API needs.

## Your Starting Project

Before we begin, this is what `mlapi/` looks like right now:

```text
mlapi/
├── train.py              # Train iris model, saves iris_model.joblib
├── model.py              # IrisClassifier — load model, predict, predict_batch
├── schemas.py            # Pydantic schemas (IrisInput, IrisOutput, etc.)
├── main.py               # FastAPI with 4 endpoints: /, /predict, /predict/batch, /health
├── iris_model.joblib     # Trained model file (run train.py to generate)
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_model.py
    └── test_api.py
```

Each section below adds or modifies files inside this `mlapi/` folder. You'll always
know exactly which file to open and where to paste the code.

## Roadmap

| Section | Topic | Files You'll Change |
|---------|-------|---------------------|
| **6.1** | Environment Variables & Config | Create `.env`, `config.py`; edit `model.py` |
| **6.2** | CORS Middleware | Edit `main.py` |
| **6.3** | API Key Authentication | Create `auth.py`; edit `main.py` |
| **6.4** | JWT Authentication | Edit `auth.py`; create `database.py`, `models.py`; edit `main.py` |
| **6.5** | Best Practices | Edit `main.py` — logging, status codes, error handling |

## Final Project Preview

After all five sections, your project will look like this:

```text
mlapi/
├── train.py              # Train iris model
├── model.py              # IrisClassifier — reads model path from config
├── schemas.py            # Pydantic schemas
├── database.py           # NEW — SQLite session (for JWT users)
├── models.py             # NEW — UserDB table
├── auth.py               # NEW — API key + JWT auth logic
├── config.py             # NEW — loads secrets from .env
├── .env                  # NEW — secrets (git-ignored)
├── main.py               # Updated — CORS, auth, logging
├── iris_model.joblib
├── requirements.txt      # + python-dotenv, python-jose, passlib, bcrypt
└── tests/
    ├── __init__.py
    ├── test_model.py
    └── test_api.py
```

Start with **Section 6.1** — environment variables are the foundation for everything.
