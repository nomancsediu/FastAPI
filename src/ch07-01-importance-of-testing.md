# Importance of Testing

## Why Testing Matters for ML APIs

ML APIs have failure modes that regular APIs don't:

| Failure Mode | What Happens | Detection |
|-------------|-------------|-----------|
| **Model not loaded** | All predictions fail with 500 | Easy (obvious crash) |
| **Wrong input shape** | Garbage prediction, random output | Hard (looks valid) |
| **Data drift** | Model accuracy degrades over time | Very hard (needs monitoring) |
| **Feature encoding mismatch** | Wrong categories mapped | Silent failure |
| **Security hole** | Unauthorized access to predictions | Critical risk |

Without tests, these issues can go undetected. A comprehensive test suite catches them before they reach production.

## What We'll Test in Each Project

### fastapi-crud/ Tests

| Test Type | What It Covers | File |
|-----------|---------------|------|
| **Unit** | Pydantic schema validation | `test_schemas.py` |
| **Unit** | CRUD database operations | `test_crud.py` |
| **Integration** | All API endpoints | `test_main.py` |
| **Integration** | Auth flow (register, login, protected routes) | `test_auth.py` |

### ml-serving-api/ Tests

| Test Type | What It Covers | File |
|-----------|---------------|------|
| **Unit** | Input/output schema validation | `test_schemas.py` |
| **Unit** | Predictor logic with mocked model | `test_predict.py` |
| **Integration** | Prediction endpoints | `test_main.py` |
| **Batch** | Batch and CSV upload endpoints | `test_batch.py` |
