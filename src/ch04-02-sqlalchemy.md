# Adding a Database with SQLAlchemy

Right now our data disappears when the server restarts. Let's fix that by adding a database.

## Step 1: Install SQLAlchemy

```bash
pip install sqlalchemy
```

```bash
echo "sqlalchemy" >> requirements.txt
```

## Step 2: Replace database.py

Replace `database.py` with SQLAlchemy code:

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./items.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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

## Step 3: Replace models.py

Replace `models.py` with a database model:

```python
# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base


class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
```

This defines the `items` table. Three columns: `id`, `name`, `price`.

Keep your Pydantic models too (they're still needed for validation):

```python
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
```

## Step 4: Update main.py

Update `main.py` to use the database:

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import ItemDB, Item, ItemUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/items/", status_code=201)
def create(data: Item, db: Session = Depends(get_db)):
    item = ItemDB(name=data.name, price=data.price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/")
def list_all(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()


@app.get("/items/{item_id}")
def get_one(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}")
def update_one(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if data.name is not None:
        item.name = data.name
    if data.price is not None:
        item.price = data.price
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_one(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return
```

## What Changed?

| Before (Chapter 3) | After (Chapter 4) |
|--------------------|-------------------|
| `database.py` had Python list functions | `database.py` has SQLAlchemy engine + `get_db()` |
| `models.py` had only Pydantic models | `models.py` has SQLAlchemy model + Pydantic models |
| `items.append(...)` | `db.add() + db.commit()` |
| `for item in items:` | `db.query(ItemDB).all()` |
| Data lost on restart | Data saved to `items.db` |

## Test It

```bash
uvicorn main:app --reload
```

Create some items, stop the server (`Ctrl+C`), start again. The items are still there!

```
fastapi-crud/
├── main.py
├── database.py      # NEW
├── models.py        # UPDATED
├── requirements.txt # + sqlalchemy
├── items.db         # Auto-created
```
