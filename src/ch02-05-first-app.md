# First App Using FastAPI

Let's write our first FastAPI app inside the `fastapi-crud/` project we created
in the previous section. This same project will grow into a full CRUD API in
Chapter 3.

## Step 1: Create main.py

Inside `fastapi-crud/`, create `main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="CRUD API", version="1.0")


@app.get("/")
def home():
    return {"message": "Hello World"}
```

## Step 2: Run It

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` — you see `{"message": "Hello World"}`.

Open `http://127.0.0.1:8000/docs` — this is **Swagger UI**, auto-generated
documentation. You can test your endpoints right from the browser.

---

## Step 3: Path Parameters

Add a path parameter endpoint. Values in `{curly braces}` are captured from the URL:

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

Visit `http://127.0.0.1:8000/items/42` → `{"item_id": 42}`

Try `http://127.0.0.1:8000/items/hello` — FastAPI returns an error because
`item_id` expects an integer. This is **automatic type validation**.

---

## Step 4: Query Parameters

Add a search endpoint with optional query parameters:

```python
@app.get("/search/")
def search(q: str = "", page: int = 1):
    return {"query": q, "page": page}
```

Test it:
- `/search/?q=python&page=2` → `{"query": "python", "page": 2}`
- `/search/` → `{"query": "", "page": 1}` (defaults used)

---

## Your `main.py` Now

```python
from fastapi import FastAPI

app = FastAPI(title="CRUD API", version="1.0")


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}


@app.get("/search/")
def search(q: str = "", page: int = 1):
    return {"query": q, "page": page}
```

---

## What You Learned

- `@app.get()` registers a GET endpoint
- Path parameters (`/items/{id}`) are captured from the URL
- Type hints (`item_id: int`) give automatic validation
- Query parameters (`q: str = ""`) are optional with defaults
- `/docs` gives you interactive Swagger UI

This `fastapi-crud/` project is ready. In **Chapter 3** we'll add POST, PUT, DELETE
and build a complete CRUD API.
