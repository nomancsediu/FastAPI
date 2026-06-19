# CRUD Operations

## What is CRUD?

CRUD stands for Create, Read, Update, Delete — the four basic operations for managing data in any application. RESTful APIs map these operations to HTTP methods: POST for Create, GET for Read, PUT/PATCH for Update, and DELETE for Delete. Building a complete CRUD API is a fundamental skill for any API developer.

```text
  +---------------------+          +------------+
  |  POST   /items/     +--Create->+            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  GET    /items/     +--Read---->  Database  |
  +---------------------+          |            |
  +---------------------+          |            |
  |  GET    /items/{id} +--Read---->            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  PUT    /items/{id} +-Update-->+            |
  +---------------------+          |            |
  +---------------------+          |            |
  |  DELETE /items/{id} +-Delete-->+            |
  +---------------------+          +------------+
```

## A Complete CRUD Example

Here is a complete CRUD API for managing items:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory database (replace with a real database in production)
db = []

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

# CREATE
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    item_dict = item.model_dump()
    item_dict["id"] = len(db) + 1
    db.append(item_dict)
    return item_dict

# READ (all items)
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):
    return db[skip : skip + limit]

# READ (single item)
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in db:
        if item["id"] == item_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, item_update: ItemUpdate):
    for item in db:
        if item["id"] == item_id:
            update_data = item_update.model_dump(exclude_unset=True)
            item.update(update_data)
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )

# DELETE
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for i, item in enumerate(db):
        if item["id"] == item_id:
            db.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with id {item_id} not found"
    )
```

## Form Data and File Uploads

FastAPI also supports form data and file uploads, which are essential for many ML applications:

```python
from fastapi import FastAPI, UploadFile, File, Form

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }

@app.post("/predict-image/")
async def predict_image(
    file: UploadFile = File(...),
    model_name: str = Form(default="resnet50")
):
    image_bytes = await file.read()
    prediction = "cat"
    confidence = 0.95
    return {"prediction": prediction, "confidence": confidence, "model": model_name}
```
