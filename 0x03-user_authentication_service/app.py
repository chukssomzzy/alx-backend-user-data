#!/usr/bin/env python3
"""Implements flask endpoints"""
from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
