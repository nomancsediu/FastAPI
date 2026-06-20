# API Key Authentication

API keys are the simplest way to secure your API. A client sends a key in the header, and you check if it's valid.

## Step 1: Create auth.py

```python
# auth.py
from fastapi import Header, HTTPException
from config import API_KEY

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
```

## Step 2: Protect an Endpoint

In `main.py`, add:

```python
from auth import verify_api_key

@app.get("/admin/stats")
def get_stats(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access", "total_items": 5}
```

(`Depends` is imported from `fastapi`)

## Test It

```bash
# Without key — 401 error
curl http://localhost:8000/admin/stats

# With key — works!
curl http://localhost:8000/admin/stats \
  -H "X-API-Key: my-super-secret-key"
```

API keys are perfect for machine-to-machine communication (a script calling your API).

## Multiple Keys (One Per User)

If you need separate keys for different users, store them in the database.

Add this to `models.py`:

```python
class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    owner = Column(String)
```

Update `auth.py` to check the database:

```python
from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ApiKey

def verify_api_key(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db),
):
    key = db.query(ApiKey).filter(ApiKey.key == x_api_key).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid key")
    return key
```

| Use Case | Method |
|----------|--------|
| Single API key | Config file (above) |
| One key per user | Database table (this section) |
| User login | JWT (section 6.5) |
