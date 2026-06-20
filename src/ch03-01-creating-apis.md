# Creating Your First API

We already have `fastapi-crud/` from Chapter 2 with a working `main.py`. Now we'll
add POST endpoints, Pydantic models, and a storage layer.

---

## Step 1: Create `models.py`

Data definitions go in their own file. Create `models.py`:

```python
# models.py
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
```

This `Item` class is a **Pydantic model**. It tells FastAPI what data to expect
when a client sends a POST request.

---

## Step 2: Create `database.py`

Storage logic goes in its own file. Create `database.py`:

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

Each function has one job. The API routes (in `main.py`) will just call these.

---

## Step 3: Connect Everything in `main.py`

Now update `main.py` to import and use the new files:

```python
from fastapi import FastAPI
from models import Item
from database import create_item, get_all_items, get_item

app = FastAPI(title="CRUD API", version="1.0")


@app.get("/")
def home():
    return {"message": "Hello World"}


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


@app.get("/search/")
def search(q: str = "", page: int = 1):
    return {"query": q, "page": page}
```

---

## Step 4: Test It

Run the server:

```bash
uvicorn main:app --reload
```

Open Swagger UI at `http://127.0.0.1:8000/docs` and test:

1. **POST /items/** with `{"name": "Laptop", "price": 999}` → gets back the saved item with an `id`
2. **POST /items/** with `{"name": "Mouse", "price": 29}` → second item
3. **GET /items/** → shows both items
4. **GET /items/1** → shows the laptop

Test validation: send `{"price": "free"}` to POST /items/ — you get a **422 error**
because `price` must be a number.

---

## Why Three Files?

| File | Job |
|------|-----|
| `models.py` | Defines what data looks like |
| `database.py` | How data is stored |
| `main.py` | HTTP routes only |

Each file has one job. When we upgrade to a real database in Chapter 4, we only
change `database.py` — `main.py` stays almost the same.

---

## Your Project Now

```
fastapi-crud/
├── main.py           # 5 endpoints (GET /, POST /items, GET /items, GET /items/{id}, GET /search/)
├── models.py         # NEW — Item Pydantic model
├── database.py       # NEW — in-memory storage functions
├── requirements.txt
└── venv/
```

Next we'll add **Update and Delete** to complete the CRUD operations.
