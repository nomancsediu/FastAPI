# JWT Authentication

JWT (JSON Web Token) lets users log in with a username and password, then get a
token they can use instead of an API key. This is useful when you want per-user
access control or a simple sign-up flow for your ML API.

```
Flow:  Register → Login (get token) → Use token on protected routes
```

## What You'll Add

| Action | File | Where |
|--------|------|-------|
| Edit | `mlapi/auth.py` | Add JWT functions at the bottom (after `verify_api_key`) |
| Create | `mlapi/database.py` | SQLAlchemy engine + session for user storage |
| Create | `mlapi/models.py` | UserDB table definition |
| Edit | `mlapi/main.py` | Add imports, `oauth`, `/register`, `/login`, JWT-protected route |

---

## Step 0: Install Dependencies

```bash
pip install "python-jose[cryptography]" passlib bcrypt sqlalchemy
```

| Package | Purpose |
|---------|---------|
| `python-jose` | Create and verify JWT tokens |
| `passlib` + `bcrypt` | Hash passwords securely |
| `sqlalchemy` | Database ORM (stores users) |

---

## Step 1: Create `database.py`

Create `mlapi/database.py` (same pattern as the CRUD project):

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import DATABASE_URL

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Step 2: Create `models.py`

Create `mlapi/models.py` with a User table:

```python
from sqlalchemy import Column, Integer, String
from database import Base


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

---

## Step 3: Add JWT Functions to `auth.py`

Open `mlapi/auth.py`. Add these functions **after** `verify_api_key`:

```python
from datetime import datetime, timedelta, timezone
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
    data = {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        return None
```

Your `auth.py` now has both API key verification and JWT support.

---

## Step 4: Update `main.py`

Open `mlapi/main.py` and make these changes.

### 4a — Add imports (top of file)

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import UserDB
from auth import hash_password, verify_password, create_token, decode_token
```

### 4b — Create tables on startup

Right after the import section, before creating `app`:

```python
Base.metadata.create_all(bind=engine)
```

### 4c — Create OAuth2 scheme (after `app.add_middleware(...)`, before routes)

```python
oauth = OAuth2PasswordBearer(tokenUrl="login")
```

### 4d — Add auth routes (at the bottom of `main.py`)

```python
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

### 4e — (Optional) Protect `/predict` with JWT instead of API key

You can replace or supplement the API key check. To use JWT on a route, add
`current_user = Depends(get_current_user)`:

```python
@app.post("/predict", response_model=IrisOutput)
def predict_iris(
    data: IrisInput,
    current_user = Depends(get_current_user),  # JWT auth
    # api_key: str = Depends(verify_api_key),  # or comment out API key
):
    ...
```

---

## Test the Auth Flow

```bash
# 1. Register a user
curl -X POST "http://localhost:8000/register?username=alice&password=secret123"

# 2. Login — get a JWT token
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=secret123"

# 3. Predict with the token (replace <token> with value from step 2)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

You can also test from **Swagger UI** at `/docs` — click "Authorize" and paste
your token.

---

## Project Structure Now

```
mlapi/
├── train.py
├── model.py
├── schemas.py
├── database.py          # NEW — SQLAlchemy engine + session
├── models.py            # NEW — UserDB table
├── auth.py              # Updated — + JWT functions
├── config.py
├── .env
├── main.py              # Updated — /register, /login, get_current_user
├── iris_model.joblib
├── users.db             # NEW — SQLite user database (auto-created)
├── requirements.txt     # + python-jose, passlib, bcrypt, sqlalchemy
└── tests/
```

Next: **Best practices** — logging, status codes, and polishing your ML API.
