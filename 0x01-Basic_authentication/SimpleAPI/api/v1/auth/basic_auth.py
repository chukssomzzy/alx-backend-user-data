#!/usr/bin/env python3
"""Basic Auth"""


from typing import Optional
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Implements basic_authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> Optional[str]:
        """Extract the content of base64 authorization header from the
        header value
        Args:
            authorization_header (str): contains base64 authorization
            credentials
        Returns:
            - base64 content after BASIC
        """
        if not authorization_header or type(authorization_header) is not str \
                or not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
