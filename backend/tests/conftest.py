import pytest
from fastapi.testclient import TestClient
from api.main import api
from api.db.conn import get_db

@pytest.fixture(scope="module")
def client():
    # Use a separate test database or mock if possible, 
    # but for this simple refactor validation we'll use the main DB 
    # (assuming it's a dev env as per user context).
    # Ideally, we would override dependency for get_db here.
    with TestClient(api) as c:
        yield c
