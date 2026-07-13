import pytest
from fastapi.testclient import TestClient
from main import app 

# TASK 6: Automated Testing
client = TestClient(app)

def test_successful_user_creation():
    response = client.post("/users/", params={"email": "newuser@test.com"})
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

def test_duplicate_email_conflict():
    response = client.post("/users/", params={"email": "existinguser@test.com"})
    assert response.status_code == 400
    
    assert response.json() == {
        "error": True, 
        "detail": "Email already registered", 
        "status": 400
    }

def test_protected_route_without_token():
    response = client.get("/users/me")
    assert response.status_code == 401
    
    assert response.json() == {
        "error": True, 
        "detail": "Not authenticated", 
        "status": 401
    }
    