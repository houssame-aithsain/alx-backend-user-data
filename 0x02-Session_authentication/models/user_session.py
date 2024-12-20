#!/usr/bin/env python3
""" UserSession module that defines a class for user session management.
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class represents a session for a user in the system.
    It contains attributes such as user_id and session_id.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a UserSession instance with user_id and session_id.

        Args:
            *args: Variable length argument
            **kwargs: Dictionary of keyword.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')  # User ID
        self.session_id = kwargs.get('session_id')  # Unique session
