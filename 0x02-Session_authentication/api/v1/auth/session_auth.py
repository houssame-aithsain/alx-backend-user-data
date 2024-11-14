#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Implements Session Authorization protocol methods """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new Session ID for a given user ID.

        Args:
            user_id (str): The user's ID

        Returns:
            str: Session ID as a string, or None if user_id is invalid
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on a given session ID.

        Args:
            session_id (str): The session ID

        Returns:
            str: User ID or None if session_id is invalid
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session cookie.

        Args:
            request: The request object containing the session cookie
        Returns:
            User: The User instance associated with the session
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id) if user_id else None

    def destroy_session(self, request=None) -> bool:
        """
        Deletes the user session associated with the request.

        Args:
            request: The request object containing the session cookie

        Returns:
            bool: True if session was successfully deleted, False otherwise
        """
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
