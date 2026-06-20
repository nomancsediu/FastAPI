# Building APIs Using FastAPI

This chapter is where you'll write your first real FastAPI code. Unlike the previous chapters (which were conceptual), here you'll build actual API projects step by step.

## What You Will Build

By the end of this chapter, you will have:

1. **A CRUD API project** — a fully functional API that can Create, Read, Update, and Delete items, stored in memory.
2. **Validation logic** — automatic input validation using Pydantic and FastAPI's built-in validators.
3. **File upload endpoints** — endpoints that accept image uploads and form data (essential for ML APIs).
4. **Async endpoints** — endpoints that handle I/O-bound operations without blocking the server.

## Project Structure

Throughout this chapter we will build toward this project layout:

```
fastapi-crud/
├── main.py              # FastAPI application + routes
├── models.py            # Pydantic models (schemas)
├── database.py          # In-memory data store
├── requirements.txt     # Python dependencies
```

> **Note:** In this chapter we keep things simple with in-memory storage. Chapter 4 will upgrade this to a real database using SQLAlchemy.

## Prerequisites

Before starting, make sure you have completed [Chapter 2](../ch02-04-installing-fastapi.md) and have FastAPI and Uvicorn installed:

```bash
pip install fastapi uvicorn
```

Now let's begin building.
