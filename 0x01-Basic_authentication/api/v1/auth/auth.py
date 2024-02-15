#!/usr/bin/env python3
""" Module of API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class for API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that require authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that handles authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that handles current user
        """
        return None
