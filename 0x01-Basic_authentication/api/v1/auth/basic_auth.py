#!/usr/bin/env python3
""" Module of API authentication
"""
from api.v1.auth.auth import Auth


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
