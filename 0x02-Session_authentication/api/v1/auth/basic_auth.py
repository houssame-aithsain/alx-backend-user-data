#!/usr/bin/env python3
"""
SessionAuth class for session-based authentication handling.
"""
import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Handles session-based authentication methods."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a new session ID for a specified user ID.

        Args:
            user_id (str): ID of the user for whom to create the session.

        Returns:
            str: The created session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Gets the user ID associated with a given session ID.

        Args:
            session_id (str): Session ID to look up.

        Returns:
            str: The user ID if the session ID is valid, otherwise None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the user associated with the session from a request.

        Args:
            request: The request object containing session data.

        Returns:
            User: The User instance linked to the session, or None if unavailable.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id) if user_id else None

    def destroy_session(self, request=None) -> bool:
        """
        Terminates the user session associated with the request.

        Args:
            request: The request object containing session data.

        Returns:
            bool: True if the session was successfully terminated, otherwise False.
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        if session_cookie not in self.user_id_by_session_id:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
