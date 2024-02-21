#!/usr/bin/env python3
""" Auth Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password and return a byte string of hashed password
    Args:
        password (str): The string representation of the password
    Returns:
        - bytes (on success)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
