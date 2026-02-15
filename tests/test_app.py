from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Basketball Team" in data

def test_signup():
    response = client.post("/activities/Basketball%20Team/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Verify added
    response2 = client.get("/activities")
    data2 = response2.json()
    assert "test@example.com" in data2["Basketball Team"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Tennis%20Club/signup?email=dup@example.com")
    # Second attempt
    response = client.post("/activities/Tennis%20Club/signup?email=dup@example.com")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister():
    # Signup first
    client.post("/activities/Debate%20Team/signup?email=del@example.com")
    # Unregister
    response = client.delete("/activities/Debate%20Team/signup?email=del@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    # Verify removed
    response2 = client.get("/activities")
    data2 = response2.json()
    assert "del@example.com" not in data2["Debate Team"]["participants"]

def test_unregister_not_signed():
    response = client.delete("/activities/Debate%20Team/signup?email=notsigned@example.com")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]