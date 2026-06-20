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

Without tests, these issues can go undetected. A comprehensive test suite catches
them before they reach production.

## What We'll Test

| Test Type | What It Covers | File |
|-----------|---------------|------|
| **Unit** | Model prediction logic | `tests/test_model.py` |
| **Integration** | All API endpoints (with auth) | `tests/test_api.py` |
| **Auth** | API key validation, JWT register/login | `tests/test_api.py` |
| **Validation** | Input schema — wrong features, types, missing fields | `tests/test_api.py` |
| **Error handling** | 401 without auth, 422 bad input, 500 model crash | `tests/test_api.py` |
