# Validation and Error Handling

FastAPI automatically checks that the data you receive is correct. If something is wrong, it returns a helpful error message.

## Built-in Validation

Let's add some rules to our `Item` model:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0, le=10000)
```

Now if someone tries to create an item with `price=0` or `name=""`, FastAPI returns a **422 error** with a message explaining what's wrong.

Try it:

```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "", "price": 0}'
```

You'll get back:

```json
{
  "detail": [
    {"loc": ["body", "name"], "msg": "ensure this value has at least 1 characters"},
    {"loc": ["body", "price"], "msg": "ensure this value is greater than 0"}
  ]
}
```

FastAPI tells you exactly which fields failed and why.

## Validating URL Parameters

You can also validate path and query parameters:

```python
from fastapi import Path, Query

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(gt=0),
    q: str = Query(None, max_length=10)
):
    return {"item_id": item_id, "q": q}
```

- `item_id` must be greater than 0
- `q` is optional, max 10 characters

## Custom Error Handling

Sometimes you want a custom error. For example, when a model isn't loaded:

```python
class ModelNotLoaded(Exception):
    pass

@app.exception_handler(ModelNotLoaded)
def handler(request, exc):
    return JSONResponse(
        status_code=503,
        content={"error": "Model is loading, try later"}
    )
```

## Summary

- FastAPI validates data **automatically**
- Use `Field(min_length=..., gt=...)` to add rules
- Invalid data → **422 error** with helpful message
- Use `HTTPException` for custom errors (like 404)
- Use `@app.exception_handler()` for special error types

You don't need to write if-statements to check data — FastAPI does it for you.
