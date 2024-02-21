#!/usr/bin/env python3
""" Auth Module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password and return a byte string of hashed password
    Args:
        password (str): The string representation of the password
    Returns:
        - bytes (on success)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Intialize auth class"""
        self._db = DB()

    def register_user(self, email, password):
        """Register a user in the user management service
        Args:
            email (str):  user email
            password (str): user password to be hashed
        Returns:
            - User object
        Exceptions:
            - ValueError: if the user  already exit in DB
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            return self._db.add_user(email,
                                     _hash_password(password).decode('utf-8'))
