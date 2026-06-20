# Creating Your First API

Let's build your first API. We'll start simple and organize our code properly from the beginning.

## Step 1: Create a Project Folder

Open your terminal:

```bash
mkdir fastapi-crud
cd fastapi-crud
```

Create `requirements.txt`:

```bash
echo "fastapi
uvicorn" > requirements.txt
```

Install:

```bash
pip install -r requirements.txt
```

## Step 2: Hello World

Create `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

Run:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` — you see `{"message": "Hello World"}`.

Open `http://127.0.0.1:8000/docs` — this is Swagger UI. FastAPI generates this documentation automatically.

## Step 3: Path Parameters

Add this to `main.py`:

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

Visit `http://127.0.0.1:8000/items/42` → `{"item_id": 42}`

Try `http://127.0.0.1:8000/items/hello` — FastAPI returns an error because `item_id` expects an integer. This is **automatic type validation**.

## Step 4: Query Parameters

Add to `main.py`:

```python
@app.get("/search/")
def search(q: str = "", page: int = 1):
    return {"query": q, "page": page}
```

Test:
- `/search/?q=python&page=2` → `{"query": "python", "page": 2}`
- `/search/` → `{"query": "", "page": 1}` (defaults used)

## Step 5: POST + Pydantic Model (create models.py)

Now we need to accept data from users. For POST, data goes in the **request body**.

First, create `models.py` for our data definitions:

```bash
touch models.py
```

```python
# models.py
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
```

This `Item` class is a **Pydantic model**. It tells FastAPI what data to expect.

Now update `main.py` to import and use it:

```python
from fastapi import FastAPI
from models import Item

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

Test in Swagger UI (`/docs`). Send:

```json
{"name": "Laptop", "price": 999.99}
```

You get back: `{"name": "Laptop", "price": 999.99}`

If you send `{"price": "free"}`, FastAPI returns a **422 error** — `price` must be a number, not text.

## Step 6: In-Memory Storage (create database.py)

Right now data is not stored anywhere. Let's add storage.

Create `database.py`:

```bash
touch database.py
```

```python
# database.py
from models import Item


items = []
next_id = 1


def create_item(item: Item) -> dict:
    global next_id
    new_item = {"id": next_id, "name": item.name, "price": item.price}
    items.append(new_item)
    next_id += 1
    return new_item


def get_all_items() -> list:
    return items


def get_item(item_id: int) -> dict | None:
    for item in items:
        if item["id"] == item_id:
            return item
    return None
```

Now update `main.py` to use `database.py`:

```python
from fastapi import FastAPI
from models import Item
from database import create_item, get_all_items, get_item

app = FastAPI()


@app.post("/items/")
def create(data: Item):
    return create_item(data)


@app.get("/items/")
def list_all():
    return get_all_items()


@app.get("/items/{item_id}")
def get_one(item_id: int):
    item = get_item(item_id)
    if item is None:
        return {"error": "Item not found"}
    return item
```

Test it:

1. `POST /items/` with `{"name": "Laptop", "price": 999}` → `{"id": 1, "name": "Laptop", "price": 999}`
2. `POST /items/` with `{"name": "Mouse", "price": 29}` → `{"id": 2, ...}`
3. `GET /items/` → shows both items
4. `GET /items/1` → shows the laptop

## Why Three Files?

| File | Job |
|------|-----|
| `models.py` | What data looks like |
| `database.py` | How data is stored |
| `main.py` | HTTP routes only |

Each file has one job. When we upgrade to a real database in Chapter 4, we only change `database.py` — `main.py` stays almost the same.

## What You Learned

- Path parameters (`/items/{id}`)
- Query parameters (`?q=hello`)
- POST with Pydantic models (in `models.py`)
- Storage in separate file (`database.py`)
- Clean project organization from the start

Your project:

```
fastapi-crud/
├── main.py
├── models.py
├── database.py
├── requirements.txt
```

In the next section, we'll add Update and Delete to make a complete CRUD API.
