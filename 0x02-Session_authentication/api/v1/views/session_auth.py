#!/usr/bin/env python3
""" Module of session auth view
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from api.v1.auth.session_auth import SessionAuth


sa = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """ Auth session login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = sa.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie('session_id', session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_logout() -> str:
    """ Auth session logout
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return jsonify({"error": "session_id for cookie not found"}), 403
    user = sa.current_user(request)
    if not user:
        return jsonify({"error": "no user found"}), 403
    sa.destroy_session(request)
    return jsonify({}), 200


@app_views.route('/auth_session/profile', methods=['GET'],
                 strict_slashes=False)
def auth_session_profile() -> str:
    """ Auth session profile
    """
    user = sa.current_user(request)
    if not user:
        return jsonify({"error": "no user found"}), 403
    return jsonify(user.to_json()), 200


@app_views.route('/auth_session/destroy', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_destroy() -> str:
    """ Auth session destroy
    """
    user = sa.current_user(request)
    if not user:
        return jsonify({"error": "no user found"}), 403
    sa.destroy_session(request)
    return jsonify({}), 200
