# CRUD Operations

CRUD stands for **C**reate, **R**ead, **U**pdate, **D**elete. These are the four basic operations for managing data. In REST APIs, they map to HTTP methods like this:

| Operation | HTTP Method | URL |
|-----------|-------------|-----|
| Create | POST | `/items/` |
| Read all | GET | `/items/` |
| Read one | GET | `/items/1` |
| Update | PUT | `/items/1` |
| Delete | DELETE | `/items/1` |

Instead of putting everything in one file, let's organize our code into separate files. Each file has one job — this makes the project easier to understand and maintain.

## Step 1: Create models.py

First, create a file for our data models:

```python
# models.py
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
```

`Item` is for creating. `ItemUpdate` is for updating (all fields optional).

## Step 2: Create database.py

Create a file for data storage:

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


def update_item(item_id: int, name=None, price=None) -> dict | None:
    item = get_item(item_id)
    if item is None:
        return None
    if name is not None:
        item["name"] = name
    if price is not None:
        item["price"] = price
    return item


def delete_item(item_id: int) -> bool:
    for i, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(i)
            return True
    return False
```

Each function does one thing. The `main.py` file will just call these functions.

## Step 3: Create main.py

Now create the FastAPI app that uses models and database:

```python
# main.py
from fastapi import FastAPI, HTTPException
from models import Item, ItemUpdate
from database import (
    create_item,
    get_all_items,
    get_item,
    update_item,
    delete_item,
)

app = FastAPI()


@app.post("/items/", status_code=201)
def create(data: Item):
    return create_item(data)


@app.get("/items/")
def list_all():
    return get_all_items()


@app.get("/items/{item_id}")
def get_one(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
def update_one(item_id: int, data: ItemUpdate):
    item = update_item(item_id, data.name, data.price)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_one(item_id: int):
    if not delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return
```

## Step 4: Run and Test

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` and test all 5 endpoints.

## Why This Organization?

| File | Job |
|------|-----|
| `models.py` | Defines what data looks like |
| `database.py` | Stores and manages data |
| `main.py` | Handles HTTP requests |

This is called **separation of concerns**. Each file has one clear job. When we upgrade to a real database in Chapter 4, we only need to change `database.py`.

## What You Built

```
fastapi-crud/
├── main.py         # 5 endpoints
├── models.py       # Pydantic models
├── database.py     # In-memory storage
├── requirements.txt
```
