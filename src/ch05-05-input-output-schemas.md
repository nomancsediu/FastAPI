# Input and Output Schemas

Schemas define the shape of data that flows in and out of your API. FastAPI uses them for validation, documentation, and automatic error handling.

## Our Schemas File

```python
from pydantic import BaseModel, Field
from typing import List


class IrisInput(BaseModel):
    """
    What the client sends when predicting one flower.
    Exactly 4 measurements required.
    """
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Four measurements: sepal_length, sepal_width, "
                    "petal_length, petal_width",
    )


class IrisOutput(BaseModel):
    """
    What the API returns: the species name and confidence.
    """
    species: str = Field(
        ...,
        description="Predicted iris species (setosa, versicolor, virginica)",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score from 0.0 to 1.0",
    )


class BatchInput(BaseModel):
    """Multiple flowers at once."""
    samples: List[List[float]] = Field(
        ...,
        min_length=1,
        description="List of flower measurement arrays",
    )


class BatchOutput(BaseModel):
    """One prediction per input sample."""
    predictions: List[IrisOutput]
    count: int
```

## What Each Part Does

### `BaseModel`

Pydantic's base class. It gives every schema:
- **Automatic type validation** — if the client sends a string where a number is expected, FastAPI returns a 422 error immediately
- **JSON serialization** — convert Python objects to JSON and back
- **Documentation** — Swagger UI shows the schema automatically

### `Field(...)`

Configures validation rules for each field:

| Parameter | Meaning |
|-----------|---------|
| `...` | Required field (client must provide it) |
| `min_length=4` | List must have at least 4 items |
| `max_length=4` | List must have at most 4 items (so exactly 4) |
| `ge=0.0` | Value must be ≥ 0.0 |
| `le=1.0` | Value must be ≤ 1.0 |
| `description=` | Text shown in Swagger UI docs |

### Why `List[float]`?

```python
features: List[float]
```

This tells Pydantic: "features must be a list, and every item in the list must be a float." If the client sends `["a", "b", "c", "d"]`, Pydantic rejects it because strings are not floats.

### Why Separate Input and Output Classes?

```python
class IrisInput(BaseModel):   # What the client sends
class IrisOutput(BaseModel):  # What the server returns
```

These are different things:
- **Input** has constraints (`min_length=4`, `max_length=4`)
- **Output** has guarantees (`ge=0.0`, `le=1.0`)

If you reuse one class for both, you can't add output-only fields (like `inference_time`) or input-only constraints without making messy optional fields.

## What FastAPI Does With Schemas

When you annotate an endpoint with `response_model=IrisOutput`:

```python
@app.post("/predict", response_model=IrisOutput)
def predict_iris(data: IrisInput):
    ...
```

FastAPI automatically:

1. **Validates the input** — before your function runs, it checks that the JSON body matches `IrisInput`. If not → 422 error.

2. **Validates the output** — after your function returns, it checks that the result matches `IrisOutput`. If not → server error (catches bugs in your code).

3. **Filters extra fields** — if your function returns `{"species": "setosa", "confidence": 1.0, "secret_key": "abc"}`, FastAPI removes `secret_key` from the response.

4. **Generates OpenAPI docs** — Swagger UI at `/docs` shows the exact JSON format, field descriptions, and constraints.
