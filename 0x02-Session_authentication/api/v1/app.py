#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Any
from typing_extensions import Tuple
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
excluded_path = ['/api/v1/status/', '/api/v1/unauthorized/',
                 '/api/v1/forbidden/', '/api/v1/auth_session/login/']

if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    from models.user_session import UserSession
    UserSession.load_from_file()
    auth = SessionDBAuth()


@app.before_request
def authorize_request():
    """Authorize the request before_been handled
    """
    if not auth or not auth.require_auth(request.path,
                                         excluded_path=excluded_path):
        return None
    if not auth.authorization_header(request) \
            and not auth.session_cookie(request):
        abort(401)
    current_user = auth.current_user(request)
    if not current_user:
        abort(403)
    request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> Tuple[Any, int]:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> Tuple[Any, int]:
    """
    Not authorized to handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_handler(error) -> Tuple[Any, int]:
    """
    Resource Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
