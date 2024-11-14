#!/usr/bin/env python3
""" Module for User views """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Returns:
      - JSON list of all User objects
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - user_id: User ID
    Returns:
      - JSON representation of the User object
      - 404 if User ID doesn't exist or is invalid
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - user_id: User ID
    Returns:
      - Empty JSON if User was successfully deleted
      - 404 if User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email (required)
      - password (required)
      - last_name (optional)
      - first_name (optional)
    Returns:
      - JSON representation of the new User object
      - 400 if there is an error in creation
    """
    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': "Wrong format"}), 400
        if "email" not in rj or rj["email"] == "":
            return jsonify({'error': "email missing"}), 400
        if "password" not in rj or rj["password"] == "":
            return jsonify({'error': "password missing"}), 400

        user = User()
        user.email = rj.get("email")
        user.password = rj.get("password")
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201

    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - user_id: User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Returns:
      - JSON representation of the updated User object
      - 404 if User ID doesn't exist
      - 400 if there is an error in updating the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    try:
        rj = request.get_json()
        if not rj:
            return jsonify({'error': "Wrong format"}), 400

        if 'first_name' in rj:
            user.first_name = rj['first_name']
        if 'last_name' in rj:
            user.last_name = rj['last_name']
        user.save()
        return jsonify(user.to_json()), 200

    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
