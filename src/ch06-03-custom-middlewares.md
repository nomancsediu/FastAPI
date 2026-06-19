# Custom Middlewares

## Building a Custom Middleware

You can create custom middleware for logging, timing, rate limiting, or any other cross-cutting concern:

```python
import time
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    return response
```

## Rate Limiting Middleware

```python
from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
import time

app = FastAPI()

request_counts = defaultdict(list)
RATE_LIMIT = 100
WINDOW_SECONDS = 60

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()

    request_counts[client_ip] = [
        t for t in request_counts[client_ip] if now - t < WINDOW_SECONDS
    ]

    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    request_counts[client_ip].append(now)
    response = await call_next(request)
    return response
```
