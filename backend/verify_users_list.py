import requests
import json

BASE_URL = "http://localhost:8000"

def verify_users_list():
    email = "debug_admin@example.com" # Existing admin from previous step
    password = "password123"

    # Login
    login_data = {"username": email, "password": password}
    r = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if r.status_code != 200:
        print("Login failed:", r.text)
        return

    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get Users
    print("Fetching /users/ ...")
    r = requests.get(f"{BASE_URL}/users/", headers=headers)
    
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        try:
            data = r.json()
            print("Response Data (First 2):", data[:2] if len(data) > 0 else "Empty List")
        except Exception as e:
            print(f"JSON Decode Error: {e}")
            print("Raw Text:", r.text)
    else:
        print("Error Response:", r.text)

if __name__ == "__main__":
    verify_users_list()
