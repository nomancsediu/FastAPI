# Async Programming

Async (short for asynchronous) lets your API handle many requests at the same time instead of one by one.

## The Problem

Imagine your API needs to read a file or query a database before responding. While waiting, the server sits idle — it could be handling other requests.

**Synchronous (slow):**
```python
import time

@app.get("/slow")
def slow_endpoint():
    time.sleep(5)  # Server waits 5 seconds, can't do anything else
    return {"done": True}
```

**Asynchronous (fast):**
```python
import asyncio

@app.get("/fast")
async def fast_endpoint():
    await asyncio.sleep(5)  # Server handles other requests while waiting
    return {"done": True}
```

With `async`, your server can handle 100 requests during those 5 seconds instead of just 1.

## When to Use Async

| Use `def` (normal) | Use `async def` |
|--------------------|-----------------|
| Simple calculations | Reading files |
| Model predictions | Database queries |
| Math operations | Downloading data |
| | Waiting for APIs |

## Simple Rule

- **CPU work** (math, prediction) → use `def`
- **Waiting** (files, database, network) → use `async def`

Here's a realistic example for ML:

```python
import asyncio
import time

def predict(text: str):
    """This is CPU work - runs in background thread."""
    time.sleep(0.5)
    return {"label": "positive", "score": 0.95}

def preprocess(text: str):
    """This is also CPU work."""
    time.sleep(0.1)
    return text.lower()

@app.post("/predict")
async def predict_endpoint(text: str):
    cleaned = await asyncio.to_thread(preprocess, text)
    result = await asyncio.to_thread(predict, cleaned)
    return result
```

`asyncio.to_thread()` runs CPU work in a background thread so it doesn't block the server.

## What You Need to Know

- `async def` makes your endpoint **non-blocking**
- Use `await` for operations that take time
- For ML predictions, use `asyncio.to_thread()`
- FastAPI handles the complexity — just use `async def` when waiting
