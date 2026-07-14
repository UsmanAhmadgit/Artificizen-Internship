import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import Base, engine

# Setup fake client
client = TestClient(app)

# Helper variables
test_user = {"email": "capstone@test.com", "password": "securepassword"}
token = ""

# 1. Test Registration
def test_register_user():
    # Drop and recreate tables to ensure a clean test state
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    assert response.json()["email"] == test_user["email"]

# 2. Test Login
def test_login_user():
    global token
    response = client.post("/auth/token", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

# 3. Test Unauthorized Access
def test_unauthorized_access():
    # Attempting to fetch tasks without the JWT
    response = client.get("/tasks/")
    assert response.status_code == 401
    # Check if global exception handler reformatted the error
    assert response.json()["error"] is True 

# 4. Test Create Task
def test_create_task():
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"title": "Submit Capstone", "description": "Finish the internship week", "status": "pending"}
    
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Submit Capstone"

# 5. Test Fetch Tasks
def test_fetch_tasks():
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    