
from fastapi import Header, HTTPException
import os

# Load your custom API key from environment or default
VALID_API_KEY = os.getenv("LIFE_OS_API_KEY", "secret123")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
