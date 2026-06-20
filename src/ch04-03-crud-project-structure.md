# Database CRUD — Summary

Your `fastapi-crud/` project now saves data permanently in a database.

## What Changed

| Before (Chapter 3) | After (Chapter 4) |
|--------------------|-------------------|
| Data in Python list | Data in SQLite database |
| `items.append(...)` | `db.add(...) + db.commit()` |
| `for item in items:` | `db.query(ItemDB).all()` |
| Lost on restart | Saved forever |

The API endpoints are exactly the same. Only the storage changed.

## Your Project

```
fastapi-crud/
├── main.py          # Same 5 endpoints
├── database.py      # NEW — database connection
├── models.py        # NEW — defines the 'items' table
├── requirements.txt # + sqlalchemy
├── items.db         # Your data lives here
```

## Key Concepts

- **ORM (Object Relational Mapper)**: SQLAlchemy lets you use Python objects to work with databases
- **`Depends(get_db)`**: Gives each request its own database session
- **`db.commit()`**: Saves changes to the database
- **`db.refresh()`**: Updates the Python object with database-generated values (like `id`)

In the next chapter, we'll build a Machine Learning API from scratch.
