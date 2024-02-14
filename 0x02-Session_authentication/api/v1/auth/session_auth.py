#!/usr/bin/env python3
"""
Session authentication for simple API
"""


from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Implements session authentication for
    flask application
    """
