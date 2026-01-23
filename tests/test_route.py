from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_fixit_mode():
    response = client.post("/route", json={"input": "Fix my broken door"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "mode" in data


def test_fridge_mode():
    response = client.post("/route", json={"input": "Scan my fridge"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "mode" in data


def test_kitchen_mode():
    response = client.post("/route", json={"input": "What can I cook with eggs?"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "mode" in data


def test_home_organizer_mode():
    response = client.post("/route", json={"input": "Organize my week"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "mode" in data


def test_invalid_mode_fallback():
    response = client.post("/route", json={"input": "Random unknown request"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "mode" in data
