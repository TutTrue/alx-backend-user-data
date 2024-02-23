#!/usr/bin/env python3
import requests


def register_user(email: str, password: str) -> None:
    """Register a user"""
    url = "http://localhost:5000/users"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("User registered")


def log_in_wrong_password(email: str, password: str) -> None:
    """Log in with wrong password"""
    url = "http://localhost:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 401
    print("Log in failed")


def profile_unlogged() -> None:
    """Profile of an unlogged user"""
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403
    print("Profile unlogged")


def log_in(email: str, password: str) -> str:
    """Log in"""
    url = "http://localhost:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Log in successful")
    return response.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """Profile of a logged user"""
    url = "http://localhost:5000/profile"
    cookies = {
        "session_id": session_id
    }
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    print("Profile logged")


def log_out(session_id: str) -> None:
    """Log out"""
    url = "http://localhost:5000/sessions"
    cookies = {
        "session_id": session_id
    }
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200
    print("Log out successful")


def reset_password_token(email: str) -> str:
    """Reset password token"""
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url, data=data)
    assert response.status_code == 200
    print("Reset password token sent")
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password"""
    url = "http://localhost:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    print("Password updated")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
