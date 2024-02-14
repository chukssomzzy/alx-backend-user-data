#!/usr/bin/env python3
"""Implements authentication"""
from typing import List, Optional, TypeVar
from flask import Request

User = TypeVar('User')


class Auth:
    """Authentication Class"""
    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """Path requiring auth

        Returns:
            bool
        """
        if not path or not excluded_path:
            return True
        if path[-1] != '/':
            path += '/'
        if path.endswith('*') and \
                any(p.startswith(path[:-1]) for p in excluded_path):
            return False
        if path in excluded_path:
            return False
        else:
            return True

    def authorization_header(self, request=None
                             ) -> Optional[str]:
        """authorization header
        """
        if not request or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """Get current User"""
        return None
