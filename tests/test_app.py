import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- /activities GET ---
def test_get_activities():
    # Arrange
    # (No setup needed, uses in-memory DB)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- /activities/{activity}/signup POST ---
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/participant?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/participant?email={email}")

def test_signup_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser3@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# --- /activities/{activity}/participant DELETE ---
def test_remove_participant_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser4@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_remove_participant_not_found():
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_remove_participant_nonexistent_activity():
    # Arrange
    activity = "Nonexistent Club"
    email = "testuser5@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/participant?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
