import pytest

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    # 200 or 400 if already exists
    assert response.status_code in [200, 400]

def test_login_user(client):
    # Ensure user exists
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123", "full_name": "Test User"}
    )
    
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_me(client):
    # Login first
    login_res = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
