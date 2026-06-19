# CRUD App Project Structure

## Project Layout

A well-organized FastAPI project with database integration typically follows this structure:

```
project/
+-- main.py           # FastAPI app, routes, startup
+-- database.py       # Engine, session, Base
+-- models.py         # SQLAlchemy ORM models
+-- schemas.py        # Pydantic request/response schemas
+-- crud.py           # Database CRUD operations
+-- requirements.txt  # Dependencies
```

```text
  +----------------------------------------------+
  |                  main.py                     |
  |          FastAPI App + Routes                |
  +----------+--------------+-------------------+
             |              |              |
             v              v              v
  +----------+--+  +--------+---+  +------+----------+
  | schemas.py  |  |  crud.py   |  |  database.py    |
  | Pydantic    |  |  DB        |  |  get_db()       |
  | Models      |  |  Operations|  |  dependency     |
  +-------------+  +-----+------+  +------+----------+
                         |                |
                         v                |
                   +-----+------+         |
                   | models.py  +<--------+
                   | SQLAlchemy |
                   | ORM Models |
                   +-----+------+
                         |
                         v
                   +-----+-----------+
                   |  database.py    |
                   |  Engine+Session |
                   +-----+-----------+
                         |
                         v
                   +-----+-----------+
                   | SQLite /        |
                   | PostgreSQL      |
                   +-----------------+
```

## database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./ml_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## models.py

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database import Base
from datetime import datetime

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(String, default="v1")
    is_correct = Column(Boolean, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## schemas.py

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PredictionRequest(BaseModel):
    input_text: str = Field(..., min_length=1, max_length=5000)

class PredictionResponse(BaseModel):
    id: int
    input_text: str
    prediction: str
    confidence: float
    model_version: str
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionFeedback(BaseModel):
    is_correct: bool
```

## crud.py

```python
from sqlalchemy.orm import Session
from models import PredictionRecord
from schemas import PredictionFeedback
from datetime import datetime

def create_prediction(db: Session, input_text: str, prediction: str,
                      confidence: float, model_version: str) -> PredictionRecord:
    record = PredictionRecord(
        input_text=input_text,
        prediction=prediction,
        confidence=confidence,
        model_version=model_version
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_prediction(db: Session, prediction_id: int):
    return db.query(PredictionRecord).filter(
        PredictionRecord.id == prediction_id
    ).first()

def get_all_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PredictionRecord).offset(skip).limit(limit).all()

def update_feedback(db: Session, prediction_id: int, feedback: PredictionFeedback):
    record = get_prediction(db, prediction_id)
    if record:
        record.is_correct = feedback.is_correct
        db.commit()
        db.refresh(record)
    return record
```

## main.py

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ML Prediction API", version="1.0")

@app.post("/predict/", response_model=schemas.PredictionResponse, status_code=201)
def predict(request: schemas.PredictionRequest, db: Session = Depends(get_db)):
    prediction_text = "positive"
    confidence = 0.92

    record = crud.create_prediction(
        db=db, input_text=request.input_text,
        prediction=prediction_text, confidence=confidence, model_version="v1"
    )
    return record

@app.get("/predictions/", response_model=list[schemas.PredictionResponse])
def list_predictions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_predictions(db, skip=skip, limit=limit)

@app.post("/predictions/{prediction_id}/feedback/")
def submit_feedback(prediction_id: int, feedback: schemas.PredictionFeedback,
                     db: Session = Depends(get_db)):
    record = crud.update_feedback(db, prediction_id, feedback)
    if not record:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": "Feedback submitted", "record": record}
```
