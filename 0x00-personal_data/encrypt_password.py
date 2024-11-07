#!/usr/bin/env python3
"""Module for securely hashing and verifying passwords."""

import bcrypt


def hash_password(password: str) -> bytes:
    """Generates a hashed password with salt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a given password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
