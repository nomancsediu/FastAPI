# Handling Validations and Errors

## Built-in Validation

FastAPI provides several layers of validation out of the box:

```python
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field, constr
from typing import Optional

app = FastAPI()

class PredictionInput(BaseModel):
    text: constr(min_length=1, max_length=1000)
    model: str = Field(default="default-model", pattern=r"^[a-zA-Z0-9_-]+$")
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)

@app.post("/predict/")
def predict(input_data: PredictionInput):
    return {"result": "processed"}

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., gt=0, description="Item ID must be positive"),
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1, description="Page number")
):
    return {"item_id": item_id, "q": q, "page": page}
```

## Custom Exception Handling

You can create custom exception handlers to return consistent error responses:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class ModelNotLoadedError(Exception):
    def __init__(self, model_name: str):
        self.model_name = model_name

@app.exception_handler(ModelNotLoadedError)
async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
    return JSONResponse(
        status_code=503,
        content={
            "error": "ModelNotLoaded",
            "message": f"Model '{exc.model_name}' is not loaded.",
            "detail": "The ML model is currently being initialized."
        }
    )

@app.get("/predict/{model_name}")
def predict(model_name: str):
    if model_name not in loaded_models:
        raise ModelNotLoadedError(model_name)
    return {"prediction": "result"}
```

```text
  +------------------+
  |  Incoming        |
  |  Request         |
  +--------+---------+
           |
           v
  +--------+---------+
  |  Pydantic        |
  |  Validation      |
  +--------+---------+
           |
     +-----+-----+
     |           |
   Valid       Invalid
     |           |
     v           v
  +------+   +------------------+
  | Endp.|   | 422 Validation   |
  | Handl|   | Error            |
  +--+---+   +------------------+
     |
  +--+--+----------+
  |     |          |
  v     v          v
+----+ +-------+ +----------------+
| 2xx| | 404   | | 500 Global     |
| OK | | Not   | | Exception      |
|    | | Found | | Handler        |
+----+ +-------+ +----------------+
```
