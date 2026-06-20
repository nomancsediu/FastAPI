# Building APIs Using FastAPI

In Chapter 2 you set up the `fastapi-crud/` project and wrote your first FastAPI
endpoints. Now we'll turn that into a fully functional CRUD API.

## What You Already Have

From Chapter 2, your `fastapi-crud/` project looks like this:

```text
fastapi-crud/
├── main.py           # GET /, GET /items/{id}, GET /search/
├── requirements.txt  # fastapi, uvicorn
└── venv/             # Virtual environment
```

## What You Will Build in This Chapter

1. **Pydantic models** — define data structures in `models.py`
2. **POST endpoints** — accept data from clients
3. **Storage layer** — in-memory storage in `database.py`
4. **Full CRUD** — Create, Read, Update, Delete
5. **Validation** — automatic input checking
6. **Async programming** — non-blocking endpoints

## Final Project Structure

By the end of this chapter:

```text
fastapi-crud/
├── main.py           # 5 CRUD endpoints
├── models.py         # Pydantic schemas (Item, ItemUpdate)
├── database.py       # In-memory data store
├── requirements.txt
└── venv/
```

> **Note:** In this chapter we use in-memory storage (data resets when the server
> restarts). Chapter 4 will upgrade to a real SQLite database using SQLAlchemy.

Let's begin. Open your `fastapi-crud/` folder from Chapter 2.
