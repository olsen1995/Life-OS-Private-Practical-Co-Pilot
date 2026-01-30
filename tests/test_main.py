import pytest
from fastapi.testclient import TestClient
from lifeos.main import app

client = TestClient(app)

# ✅ Authorization header expected by your middleware
HEADERS = {"x-api-key": "secret123"}

def test_ask_endpoint():
    res = client.post("/ask", json={
        "message": "What can I make with eggs?",
        "user_id": "user_test"
    }, headers=HEADERS)

    assert res.status_code == 200
    assert "summary" in res.json()

def test_memory_flow():
    # Add a memory manually
    from lifeos.storage.memory_manager import MemoryManager
    mm = MemoryManager("user_test")
    mm.add_memory("Remember the eggs.")

    # Retrieve memory
    response = client.get("/memory?user_id=user_test")
    assert response.status_code == 200
    assert "Remember the eggs" in response.text

    # Clear memory
    response = client.post("/memory", data={"confirm": "yes", "user_id": "user_test"})
    assert response.status_code == 303
