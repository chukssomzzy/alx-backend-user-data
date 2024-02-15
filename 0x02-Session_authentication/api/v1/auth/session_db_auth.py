#!/usr/bin/env python3
"""session db authentication
"""
from datetime import datetime
from typing import Optional
from flask.app import timedelta
from flask.globals import LocalProxy
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Implements Session DB Authentication
    """
    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """Creates a session for the userid in db
        Args:
            user_id (str): the user_id to store in session
        Returns:
            - session_id
        """
        if not user_id:
            return None
        user_session = UserSession(user_id=user_id)
        try:
            user_session.save()
            return str(user_session.session_id)
        except KeyError:
            return None

    def user_id_for_session_id(self,
                               session_id: Optional[str] = None
                               ) -> Optional[str]:
        """Get user_id for the session id
        Args:
            session_id (str): user id for session id
        Returns:
            - session_id for the current user
        """
        if not session_id:
            return None
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        elif user_session.created_at + timedelta(seconds=self.session_duration
                                                 ) < datetime.now():
            user_session.remove()
            return None
        return user_session.user_id

    def destroy_session(self, request: Optional[LocalProxy] = None) -> bool:
        """Destroy a user session from storage db
        Args:
            request (LocalProxy): the current request object
        Returns:
            - True (successfully destroyed session)
            - False (unsuccessful)
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
