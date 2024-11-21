#!/usr/bin/env python3
"""
A simple Flask app for user authentication management.
"""
import logging
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth

# Disabling warning logs for cleaner output
logging.disable(logging.WARNING)

# Initialize the Auth class and Flask application
AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home_page() -> str:
    """Handle GET requests to the root endpoint.

    Returns:
        - JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """Handle POST requests to register a new user.
    Returns:
        - JSON response with the registration status.
    """
    email, password = request.form.get("email"), request.form.get("password")

    try:
        # Attempt to register the user
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        # If email is already registered, return error response
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login_user() -> str:
    """Handle POST requests to log in a user.

    Returns:
        - JSON response with login status and session cookie.
    """
    email, password = request.form.get("email"), request.form.get("password")

    if not AUTH.valid_login(email, password):
        # Invalid credentials, return unauthorized error
        abort(401)

    # Create a session and return response with session cookie
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout_user() -> str:
    """Handle DELETE requests to log out a user.

    Returns:
        - Redirects to the home page if successful.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # Unauthorized user, abort with forbidden error
        abort(403)

    # Destroy the session and redirect to home page
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def get_user_profile() -> str:
    """Handle GET requests to retrieve user profile.
    Returns:
        - JSON response with user's email if logged in.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # Unauthorized access, abort with forbidden error
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def request_password_reset() -> str:
    """Handle POST requests to generate a password reset token.

    Returns:
        - JSON response with email and reset token if successful.
    """
    email = request.form.get("email")

    try:
        # Generate a reset token for the provided email
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # Invalid email, return forbidden error
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_user_password() -> str:
    """Handle PUT requests to update the user's password.
    Returns:
        - JSON response confirming the password update.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        # Attempt to update the password with the provided new password
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # Invalid reset token, return forbidden error
        abort(403)

    return jsonify({"email": email,
                    "message": "Password updated successfully"})


if __name__ == "__main__":
    # Run the Flask app on all available IP addresses and port 5000
    app.run(host="0.0.0.0", port=5000)
