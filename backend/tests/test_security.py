import pytest
import time
from fastapi.testclient import TestClient

def test_password_complexity(client):
    # Too short
    response = client.post(
        "/auth/register",
        json={"email": "weak@example.com", "password": "123", "full_name": "Weak Pwd"}
    )
    assert response.status_code == 422
    
    # No number
    response = client.post(
        "/auth/register",
        json={"email": "weak2@example.com", "password": "passwordonly", "full_name": "Weak Pwd"}
    )
    assert response.status_code == 422
    
    # Good password - Use unique email/IP
    unique_email = f"strong_{int(time.time())}@example.com"
    response = client.post(
        "/auth/register",
        json={"email": unique_email, "password": "password123", "full_name": "Strong Pwd"},
        headers={"X-Forwarded-For": "1.1.1.1"}
    )
    assert response.status_code == 200

def test_rate_limiting(client):
    # Ensure user exists
    client.post(
        "/auth/register",
        json={"email": "rate@example.com", "password": "password123", "full_name": "Rate User"}
    )
    
    # Hit login limit (5/minute)
    # We make 6 requests
    for i in range(6):
        response = client.post(
            "/auth/login",
            data={"username": "rate@example.com", "password": "password123"},
            headers={"X-Forwarded-For": "2.2.2.2"}
        )
        if i < 5:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            
def test_refresh_token_flow(client):
    # Register
    client.post(
        "/auth/register",
        json={"email": "refresh@example.com", "password": "password123", "full_name": "Refresh User"}
    )
    
    # Login - Use unique IP
    login_res = client.post(
        "/auth/login",
        data={"username": "refresh@example.com", "password": "password123"},
        headers={"X-Forwarded-For": "3.3.3.3"}
    )
    assert login_res.status_code == 200
    data = login_res.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    refresh_token = data["refresh_token"]
    
    # Use refresh token
    refresh_res = client.post(
        "/auth/refresh",
        headers={"x-refresh-token": refresh_token}
    )
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()
