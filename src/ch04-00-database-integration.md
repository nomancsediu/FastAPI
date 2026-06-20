# Database Integration

In Chapter 3, we built a CRUD API using in-memory storage. Data disappeared when the server restarted. Now we'll upgrade the **same** `fastapi-crud/` project to use a real database with **SQLAlchemy** and **SQLite**.

## What Changes

We will modify these files in your existing `fastapi-crud/` project:

| File | Purpose | Change |
|------|---------|--------|
| `database.py` | SQLAlchemy engine + session | **Replaced** (was in-memory list) |
| `models.py` | SQLAlchemy table + Pydantic models | **Updated** (add ORM model) |
| `main.py` | Use database instead of in-memory | **Updated** |
| `requirements.txt` | + sqlalchemy | **Updated** |

## Current Project Structure

```
fastapi-crud/
├── main.py              # 5 CRUD endpoints (in-memory)
├── models.py            # Pydantic models (Item, ItemUpdate)
├── database.py          # In-memory list functions (WILL BE REPLACED)
├── requirements.txt     # fastapi, uvicorn
```

## After This Chapter

```
fastapi-crud/
├── main.py              # Updated: uses database sessions
├── database.py          # SQLAlchemy engine + get_db()
├── models.py            # SQLAlchemy ORM model + Pydantic models
├── requirements.txt     # + sqlalchemy
├── items.db             # SQLite database (auto-created)
```

> **Key point:** We're evolving one project, not starting a new one. Every concept from Chapter 3 still applies — we're just replacing the storage layer.
