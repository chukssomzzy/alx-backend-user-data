#!/usr/bin/env python3
"""Implements auth routes
"""
from os import getenv
from flask import jsonify, make_response, request
from werkzeug.exceptions import abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """Login authentication route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    elif not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({'error': "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({'error': "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user_id=str(user.id))
    resp = make_response(user.to_json())
    session_name = getenv('SESSION_NAME')
    if not session_name:
        abort(500)
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route('/auth_session/logout',
                 methods=["DELETE"], strict_slashes=False)
def logout():
    """Delete a user from a session
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return {}
