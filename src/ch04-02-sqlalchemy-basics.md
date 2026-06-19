# 4.2 SQLAlchemy Basics

SQLAlchemy is Python's most popular ORM (Object-Relational Mapping). It allows you to perform database operations using Python classes instead of writing SQL.

## Defining Models

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    model_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```
ORM Flow:
[Python Class] ──> [SQLAlchemy ORM] ──> [SQL Query] ──> [Database]
[Database]    <─── [SQL Result]   <─── [SQL Query] <─── [Python Object]
```
