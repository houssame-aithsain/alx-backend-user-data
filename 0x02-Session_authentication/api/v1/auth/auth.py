#!/usr/bin/env python3
"""
Auth class for managing API authentication.
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Handles API authentication mechanisms and utilities."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a given path requires authentication.

        Args:
            path (str): The URL path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i.endswith("*") and path.startswith(i[:-1]):
                return False
            if i.startswith(path) or path.startswith(i):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from a request.

        Args:
            request: The request object from which to get the header.

        Returns:
            str: The authorization header if present, otherwise None.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder for retrieving the current user based on request data.

        Args:
            request: The request object containing user data.

        Returns:
            User: The current user instance, or None if not implemented.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from a request.

        Args:
            request: The request object containing cookie data.
        Returns:
            str: The session cookie value if present, otherwise None.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
