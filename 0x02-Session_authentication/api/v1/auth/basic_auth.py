#!/usr/bin/env python3
"""
SessionAuth class for session-based authorization.
"""
import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Manages session-based authentication for users. """

    # Dictionary mapping session IDs to user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a new session ID for a given user ID.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            str: New session ID, or None if user_id is invalid.
        """
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Fetches the user ID associated with a session ID.

        Args:
            session_id (str): Session identifier.

        Returns:
            str: Corresponding user ID, or None if session ID is invalid.
        """
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Gets the current user based on session data from the request.

        Args:
            request: HTTP request containing the session cookie.

        Returns:
            User: The user instance linked to the session, or None if not found.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id) if user_id else None

    def destroy_session(self, request=None) -> bool:
        """
        Ends a user session based on session data in the request.

        Args:
            request: HTTP request containing the session cookie.

        Returns:
            bool: True if the session was deleted, False otherwise.
        """
        if not request:
            return False
        session_cookie = self.session_cookie(request)
        if not session_cookie or not self.user_id_for_session_id(session_cookie):
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
