# CORS — Let Web Apps Use Your API

If you build a website (React, Vue, etc.) that calls your API, the browser will block it unless you enable CORS.

CORS = Cross-Origin Resource Sharing. It's a browser security feature.

## Add CORS to Your API

In `main.py`, add this:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development only)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
```

Put this line right after `app = FastAPI()`.

## For Production

In production, tell CORS which website is allowed:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],  # Only this site
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization"],
)
```

That's it. One code block and your API works with web browsers.
