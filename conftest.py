import pytest
import uuid
import requests
from utils.api_endpoints import BASE_URL, REGISTER

@pytest.fixture
def unique_email():
    return f"user_{uuid.uuid4().hex}@example.com"

@pytest.fixture
def test_user(unique_email):
    user_data = {
        "email": unique_email,
        "password": "SecurePass123!",
        "name": "Test User"
    }
    response = requests.post(REGISTER, json=user_data)
    return {
        **user_data,
        "accessToken": response.json()["accessToken"]
    }

@pytest.fixture
def valid_ingredients():
    response = requests.get(f"{BASE_URL}/ingredients")
    return [ingredient["_id"] for ingredient in response.json()["data"]]