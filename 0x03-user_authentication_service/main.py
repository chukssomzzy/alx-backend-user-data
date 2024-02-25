#!/usr/bin/env python3
"""
Main file
"""
import requests
base_url = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, passwd: str) -> None:
    """Text Register User endpoint with requests"""
    expect_json = {"email": email, "message": "user created"}
    expect_json_error = {"message": "email already registered"}

    r = requests.post(base_url + "/users",
                      data={"email": email, "password": passwd})
    assert r.json() == expect_json
    assert r.status_code == 200

    r = requests.post(base_url + "/users",
                      data={"email": email, "password": passwd})
    assert r.json() == expect_json_error
    assert r.status_code == 400

    r = requests.post(base_url + "/users",
                      data={"email": email})

    assert r.status_code == 400


def log_in_wrong_password(email: str, new_passwd: str) -> None:
    """Test login with a new user with wrong password"""
    r = requests.post(base_url + "/sessions",
                      data={"email": email, "password": new_passwd})
    assert r.cookies.get("session_id") is None
    assert r.status_code == 401


def profile_unlogged():
    """Test profile access before login"""
    r = requests.get(base_url + "/profile")
    assert r.status_code == 403


def log_in(email: str, password: str) -> str:
    """Login a user
    Args:
        email (str): user email
        password (str): user password
    Returns:
        - return session_id cookie value
    """
    r = requests.post(base_url + '/sessions', data={"email": email,
                                                    "password": password})
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """Login a profile  with session_id
    """
    r = requests.get(base_url + "/profile", cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """Test logout session
    """
    r = requests.delete(base_url + "/sessions",
                        cookies={"session_id": session_id},
                        allow_redirects=False)
    assert r.status_code == 302
    r = requests.delete(base_url + "/sessions",
                        cookies={"session_id": session_id})
    assert r.status_code == 403


def reset_password_token(email: str) -> str:
    """Reset password token
    """
    r = requests.post(base_url + "/reset_password", data={"email": email})
    assert r.status_code == 200
    reset_token = r.json()["reset_token"]
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update a user  password
    Args:
        email (str): user email address
        reset_token (str): password reset token
        new_password (str): password to reset token with
    Returns:
        - None
    """
    r = requests.put(base_url + "/reset_password",
                     data={"email": email, "password": new_password,
                           "reset_token": reset_token})
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}

    r = requests.put(base_url + "/reset_password")
    assert r.status_code == 403


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
