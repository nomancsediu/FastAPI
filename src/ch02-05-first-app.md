# First App Using FastAPI

## Hello World

Create a file called `main.py` with the following content:

```python
from fastapi import FastAPI

app = FastAPI(title="My First API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

Run it with:

```bash
uvicorn main:app --reload
```

Now visit `http://127.0.0.1:8000/docs` to see the interactive Swagger UI documentation. You will see all your endpoints listed, with the ability to try them out directly from the browser.

## Understanding What Just Happened

- `FastAPI()` creates the application instance. The `title` and `version` parameters are used in the auto-generated documentation.
- `@app.get("/")` is a decorator that registers a GET endpoint at the root URL path.
- `def read_root():` is the handler function that gets called when someone visits the root URL.
- `item_id: int` tells FastAPI to expect an integer in the URL path and automatically convert/validate it.
- `q: str = None` defines an optional query parameter. FastAPI will look for `?q=value` in the URL.

## Path Parameters and Query Parameters

FastAPI makes it easy to work with both path parameters (embedded in the URL) and query parameters (appended after `?` in the URL):

```python
from fastapi import FastAPI

app = FastAPI()

# Path parameter: /users/42
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# Query parameters: /items/?skip=10&limit=5
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Both path and query: /users/42/posts?published=true
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, published: bool = False):
    return {"user_id": user_id, "published": published}
```
