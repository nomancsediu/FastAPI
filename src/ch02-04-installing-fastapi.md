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

A typical FastAPI project has a clean directory structure. Create a project directory and set up a virtual environment:

```bash
mkdir fastapi-ml-project
cd fastapi-ml-project

python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install fastapi uvicorn pydantic scikit-learn
```

## Running the Server

FastAPI applications are run using Uvicorn. The basic command is:

```bash
uvicorn main:app --reload
```

Here, `main` refers to the Python file name (`main.py`), `app` is the FastAPI instance variable, and `--reload` enables auto-reload during development (the server restarts automatically when you make code changes). In production, you would run multiple Uvicorn workers behind a process manager like Gunicorn.
