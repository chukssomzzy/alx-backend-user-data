#!/usr/bin/env python3
"""Models user session"""


from typing import Dict, List
import uuid
from models.base import Base


class UserSession(Base):
    """Defines Usersession Models
    """
    def __init__(self, *args: List, **kwargs: Dict) -> None:
        """Initializes the user session models
        Args:
            args (list): contains args to initilize the session
            kwargs (dict):  kwargs to initialize the session
        Returns:
            - (None) on success
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
