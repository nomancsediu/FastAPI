# JWT Authentication

JWT (JSON Web Token) lets users log in and get a token. They use that token to access protected endpoints.

## How It Works

```
1. User sends username + password → POST /login
2. Server checks credentials, returns a token
3. User sends token with every request → Authorization: Bearer <token>
4. Server checks token, allows access
```

## Step 1: Install Dependencies

```bash
pip install "python-jose[cryptography]" passlib bcrypt
```

## Step 2: Create auth.py

```python
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from config import SECRET_KEY

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(username: str) -> str:
    data = {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except:
        return None
```

## Step 3: Add Users Table to models.py

Open `models.py` and add this at the bottom:

```python
from sqlalchemy import Column, Integer, String


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

Now `models.py` has two models: `ItemDB` (from Chapter 4) and `UserDB` (new).

## Step 4: Add Auth Endpoints to main.py

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import UserDB
from auth import hash_password, verify_password, create_token, decode_token

oauth = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    user = UserDB(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth), db: Session = Depends(get_db)):
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

## Step 5: Protect Routes

To protect a route, add `current_user = Depends(get_current_user)`:

```python
@app.get("/items/")
def list_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(ItemDB).all()
```

Now only logged-in users can see items.

## Test the Auth Flow

```bash
# Register
curl -X POST "http://localhost:8000/register?username=alice&password=secret123"

# Login (get token)
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=secret123"

# Use token
curl "http://localhost:8000/items/" \
  -H "Authorization: Bearer <token>"
```
