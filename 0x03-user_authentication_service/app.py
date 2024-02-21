#!/usr/bin/env python3
"""Implements flask endpoints"""
from flask import (Flask, Response, abort, jsonify, make_response, redirect,
                   request, url_for)

from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", strict_slashes=False)
def index():
    """A basic flask endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"], strict_slashes=False)
def users():
    """Register user endpoint
    Forms:
        email (str): user email
        password (str): user password
    Response:
        200:
            registeredUser:
                email: str
                message: str
        400:
            alreadyRegisteredUser:
                message: str
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> Response:
    """Login a user to the user management service
    Forms:
        email (str): the user email
        password (str): the user password
    Response:
        200:
            userLogged:
                email: str
                message: str
        401:
            None
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password or not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    if not session_id:
        abort(401)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """Delete a  users session
    Redirects:
        - Home route
    Response:
        403:
            None
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = auth.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)
    auth.destroy_session(user_id=user.id)
    return redirect(url_for('index'))


@app.route('/profile', strict_slashes=False)
def profile() -> Response:
    """Get a user profile information
    Response:
        200:
            user_profile:
                email: str
        403:
            None
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = auth.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)
    return jsonify({'email': user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
