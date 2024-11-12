#!/usr/bin/env python3
"""
API Routing module.
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# Initialize authentication type based on environment variable
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()


@app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """Handles 401 Unauthorized errors with a JSON response."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """Handles 403 Forbidden errors with a JSON response."""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def handle_not_found(error) -> str:
    """Handles 404 Not Found errors with a JSON response."""
    return jsonify({"error": "Not found"}), 404


@app.before_request
def authenticate_user():
    """
    Authenticates user before processing each request.
    If authentication is required but missing.
    """
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            if auth_header is None:
                abort(401)
            if user is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
