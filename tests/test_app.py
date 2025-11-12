import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Check participant added
    get_response = client.get("/activities")
    assert email in get_response.json()[activity]["participants"]


def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success():
    email = "emma@mergington.edu"
    activity = "Programming Class"
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    # Check participant removed
    get_response = client.get("/activities")
    assert email not in get_response.json()[activity]["participants"]


def test_unregister_from_activity_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
