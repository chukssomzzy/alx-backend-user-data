#!/usr/bin/env python3
"""Session authentication with sessin expiring date
"""


from datetime import datetime, timedelta
from os import getenv
from typing import Optional
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Implementations Session auth with expiration date
    """
    def __init__(self):
        """Initialize the session auth with expiration date
        """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """Create a session that expires after the session duration
        Args:
            user_id (str): user id to add to session dict
        Returns:
            - session_id (str) of the session key
            - (None) on error
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id:
                               Optional[str] = None) -> Optional[str]:
        """Get userid from session if the current session hasn't expired
        Args:
            session_id (str): session dict key
        Returns:
            - user_id from the sesion
            - (None) if session is expired
        """
        if not session_id or session_id not in self.user_id_by_session_id:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        elif not session_dict.get('created_at'):
            return None
        elif session_dict['created_at'] + timedelta(seconds=self.
                                                    session_duration
                                                    ) < datetime.now():
            return None
        return session_dict["user_id"]
