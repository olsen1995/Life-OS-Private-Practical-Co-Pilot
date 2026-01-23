from fastapi.testclient import TestClient
from main import app  # 👈 replace with your actual app import path

client = TestClient(app)

def test_fixit_mode():
    response = client.post(
        "/route",
        json={"mode": "Fixit", "input_text": "Fix the broken lamp"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

def test_fridge_mode():
    response = client.post(
        "/route",
        json={"mode": "Fridge", "input_text": "Scan my fridge"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

def test_kitchen_mode():
    response = client.post(
        "/route",
        json={"mode": "Kitchen", "input_text": "What can I cook?"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

def test_home_organizer_mode():
    response = client.post(
        "/route",
        json={"mode": "HomeOrganizer", "input_text": "Organize my week"}
    )
    assert response.status_code == 200
    assert "result" in response.json()

def test_invalid_mode():
    response = client.post(
        "/route",
        json={"mode": "InvalidMode", "input_text": "This should fail"}
    )
    assert response.status_code in [400, 422]Get-ChildItem -Recurse -Include *.py -Exclude .venv | Select-String "app = FastAPI()"
