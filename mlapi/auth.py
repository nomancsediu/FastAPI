from datetime import datetime, timedelta, timezone
from fastapi import Header, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from config import API_KEY, SECRET_KEY
from database import get_db
from models import UserDB

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


def verify_api_key(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


def verify_api_key_db(
    x_api_key: str | None = Header(None),
    db: Session = Depends(get_db),
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    key = db.query(UserDB).filter(UserDB.username == x_api_key).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key
