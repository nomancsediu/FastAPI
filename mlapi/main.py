import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from model import classifier
from schemas import IrisInput, IrisOutput, BatchInput, BatchOutput
from auth import (
    verify_api_key,
    verify_api_key_db,
    hash_password,
    verify_password,
    create_token,
)
from database import engine, get_db, Base
from models import UserDB
logger = logging.getLogger("mlapi")
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ML API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-API-Key"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} → {response.status_code}")
    return response


@app.get("/")
def root():
    return {"message": "ML API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=IrisOutput)
def predict(input_data: IrisInput, _=Depends(verify_api_key)):
    try:
        return classifier.predict(input_data.features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/batch", response_model=BatchOutput)
def predict_batch(input_data: BatchInput, _=Depends(verify_api_key)):
    try:
        predictions = classifier.predict_batch(input_data.samples)
        return {"predictions": predictions, "count": len(predictions)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = UserDB(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created"}


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/predict/v2", response_model=IrisOutput)
def predict_v2(input_data: IrisInput, _=Depends(verify_api_key_db)):
    try:
        return classifier.predict(input_data.features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
