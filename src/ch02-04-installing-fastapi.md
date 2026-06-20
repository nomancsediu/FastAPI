# Installing FastAPI

## Installation

FastAPI can be installed with pip. It is recommended to install it along with an ASGI server (Uvicorn) and the standard optional dependencies:

```bash
# Install FastAPI with standard optional dependencies
pip install "fastapi[standard]"

# Or install individually
pip install fastapi uvicorn

# For development with auto-reload
pip install fastapi uvicorn[standard]
```

## Project Setup

Create a project directory and set up a virtual environment. We'll use this same
project folder (`fastapi-crud/`) throughout the book.

```bash
mkdir fastapi-crud
cd fastapi-crud

python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install fastapi uvicorn
```

This is the project where we'll build our CRUD API in **Chapter 3**.

## Running the Server

FastAPI applications are run using Uvicorn. The basic command is:

```bash
uvicorn main:app --reload
```

- `main` — the Python file name (`main.py`)
- `app` — the FastAPI instance variable inside that file
- `--reload` — auto-restart when code changes (development only)

In Chapter 3 you'll create `main.py` and run this command yourself.
