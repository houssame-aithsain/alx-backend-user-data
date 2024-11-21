#!/usr/bin/env python3
"""Module for end-to-end (E2E) integration tests for the `app.py` application.
"""

import requests
from app import AUTH

# Constants for test email, password, and base URL
TEST_EMAIL = "houssameaithsain@holberton.com"
TEST_PASSWORD = "ara3lihachiALX"
NEW_TEST_PASSWORD = "gfgfgfgfgS10"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration endpoint.

    Args:
        email (str): The user's email.
        password (str): The user's password.
    """
    url = f"{BASE_URL}/users"
    data = {
        "email": email,
        "password": password
    }
    # Attempt to register a new user
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    # Attempt to register the same user again (should fail)
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def attempt_login_with_wrong_password(email: str, password: str) -> None:
    """Test login attempt with an incorrect password.

    Args:
        email (str): The user's email.
        password (str): The incorrect password.
    """
    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 401


def test_profile_access_without_login() -> None:
    """Test profile access without being logged in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403


def test_profile_access_with_login(session_id: str) -> None:
    """Test profile access with a valid session ID.

    Args:
        session_id (str): The session ID of the logged-in user.
    """
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200

    payload = response.json()
    assert "email" in payload

    user = AUTH.get_user_from_session_id(session_id)
    assert user.email == payload["email"]


def logout_user(session_id: str) -> None:
    """Test the logout process.

    Args:
        session_id (str): The session ID of the user to log out.
    """
    url = f"{BASE_URL}/sessions"
    headers = {"Content-Type": "application/json"}
    data = {"session_id": session_id}
    response = requests.delete(url, headers=headers, cookies=data)
    assert response.status_code == 200


def request_password_reset(email: str) -> str:
    """Test the password reset process by requesting a reset token.

    Args:
        email (str): The user's email to request a password reset.
    """
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == email

    reset_token = response.json()["reset_token"]
    return reset_token


def update_user_password(email: str, reset_token: str,
                         new_password: str) -> None:
    """Test the process of updating the user's password using a reset token.

    Args:
        email (str): The user's email whose password needs to be updated.
        reset_token (str): The reset token generated for the user.
        new_password (str): The new password to set for the user.
    """
    url = f"{BASE_URL}/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated"
    assert response.json()["email"] == email


def login_user(email: str, password: str) -> str:
    """Test the login process and return the session ID.

    Args:
        email (str): The user's email to log in.
        password (str): The user's password.
    """
    url = f"{BASE_URL}/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)

    if response.status_code == 401:
        return "Invalid credentials"

    assert response.status_code == 200
    response_json = response.json()
    assert "email" in response_json
    assert "message" in response_json
    assert response_json["email"] == email

    return response.cookies.get("session_id")


if __name__ == "__main__":
    # Run all the test functions
    register_user(TEST_EMAIL, TEST_PASSWORD)
    attempt_login_with_wrong_password(TEST_EMAIL, NEW_TEST_PASSWORD)
    test_profile_access_without_login()

    session_id = login_user(TEST_EMAIL, TEST_PASSWORD)
    test_profile_access_with_login(session_id)
    logout_user(session_id)

    reset_token = request_password_reset(TEST_EMAIL)
    update_user_password(TEST_EMAIL, reset_token, NEW_TEST_PASSWORD)
    login_user(TEST_EMAIL, NEW_TEST_PASSWORD)
