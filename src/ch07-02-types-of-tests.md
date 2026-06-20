# Testing the CRUD API

Let's write tests for our `fastapi-crud/` project.

## Step 1: Install Test Tools

```bash
cd fastapi-crud
pip install pytest httpx
```

## Step 2: Create a Test File

```bash
mkdir tests
touch tests/__init__.py tests/test_api.py
```

## Step 3: Write Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_item():
    response = client.post("/items/", json={"name": "Laptop", "price": 999})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999
    assert "id" in data


def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_update_item():
    # Create first
    created = client.post("/items/", json={"name": "Mouse", "price": 29}).json()
    item_id = created["id"]

    # Update
    response = client.put(f"/items/{item_id}", json={"price": 35})
    assert response.status_code == 200
    assert response.json()["price"] == 35


def test_delete_item():
    created = client.post("/items/", json={"name": "Temp", "price": 10}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204


def test_missing_required_field():
    response = client.post("/items/", json={"name": "Test"})  # Missing price
    assert response.status_code == 422
```

## Step 4: Run Tests

```bash
pytest tests/ -v
```

You'll see:

```
tests/test_api.py .......                                         [100%]
```

All green! Each test:
1. Sends a real HTTP request to your API
2. Checks the response status code
3. Checks the response data

`TestClient` works just like curl — no special setup needed.
