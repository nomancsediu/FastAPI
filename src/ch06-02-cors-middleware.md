# CORS Middleware

If you build a dashboard or website that calls your `/predict` endpoint from the
browser, the browser will block the request unless you enable CORS.

CORS = Cross-Origin Resource Sharing. It's a browser security feature.

## What You'll Add

| Action | File | Where |
|--------|------|-------|
| Edit | `mlapi/main.py` | Add import at top **+** add middleware right after `app = FastAPI()` |

---

## Step 1: Add the Import

Open `mlapi/main.py`. Near the top with the other imports, add:

```python
from fastapi.middleware.cors import CORSMiddleware
```

---

## Step 2: Register the Middleware

Find the line `app = FastAPI(...)`. Right after it, add this block:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development only)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
```

Your `main.py` should now look like this around the app creation:

```python
app = FastAPI(title="Iris Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## For Production

When you deploy, restrict CORS to your real dashboard domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mydashboard.com"],  # Only this domain
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
)
```

---

## Test It

Restart the server. CORS doesn't change any endpoint behavior — it only adds
HTTP headers to responses:

```bash
curl -I http://localhost:8000/health 2>&1 | grep -i access-control
```

If you see `access-control-allow-origin: *`, CORS is active.

---

## Project Structure Now

```
mlapi/
├── train.py
├── model.py
├── schemas.py
├── main.py            # Updated — CORS middleware added
├── config.py
├── .env
├── iris_model.joblib
├── requirements.txt
└── tests/
```

Next we'll secure your ML API with **API Key Authentication**.
