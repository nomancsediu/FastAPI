# API Key Authentication

API keys are the simplest and most common way to secure ML APIs. A client (another
service, a script, a dashboard) sends a key in the header, and your server checks
if it's valid.

## What You'll Add

| Action | File | Where |
|--------|------|-------|
| Create | `mlapi/auth.py` | New file — API key verification function |
| Edit | `mlapi/main.py` | Add import at top **+** protect `/predict` and `/predict/batch` |

---

## Step 1: Create `auth.py`

Create `mlapi/auth.py`:

```python
from fastapi import Header, HTTPException
from config import API_KEY

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
```

This function reads the `X-API-Key` header from every request and compares it
against the value in your `.env` file.

---

## Step 2: Protect the Prediction Endpoints in `main.py`

### 2a — Add the import

Open `mlapi/main.py`. Add this import near the top:

```python
from auth import verify_api_key
from fastapi import Depends  # Add Depends if not already imported
```

### 2b — Protect `/predict`

Find the `predict_iris` function. Add `api_key: str = Depends(verify_api_key)`:

```python
@app.post("/predict", response_model=IrisOutput)
def predict_iris(
    data: IrisInput,
    api_key: str = Depends(verify_api_key),   # ← add this
):
    try:
        return classifier.predict(data.features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2c — Protect `/predict/batch`

Do the same for the batch endpoint:

```python
@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(
    data: BatchInput,
    api_key: str = Depends(verify_api_key),   # ← add this
):
    ...
```

Now both prediction endpoints require a valid API key. The `/` and `/health`
endpoints stay public.

---

## Test It

```bash
# Without key — 401 error
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

# With the correct key — works!
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ml-inference-key-123" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

## Why API Keys for ML?

| Feature | Benefit |
|---------|---------|
| Simple | One header, no login flow needed |
| Machine-to-machine | Perfect for service-to-service calls |
| Track usage | Give each client a unique key, monitor per-key |
| Revoke instantly | Delete a key, access is blocked |

In the next section we'll add **JWT authentication** so users can log in and get
temporary tokens.
