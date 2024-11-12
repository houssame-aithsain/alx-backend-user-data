#!/usr/bin/env python3
"""
Module for Index views, handling various endpoints.
"""
from flask import jsonify, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Returns:
      - JSON with API status.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Returns:
      - JSON with the count of each object type.
    """
    stats = {'users': User.count()}
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """
    GET /api/v1/unauthorized
    Triggers:
      - 401 Unauthorized error for testing.
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """
    GET /api/v1/forbidden
    Triggers:
      - 403 Forbidden error for testing.
    """
    abort(403)
