
import os
import json
from datetime import datetime, timedelta
from fastapi import Header, HTTPException

API_KEYS_FILE = "storage/api_keys.json"

# Default keys to preload if file doesn't exist
DEFAULT_KEYS = {
    "secret123-john": {"active": True, "requests": 0, "last_used": None},
    "secret123-jane": {"active": True, "requests": 0, "last_used": None}
}

# Load or create key file
if not os.path.exists(API_KEYS_FILE):
    os.makedirs(os.path.dirname(API_KEYS_FILE), exist_ok=True)
    with open(API_KEYS_FILE, "w") as f:
        json.dump(DEFAULT_KEYS, f, indent=2)

def load_keys():
    with open(API_KEYS_FILE, "r") as f:
        return json.load(f)

def save_keys(keys):
    with open(API_KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=2)

def verify_api_key(x_api_key: str = Header(...)):
    keys = load_keys()

    if x_api_key not in keys:
        raise HTTPException(status_code=403, detail="API key not found")

    if not keys[x_api_key]["active"]:
        raise HTTPException(status_code=403, detail="API key disabled")

    # Rate limiting (example: 100 requests/day)
    limit = 100
    last_used = keys[x_api_key].get("last_used")
    today = datetime.utcnow().date()

    if last_used:
        last_dt = datetime.fromisoformat(last_used)
        if last_dt.date() == today and keys[x_api_key]["requests"] >= limit:
            raise HTTPException(status_code=429, detail="API key rate limit reached")

    # Update usage
    if last_used and datetime.fromisoformat(last_used).date() == today:
        keys[x_api_key]["requests"] += 1
    else:
        keys[x_api_key]["requests"] = 1

    keys[x_api_key]["last_used"] = datetime.utcnow().isoformat()
    save_keys(keys)

    return x_api_key  # return key for tracking if needed

# Utility functions
def get_api_key_info():
    return load_keys()

def toggle_api_key(key: str, active: bool):
    keys = load_keys()
    if key in keys:
        keys[key]["active"] = active
        save_keys(keys)

def create_api_key(key: str):
    keys = load_keys()
    keys[key] = {"active": True, "requests": 0, "last_used": None}
    save_keys(keys)

def delete_api_key(key: str):
    keys = load_keys()
    if key in keys:
        del keys[key]
        save_keys(keys)
