# Asynchronous Programming

## Why Async Matters for ML APIs

Machine learning APIs often perform operations that are I/O-bound rather than CPU-bound. Reading image files from disk, querying databases, making requests to external APIs, and even loading model weights are all I/O operations. Traditional synchronous code blocks the entire server while waiting for these operations to complete, meaning the server cannot handle other requests during that time. Asynchronous code, on the other hand, allows the server to switch to handling other requests while waiting for I/O operations to finish, dramatically improving throughput under load.

## Defining Async Endpoints

```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/sync-predict/")
def sync_predict(text: str):
    # This blocks the server while "processing"
    result = expensive_ml_operation(text)
    return {"result": result}

@app.get("/async-predict/")
async def async_predict(text: str):
    # This does NOT block - server can handle other requests
    result = await asyncio.to_thread(expensive_ml_operation, text)
    return {"result": result}
```

## When to Use Async vs Sync

Use `async def` for endpoints that perform I/O operations (database queries, file reads, HTTP calls). Use regular `def` for endpoints that perform CPU-bound work (model inference with NumPy/PyTorch, complex computations). FastAPI automatically runs `def` endpoints in an external threadpool, so they do not block the event loop. The rule of thumb: if the operation involves waiting (I/O), use `async`; if the operation involves heavy computation (CPU), use `def`.

```text
  +------------------+
  |  Request Arrives |
  +--------+---------+
           |
           v
  +--------+---------+
  |  Operation Type? |
  +--+------------+--+
     |            |
  I/O Bound    CPU Bound
  DB/File/HTTP NumPy/PyTorch
     |            |
     v            v
  +-----------+ +--------------------+
  | async def | | def                |
  | handler   | | runs in threadpool |
  +-----------+ +--------------------+
     |            |
     v            v
  +-----------+ +--------------------+
  | await I/O | | blocks threadpool  |
  | event     | | event loop free    |
  | loop free | |                    |
  +-----------+ +--------------------+
     |            |
     +-----+------+
           |
           v
  +--------+---------+
  |    Response      |
  +------------------+
```

```python
import asyncio
import time
from fastapi import FastAPI

app = FastAPI()

async def fetch_data_from_db(query: str):
    await asyncio.sleep(1)  # Simulates I/O wait
    return {"data": "result from db"}

def run_model_inference(data: dict):
    time.sleep(0.5)  # Simulates CPU work
    return {"prediction": "cat", "confidence": 0.95}

@app.post("/full-pipeline/")
async def full_pipeline():
    db_result = await fetch_data_from_db("SELECT * FROM items")
    model_result = await asyncio.to_thread(run_model_inference, db_result)
    return {"db_data": db_result, "ml_result": model_result}
```
