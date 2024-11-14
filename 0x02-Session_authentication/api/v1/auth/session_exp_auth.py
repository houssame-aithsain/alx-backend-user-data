#!/usr/bin/env python3
"""
SessionExpAuth class for session handling with expiration.
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Manages sessions with an expiration time.
    """

    def __init__(self):
        """
        Sets the session duration from environment variables, defaulting to 0.
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session ID with an expiration timestamp for a user.

        Args:
            user_id (str): The ID of the user

        Returns:
            str: The session ID, or None if user_id is invalid.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID for a session, considering expiration.

        Args:
            session_id (str): The session ID

        Returns:
            str: User ID if session is valid, otherwise None.
        """
        if session_id is None:
            return None

        user_details = self.user_id_by_session_id.get(session_id)
        if not user_details or "created_at" not in user_details:
            return None

        # Check if session is expired
        if self.session_duration <= 0:
            return user_details.get("user_id")

        created_at = user_details["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_details.get("user_id")
