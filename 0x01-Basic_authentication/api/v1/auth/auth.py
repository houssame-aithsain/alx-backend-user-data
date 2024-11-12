#!/usr/bin/env python3
"""
API authentication management module.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication methods.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a path requires authentication based on excluded paths.

        Args:
            path (str): The requested path.
            excluded_paths (List[str]): List of paths.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Ensure path and excluded paths end with '/'
        if path[-1] != '/':
            path += '/'
        excluded_paths = [p if p[-1] == '/' else p + '/'
                          for p in excluded_paths]

        # Handle wildcard paths ending with '*'
        wildcard_paths = [p[:-1] for p in excluded_paths if p.endswith('*')]
        for wp in wildcard_paths:
            if path.startswith(wp):
                return False

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from a request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the 'Authorization' header if present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current authenticated user.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated user object if available, otherwise None.
        """
        return None
