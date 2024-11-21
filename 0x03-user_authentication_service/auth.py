#!/usr/bin/env python3
"""
Authentication module for managing user registration.
"""
import bcrypt
from db import DatabaseManager
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


class AuthenticationService:
    """
    A class to handle authentication operations, including user registration,
    login, session management, and password resets.
    """

    def __init__(self):
        """
        Initializes an instance of AuthenticationService.
        Sets up a database connection.
        """
        self._db_manager = DatabaseManager()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the system.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The newly created User instance.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            self._db_manager.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db_manager.add_user(email, hashed_password)
        raise ValueError(f"User with email {email} already exists.")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Verifies user credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if credentials are valid, otherwise False.
        """
        try:
            user = self._db_manager.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID for the user.
        """
        try:
            user = self._db_manager.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db_manager.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user associated with a given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The user associated with the session ID.
        """
        if not session_id:
            return None
        try:
            return self._db_manager.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Ends a user's session.

        Args:
            user_id (int): The ID of the user whose session.
        """
        self._db_manager.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: A password reset token.

        Raises:
            ValueError: If the email is not associated with any user.
        """
        try:
            user = self._db_manager.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User with the provided email does not exist.")
        reset_token = _generate_uuid()
        self._db_manager.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """
        Updates a user's password using a reset token.

        Args:
            reset_token (str): The reset token provided to the user.
            new_password (str): The new password to set.

        Raises:
            ValueError: If the reset token is invalid or not found.
        """
        try:
            user = self._db_manager.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token.")
        hashed_password = _hash_password(new_password)
        self._db_manager.update_user(user.id, hashed_password=hashed_password,
                                     reset_token=None)


def _hash_password(password: str) -> bytes:
    """
    Hashes a password for secure storage.

    Args:
        password (str): The plain-text password.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a unique identifier.

    Returns:
        str: A new UUID as a string.
    """
    return str(uuid4())
