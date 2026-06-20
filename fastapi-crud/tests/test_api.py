from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello World"}


def test_search():
    resp = client.get("/search/?q=python&page=2")
    assert resp.status_code == 200
    assert resp.json() == {"query": "python", "page": 2}


def test_create_item():
    resp = client.post("/items/", json={"name": "Laptop", "price": 999.0})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.0
    assert "id" in data


def test_list_items():
    resp = client.get("/items/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_item():
    create = client.post("/items/", json={"name": "Mouse", "price": 29.0})
    item_id = create.json()["id"]
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Mouse"


def test_get_item_not_found():
    resp = client.get("/items/99999")
    assert resp.status_code == 404


def test_update_item():
    create = client.post("/items/", json={"name": "Keyboard", "price": 49.0})
    item_id = create.json()["id"]
    resp = client.put(f"/items/{item_id}", json={"price": 39.0})
    assert resp.status_code == 200
    assert resp.json()["price"] == 39.0
    assert resp.json()["name"] == "Keyboard"


def test_delete_item():
    create = client.post("/items/", json={"name": "Monitor", "price": 299.0})
    item_id = create.json()["id"]
    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204
    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404


def test_validation_error():
    resp = client.post("/items/", json={"name": "Test", "price": "free"})
    assert resp.status_code == 422
