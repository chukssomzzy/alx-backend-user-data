#!/usr/bin/env python3
"""Implements a password hasher"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password and returns a salted hash of
    password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
