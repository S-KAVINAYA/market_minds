import requests

BASE_URL = "http://backend-api-url"  # Replace later

# Temporary in-memory storage (for demo only)
MANAGERS = {}

def signup_manager_api(username, password):

    if username in MANAGERS:
        return {"status": "error", "message": "Manager already exists"}

    MANAGERS[username] = password
    return {"status": "success"}


def login_manager_api(username, password):

    if username in MANAGERS and MANAGERS[username] == password:
        return {"status": "success", "manager_id": username}

    return {"status": "error", "message": "Invalid credentials"}


# BACKEND DATA FETCH
def fetch_clients(manager_id):
    """
    This will later call backend.
    For now, returning dummy structure.
    """

    return [
        {
            "client_id": "C101",
            "risk_level": "High",
            "risk_asset": "Stocks",
            "invested_value": 100000,
            "current_value": 87000
        },
        {
            "client_id": "C102",
            "risk_level": "Moderate",
            "risk_asset": "ETFs",
            "invested_value": 150000,
            "current_value": 140000
        }
    ]
