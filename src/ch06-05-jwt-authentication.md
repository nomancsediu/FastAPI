# JWT Authentication

## How JWT Works

JSON Web Tokens (JWT) provide a stateless, scalable authentication mechanism for APIs. The flow works as follows: the client sends their credentials (username/password) to a `/login` endpoint. The server verifies the credentials and creates a JWT containing a payload (user ID, role, expiration time) signed with a secret key. The client stores this token and includes it in the `Authorization: Bearer <token>` header of every subsequent request. The server verifies the token's signature on each request and extracts the user information from the payload.

```text
  Client            Server /login         User DB       Protected Endpoint
    |                     |                  |                  |
    +---POST /login------->                  |                  |
    |   user + password   |                  |                  |
    |                     +---verify creds-->|                  |
    |                     |<--user found-----+                  |
    |                     |                                     |
    |                     +---create JWT (sign w/ SECRET_KEY)   |
    |<--{access_token,----+                  |                  |
    |    token_type}      |                  |                  |
    |                                                           |
    +---GET /predict (Authorization: Bearer <token>)---------->|
    |                                        +--verify sig----->|
    |                                        +--extract user--->|
    |<--200 OK + data---------------------------------------------------+
```

## Implementation

```python
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("admin123"),
        "role": "admin"
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in fake_users_db:
        raise credentials_exception
    return fake_users_db[username]

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected/")
async def protected_route(current_user=Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user["username"]}
```
