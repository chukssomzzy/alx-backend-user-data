#!/usr/bin/env python3
"""
Session authentication for simple API
"""


from os import getenv
from typing import Optional
import uuid

from flask.globals import LocalProxy
from api.v1.auth.auth import Auth
from models.user import User


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

    def user_id_for_session_id(self,
                               session_id: Optional[str] = None
                               ) -> Optional[str]:
        """Get a user_id associated with a session id"""
        if not session_id or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request: Optional[LocalProxy]
                     = None) -> Optional[User]:
        """Get a user instance for the current request
        Args:
            request (LocalProxy): request object containing information of the
                request
        Returns:
            - user instance
            - None (error)
        """
        if not request or not request.cookies:
            return None
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        if not user_id or type(user_id) is not str:
            return None
        user = User.get(user_id)
        if isinstance(user, User):
            return user
        return None

    def destroy_session(self, request: Optional[LocalProxy] = None) -> bool:
        """Destroy the user session on logout
        Args:
            request (LocalProxy): localproxy to the request object
        Returns:
            - bool
        """
        session_name = getenv("SESSION_NAME")
        if not session_name or not request or not self.session_cookie(request):
            return False
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
