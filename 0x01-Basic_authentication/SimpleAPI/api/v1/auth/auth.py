#!/usr/bin/env python3
"""Implements authentication"""
from typing import List, TypeVar
from flask import request

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
        if path in excluded_path:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """authorization header
        """
        return None

    def current_user(self, request=None) -> User:
        """Get current User"""
        return None
