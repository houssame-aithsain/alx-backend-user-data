#!/usr/bin/env python3
"""
SessionAuth class for managing session-based authentication.
"""
import base64
from uuid import uuid4
from typing import Optional
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session-based authentication manager."""

    user_id_by_session_id = {}

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create a session ID for a given user ID.

        Args:
            user_id (str): Unique identifier for the user.

        Returns:
            str: New session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: Optional[str] = None) -> Optional[str]:
        """
        Retrieve the user ID associated with a session ID.

        Args:
            session_id (str): Session identifier.

        Returns:
            str: Corresponding user ID, or None if session ID is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieve the current user based on session data from the request.

        Args:
            request: HTTP request containing the session cookie.

        Returns:
            User: User instance linked to the session, or None if not found.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id) if user_id else None

    def destroy_session(self, request=None) -> bool:
        """
        End a user session based on session data in the request.

        Args:
            request: HTTP request containing the session cookie.

        Returns:
            bool: True if the session was deleted, False otherwise.
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
