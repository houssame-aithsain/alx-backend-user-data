"""Authentication module to manage user registration."""

import logging
from typing import Union
from uuid import uuid4

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User

logging.disable(logging.WARNING)


def hash_password(plain_password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        plain_password (str): The plain text password.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())


def generate_uuid() -> str:
    """Generates a unique identifier.

    Returns:
        str: A string representation of the new UUID.
    """
    return str(uuid4())


class Auth:
    """Handles user authentication operations: registration."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, plain_password: str) -> User:
        """Registers a new user with an email and password.

        Args:
            email (str): The user's email.
            plain_password (str): The user's plain text password.

        Returns:
            User: The registered user object.

        Raises:
            ValueError: If the email is already registered.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User with email {email} already exists")
        except NoResultFound:
            pass

        hashed_password = hash_password(plain_password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, plain_password: str) -> bool:
        """Validates a user's login credentials.

        Args:
            email (str): The user's email.
            plain_password (str): The user's plain text password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(plain_password.encode('utf-8'),
                                      user.hashed_password)
        except NoResultFound:
            return False

        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user and returns a session ID.

        Args:
            email (str): The user's email.

        Returns:
            str: The new session ID or None if user not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Fetches a user associated with the given session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User or None: The user object or None if not found.
        """
        if not session_id:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the given user ID.

        Args:
            user_id (int): The user's ID.
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for the given email.

        Args:
            email (str): The user's email.

        Raises:
            ValueError: If no user is found for the email.

        Returns:
            str: The reset token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User with this email does not exist")

        reset_token = generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Updates the password for a user using a reset token.

        Args:
            reset_token (str): The reset token.
            new_password (str): The new password to be set.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        new_hashed_password = hash_password(new_password)
        self._db.update_user(user.id, hashed_password=new_hashed_password,
                             reset_token=None)
