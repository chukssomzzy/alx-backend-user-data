#!/usr/bin/env python3
""" Auth Module
"""
from typing import Optional
import uuid
import bcrypt
from sqlalchemy.exc import InvalidRequestError
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


def _generate_uuid() -> str:
    """Generate a uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a password is valid for a user identified by email
        Args:
            email (str): user email
            password (str): user password
        Returns:
            - True: valid password for user
            - False: invalid password for user
        """
        try:
            if not email or not password:
                return False
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except (ValueError, NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Creates a session
        Args:
            email (str): create a session for the current user
        Returns:
            - session_id (str): user session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (ValueError, NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Get a user attached to a session id"""
        try:
            if not session_id:
                return None
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id):
        """Destroy the session attached to a user
        Args:
            user_id (any): identifier for the user
        Returns:
            - None
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except (NoResultFound, InvalidRequestError):
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate and set user reset password token
        Args:
            email (str): user email
        Returns:
            - The reset token
        """
        try:
            if not email:
                raise ValueError
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: Optional[str],
                        password: Optional[str]) -> None:
        """Update a user password
        Args:
            reset_token (str): A user reset token
            password (str): Password to update on
        Returns:
            - None
        """
        try:
            if type(reset_token) is not str or type(password) is not str:
                raise ValueError
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 reset_token=None,
                                 hashed_password=_hash_password(password).
                                 decode("utf-8"))
        except (NoResultFound, InvalidRequestError):
            raise ValueError
