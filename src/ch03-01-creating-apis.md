# Creating APIs

## Request Body with Pydantic Models

For endpoints that accept data in the request body (POST, PUT, PATCH), you define Pydantic models to describe the expected data structure:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be positive")
    tax: Optional[float] = None
    tags: List[str] = []

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "total_price": item.price + (item.tax or 0)}
```

Pydantic's `Field` allows you to add constraints like `gt=0` (greater than 0), `le=100` (less than or equal to 100), `min_length=1`, `regex="^pattern$"`, and more. If a client sends invalid data, FastAPI automatically returns a 422 error with details about which fields failed validation.

## Response Models

You can also define the response structure using Pydantic models. This filters the output to only include the specified fields:

```python
from pydantic import BaseModel
from typing import Optional

class ItemResponse(BaseModel):
    name: str
    price: float

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    # Business logic here
    return {"name": item.name, "price": item.price, "description": item.description}
```

Even though the function returns a dictionary with a `description` field, the response model filters it out, so the client only receives `name` and `price`.

## Status Codes

You can explicitly set the status code for each endpoint:

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    # Create item in database
    return {"message": "Item created successfully", "item": item}
```
