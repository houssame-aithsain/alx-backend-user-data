#!/usr/bin/env python3
"""
Defines the SessionDBAuth class that manages sessions with persistent storage
in a database.
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Implements session authentication with persistence by storing session data
    in a database.
    """

    def create_session(self, user_id=None):
        """
        Creates a Session ID for a given user_id and stores it in the database.

        Args:
            user_id (str): session is being created

        Returns:
            str: Session ID if successful, None otherwise
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()  # Persist the session data in the database
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to look up

        Returns:
            str: User ID associated with the session ID, or None if not found
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id[0].user_id  #  user_id from the session data
        return None

    def destroy_session(self, request=None):
        """
        Destroys the user session based on the session.

        Args:
            request: The request object containing the session cookie

        Returns:
            bool: True if the session was successfully destroyed
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if user_session:
            user_session[0].remove()  # Remove the session from the database
            return True
        return False
