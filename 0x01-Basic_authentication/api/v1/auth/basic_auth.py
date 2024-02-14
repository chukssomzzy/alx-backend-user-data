#!/usr/bin/env python3
"""
Basic Auth Implemetation
"""
import base64
import binascii
from typing import Optional, Tuple, TypeVar, Union

from flask.globals import LocalProxy
from api.v1.auth.auth import Auth
from models.user import User

U = TypeVar('U')


class BasicAuth(Auth):
    """
    Implements basic_authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: Optional[str]
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
                                           base64_authorization_header:
                                           Optional[str]
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
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 Optional[str]
                                 ) -> Tuple[Optional[str], Optional[str]]:
        """Extact username or password from the decoded str
        Args:
            decoded_base64_authorization_header (str): the string to extract
            login credentials from
        Returns:
            - Tuple of username and password
            - None on error
        """
        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) is not str or \
                ":" not in decoded_base64_authorization_header:
            return None, None
        user_email = decoded_base64_authorization_header.split(':')[0]
        user_pass = decoded_base64_authorization_header[(len(user_email) + 1):]
        return user_email, user_pass

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> Optional[U]:
        """Returns user instance based on the credentials user_email and
        user_pwd
        Args:
            user_email (str): the user email
            user_pwd (str): The user password
        Returns:
            - The user instance
            - None on error
        """
        if not user_email or not user_pwd or \
                not User.count() or \
                not User.search({"email": user_email}):
            return None
        user = User.search({"email": user_email})[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request: Optional[LocalProxy]
                     = None) -> Union[U, None]:
        """Return current login user object
        Args:
            request (Request): request object
        Returns:
            - A user object
        """
        if not request:
            return None
        auth_header = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(auth_header)
        auth_header = self.decode_base64_authorization_header(auth_header)
        user_cred = self.extract_user_credentials(auth_header)
        if user_cred:
            return self.user_object_from_credentials(*user_cred)
        return None
