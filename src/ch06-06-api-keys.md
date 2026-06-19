# Managing API Keys

## API Keys with Headers

API keys are a simpler alternative to JWT for machine-to-machine communication:

```python
from fastapi import FastAPI, Header, HTTPException, status

app = FastAPI()

API_KEYS = {"ml-client-key-001", "ml-client-key-002"}

@app.get("/predict/")
async def predict(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return {"prediction": "result"}
```

## API Keys with .env File

For better security, store API keys in environment variables and manage them with a `.env` file:

```python
# .env file
API_KEY_ML_SERVICE=sk-ml-abc123
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-production-secret-key

# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key_ml_service: str
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()

# main.py
from fastapi import Header, HTTPException
import settings

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key_ml_service:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.get("/predict/")
async def predict(api_key: str = Depends(verify_api_key)):
    return {"prediction": "result"}
```
