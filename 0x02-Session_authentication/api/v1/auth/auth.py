#!/usr/bin/env python3
"""
Implements authentication
"""
from os import getenv
from typing import List, Optional, TypeVar

from flask.globals import LocalProxy


User = TypeVar('User')


class Auth:
    """Authentication Class"""
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """Path requiring auth

        Returns:
            - bool
        """
        if not path or not excluded_path:
            return True
        if path[-1] != '/':
            path += '/'
        wildcard_excluded_path = [p for p in excluded_path if p.endswith('*')]
        if any(path.startswith(p[:-1]) for p in wildcard_excluded_path):
            return False
        if path in excluded_path:
            return False
        else:
            return True

    def authorization_header(self, request=None
                             ) -> Optional[str]:
        """authorization header
        returns:
            - Auth header from request
        """
        if not request or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Get current User
        Returns:
            - None
        """
        return None

    def session_cookie(self, request: Optional[LocalProxy]) -> Optional[str]:
        """Get a session_id value from a request object
        Args:
            request (LocalProxy): request object
        Returns:
            - The content of session_key in the cookie
            - None on error
        """
        cookie_name = getenv("SESSION_NAME")
        if not cookie_name or not request:
            return None
        return request.cookies.get(cookie_name)




