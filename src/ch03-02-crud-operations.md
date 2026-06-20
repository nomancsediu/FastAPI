# CRUD Operations

CRUD stands for **C**reate, **R**ead, **U**pdate, **D**elete. In REST APIs, they
map to HTTP methods like this:

| Operation | HTTP Method | URL |
|-----------|-------------|-----|
| Create | POST | `/items/` |
| Read all | GET | `/items/` |
| Read one | GET | `/items/1` |
| Update | PUT | `/items/1` |
| Delete | DELETE | `/items/1` |

From the previous section, your project already has Create and Read. Now we'll add
Update and Delete.

---

## Step 1: Add `ItemUpdate` to `models.py`

The update endpoint needs a model where all fields are optional (the client only
sends the fields they want to change). Open `fastapi-crud/models.py` and add this
at the bottom:

```python
class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
```

Now `models.py` has both `Item` (for create) and `ItemUpdate` (for update).

---

## Step 2: Add Update + Delete to `database.py`

> **Python version note:** The `dict | None` syntax below requires Python 3.10+.
> If you're on Python 3.9, use `Optional[dict]` instead (`from typing import Optional`).

Open `fastapi-crud/database.py`. Add these two functions at the bottom:

```python
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

Now `database.py` has all five operations: create, get_all, get_one, update, delete.

---

## Step 3: Add PUT + DELETE Routes to `main.py`

Open `fastapi-crud/main.py`. Add these imports at the top:

```python
from models import ItemUpdate
from database import update_item, delete_item
```

Then add these routes at the bottom (before `@app.get("/search/")`):

```python
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

You also need to add the import for `HTTPException`. Update the import line at the
top of `main.py`:

```python
from fastapi import FastAPI, HTTPException
```

---

## Step 4: Run and Test

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` and test all 5 endpoints:

1. **POST /items/** — create an item
2. **GET /items/** — list all
3. **GET /items/1** — get one
4. **PUT /items/1** — update an item
5. **DELETE /items/1** — delete an item

---

## Your Complete Project Now

```
fastapi-crud/
├── main.py           # 5 endpoints (all CRUD)
├── models.py         # Pydantic models (Item, ItemUpdate)
├── database.py       # In-memory storage (5 functions)
├── requirements.txt
```

Each file has one job. When we upgrade to a real database in Chapter 4, we only
change `database.py` — `main.py` stays almost the same.
