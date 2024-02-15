#!/usr/bin/env python3
""" Module of API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Class for API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that require authentication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*') and path.startswith(p[:-1]) or path == p:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header
        """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that handles current user
        """
        return None

    def session_cookie(self, request=None):
        """ Method that handles session cookie
        """
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
