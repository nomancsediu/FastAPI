# Dependency Injection

## How Dependency Injection Works

FastAPI's dependency injection system allows you to declare dependencies that your endpoint functions need, and FastAPI will automatically provide them. Dependencies are declared using the `Depends()` function. When a request arrives, FastAPI resolves all dependencies, calls them in the correct order, and passes their return values to your endpoint function. This pattern promotes code reuse, makes testing easier, and keeps your endpoint functions clean.

```text
  +--------------------+
  |  Endpoint Function |
  +--+----------+--+---+
     |          |  |
     |          |  |
     v          v  v
  +--+-----------+------+
  |       Depends()     |
  +--+----------+--+----+
     |          |  |
     v          v  v
  +-------+ +--------+ +-----------+
  | get_db| |get_user| |get_settings|
  | DB    | | JWT    | | .env File  |
  | Sess. | | Auth   | |            |
  +---+---+ +---+----+ +-----+------+
      |         |            |
      v         v            v
  +--------+ +-------+ +-----------+
  |Database| |  JWT  | |  .env     |
  |        | | Store | |  Config   |
  +--------+ +-------+ +-----------+
```

## Database Connection Dependency

```python
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db

@app.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    record = crud.get_prediction(db, prediction_id)
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return record
```

## Configuration Management

```python
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    secret_key: str = "your-secret-key"
    model_path: str = "model.joblib"
    debug: bool = False

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

@app.get("/config")
def get_config(settings: Settings = Depends(get_settings)):
    return {
        "database_url": settings.database_url,
        "model_path": settings.model_path,
        "debug": settings.debug
    }
```
