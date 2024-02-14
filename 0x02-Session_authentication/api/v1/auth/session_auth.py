#!/usr/bin/env python3
"""
Session authentication for simple API
"""


from typing import Optional
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Implements session authentication for
    flask application
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """Create a inmemory login session for each authenticated user
        Args:
            user_id (str): the authenticated user id
        Returns:
            - (str) The session id
            - (None) on error
        """
        if not user_id or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
