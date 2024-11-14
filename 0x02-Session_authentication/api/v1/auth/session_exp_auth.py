#!/usr/bin/env python3
"""
Define SessionExpAuth class
"""
import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Class that adds an expiration date to a Session ID for session management.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth class with a session duration.
        """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID for a given user ID, adding an expiration timestamp.

        Args:
            user_id (str): User's ID

        Returns:
            str: Session ID, or None if user_id is invalid
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
        Retrieves a user ID based on the session ID, considering session expiration.
        
        Args:
            session_id (str): The session ID
        
        Returns:
            str: User ID if session is valid, otherwise None
        """
        if session_id is None:
            return None

        user_details = self.user_id_by_session_id.get(session_id)
        if not user_details or "created_at" not in user_details:
            return None

        if self.session_duration <= 0:
            return user_details.get("user_id")

        created_at = user_details["created_at"]
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_details.get("user_id")
