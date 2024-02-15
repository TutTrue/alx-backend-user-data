#!/usr/bin/env python3
""" Module of API authentication
"""
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """ Class for Basic API authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Method that extracts base64 authorization header
        """
        if authorization_header is None or \
                type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ Method that decodes base64 authorization header
        """
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None
        try:
            import base64
            return base64.b64decode(base64_authorization_header). \
                decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Method that extracts user credentials
        """
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Method that returns user object from credentials
        """
        if user_email is None or type(user_email) is not str or \
                user_pwd is None or type(user_pwd) is not str:
            return None
        from models.user import User
        try:
            user = User.search({'email': user_email})[0]
        except Exception:
            return None
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that overloads Auth and retrieves current user
        """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(base64_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
