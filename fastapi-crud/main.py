from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import ItemDB, Item, ItemUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


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


@app.get("/search/")
def search(q: str = "", page: int = 1):
    return {"query": q, "page": page}
