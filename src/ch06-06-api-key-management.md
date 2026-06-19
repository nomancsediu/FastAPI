# 6.6 API Key Management

API Key is simpler authentication than JWT — ideal for machine-to-machine communication.

## API Key via Header

```python
from fastapi import FastAPI, Header, HTTPException, status

app = FastAPI()
API_KEYS = {"ml-client-key-001", "ml-client-key-002"}

@app.get("/predict/")
async def predict(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return {"prediction": "result"}
```

## Management via .env File

```bash
# .env
API_KEY_ML_SERVICE=sk-ml-abc123
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-production-secret-key
```

```python
# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key_ml_service: str
    database_url: str
    secret_key: str
    class Config:
        env_file = ".env"

settings = Settings()
```

## API Key vs JWT

| | API Key | JWT |
|--|---------|-----|
| Complexity | Simple | Moderate |
| Scalability | Low | High |
| Use Case | Machine-to-Machine | User Authentication |
| Expiry | Manual | Built-in |
