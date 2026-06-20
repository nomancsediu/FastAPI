# Environment Variables & Configuration

Never hardcode paths, API keys, or secrets in your Python files. If you commit them
to git, anyone with repo access sees them.

For an ML API, the most important thing to externalize is the **model path** —
so you can switch models without changing code.

## What You'll Add

| Action | File | Details |
|--------|------|---------|
| Create | `mlapi/.env` | Store secrets as key=value pairs |
| Create | `mlapi/config.py` | Load secrets from `.env` so Python can import them |
| Update | `mlapi/model.py` | Read `MODEL_PATH` from config instead of hardcoding |

---

## Step 1: Create `.env`

Create `mlapi/.env` with this content:

```bash
MODEL_PATH=iris_model.joblib
API_KEY=ml-inference-key-123
SECRET_KEY=jwt-secret-change-in-production
DATABASE_URL=sqlite:///./users.db
```

> **Important:** Add `.env` to `.gitignore` so you never commit secrets.

---

## Step 2: Create `config.py`

Create `mlapi/config.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "iris_model.joblib")
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")
```

The second argument to `os.getenv` is a default value — if `.env` is missing,
it falls back to the hardcoded path so your project still works.

Install the package:

```bash
pip install python-dotenv
```

---

## Step 3: Update `model.py`

Open `mlapi/model.py`. Currently it loads the model with a hardcoded path.
Change the `IrisClassifier.__init__` default to use `config.MODEL_PATH`:

**Before:**

```python
def __init__(self, model_path: str = "iris_model.joblib"):
```

**After:**

```python
from config import MODEL_PATH

class IrisClassifier:
    def __init__(self, model_path: str = MODEL_PATH):
```

Now the model path is controlled by your `.env` file. Change it without touching code.

---

## Test It

```bash
uvicorn main:app --reload
```

If the server starts and predictions still work, config is set up correctly:

```bash
curl http://localhost:8000/health
```

---

## Project Structure Now

```
mlapi/
├── train.py
├── model.py           # Updated — reads MODEL_PATH from config
├── schemas.py
├── main.py
├── config.py           # NEW — loads secrets from .env
├── .env                # NEW — your secrets (git-ignored)
├── iris_model.joblib
├── requirements.txt    # + python-dotenv
└── tests/
```

Config is ready. Next we'll add **CORS middleware** so a frontend dashboard can
call your prediction endpoint.
