import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -----------------------------
# Test Create Order (Valid)
# -----------------------------
def test_create_order_success():
    payload = {
        "customer_name": "John Doe",
        "address": "123 Main Street",
        "phone": "9876543210",
        "items": [
            {
                "menu_id": 1,
                "quantity": 2
            }
        ]
    }

    response = client.post("/api/orders/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == "RECEIVED"
    assert len(data["items"]) == 1


# -----------------------------
# Test Empty Cart Validation
# -----------------------------
def test_create_order_empty_cart():
    payload = {
        "customer_name": "John Doe",
        "address": "123 Main Street",
        "phone": "9876543210",
        "items": []
    }

    response = client.post("/api/orders/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Cart cannot be empty"


# -----------------------------
# Test Phone Validation
# -----------------------------
def test_invalid_phone():
    payload = {
        "customer_name": "John Doe",
        "address": "123 Main Street",
        "phone": "12345",
        "items": [
            {
                "menu_id": 1,
                "quantity": 1
            }
        ]
    }

    response = client.post("/api/orders/", json=payload)

    assert response.status_code == 422


# -----------------------------
# Test Get All Orders
# -----------------------------
def test_get_orders():
    response = client.get("/api/orders/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------------
# Test Get Single Order
# -----------------------------
def test_get_single_order():
    response = client.get("/api/orders/1")

    assert response.status_code in [200, 404]


# -----------------------------
# Test Update Order Status
# -----------------------------
def test_update_order_status():
    payload = {
        "status": "PREPARING"
    }

    response = client.put("/api/orders/1/status", json=payload)

    assert response.status_code in [200, 404]
