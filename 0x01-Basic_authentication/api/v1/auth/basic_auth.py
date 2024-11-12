#!/usr/bin/env python3
"""
Module for Basic Authentication.
"""
from typing import TypeVar, Tuple
from base64 import b64decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    BasicAuth class for handling user authentication via Basic Auth.
    """
    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            auth_header (str): The full authorization header string.

        Returns:
            str: The Base64 encoded string after 'Basic ', or None if invalid.
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if not auth_header.startswith('Basic '):
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """
        Decodes the Base64 encoded part of the Authorization header.

        Args:
            b64_auth_header (str): Base64 encoded authorization header.

        Returns:
            str: The decoded header string in UTF-8, or None if decoding fails.
        """
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(b64_auth_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_b64_auth_header:
                                 str) -> Tuple[str, str]:
        """
        Extracts user credentials from the decoded Base64 header.

        Args:
            decoded_b64_auth_header (str): Decoded authorization header.

        Returns:
            Tuple[str, str]: User email and password.
        """
        if decoded_b64_auth_header is None or \
            not isinstance(decoded_b64_auth_header, str) \
           or ':' not in decoded_b64_auth_header:
            return (None, None)
        return decoded_b64_auth_header.split(':', 1)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.

        Args:
            user_email (str): User's email.
            user_pwd (str): User's password.

        Returns:
            User: The User object if credentials are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str) \
           or user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current authenticated user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            User: The authenticated user object if available, otherwise None.
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        extract_base64 = self.extract_base64_authorization_header(auth_header)
        decode_base64 = self.decode_base64_authorization_header(extract_base64)
        user_email, user_password = \
            self.extract_user_credentials(decode_base64)
        return self.user_object_from_credentials(user_email, user_password)
