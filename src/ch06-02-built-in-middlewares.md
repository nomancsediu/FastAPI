# Built-in Middlewares

## CORS Middleware

CORS (Cross-Origin Resource Sharing) is a security feature built into browsers that prevents web pages from making requests to a different domain than the one that served the page. When building an ML API that will be called from a web front end, you need to configure CORS to allow requests from your front end's domain:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For development, you can use `allow_origins=["*"]` to allow all origins, but for production, you should always specify the exact allowed origins for security.
