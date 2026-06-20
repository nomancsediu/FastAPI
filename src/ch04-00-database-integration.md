# Database Integration

In Chapter 3, we built a CRUD API using in-memory storage. Data disappeared when the server restarted. Now we'll upgrade the **same** `fastapi-crud/` project to use a real database with **SQLAlchemy** and **SQLite**.

## What Changes

We will add these files to your existing `fastapi-crud/` project:

| File | Purpose | New or Modified |
|------|---------|----------------|
| `database.py` | SQLAlchemy engine + session config | **New** |
| `models.py` | SQLAlchemy ORM models (database tables) | **Modified** (was Pydantic-only) |
| `schemas.py` | Pydantic request/response models | **New** (split from models.py) |
| `crud.py` | Database read/write operations | **New** |
| `main.py` | Updated to use database instead of in-memory | **Modified** |
| `requirements.txt` | Updated with SQLAlchemy | **Modified** |

## Current Project Structure

```
fastapi-crud/
├── main.py              # In-memory CRUD endpoints
├── models.py            # Pydantic models only
├── database.py          # In-memory data store (WILL BE REPLACED)
├── requirements.txt     # fastapi, uvicorn, pydantic
```

## After This Chapter

```
fastapi-crud/
├── main.py              # Updated: uses database instead of in-memory
├── database.py          # SQLAlchemy engine + get_db() dependency
├── models.py            # SQLAlchemy ORM models (database tables)
├── schemas.py           # Pydantic models (API request/response)
├── crud.py              # Database CRUD operations
├── requirements.txt     # + sqlalchemy added
├── app.db               # SQLite database (auto-created)
```

> **Key point:** We're evolving one project, not starting a new one. Every concept from Chapter 3 still applies — we're just replacing the storage layer.
