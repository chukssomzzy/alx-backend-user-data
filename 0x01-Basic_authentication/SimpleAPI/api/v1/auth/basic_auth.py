#!/usr/bin/env python3
"""Basic Auth"""


import base64
import binascii
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> Optional[str]:
        """Decode the content of basic auth header
        Args:
            base64_authorization_header (str): base64 bytes of base64 header
        Returns:
            - returns the decoded str
            - return None on error
        """
        if not base64_authorization_header or type(base64_authorization_header
                                                   ) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header)\
                .decode('utf-8')
        except binascii.Error:
            return None
