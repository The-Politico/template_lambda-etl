import os
from functools import wraps
from flask import request, jsonify


def token_authed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # literal "Token" plus whitespace, e.g., "Token <AUTHTOKEN>"
            token = request.headers.get("Authorization", "").split()[1]
        except IndexError:
            response = jsonify(
                {"msg": "No auth token or incorrect token format provided"}
            )
            response.status_code = 401
            return response

        if token != os.getenv("API_AUTH_TOKEN", ""):
            response = jsonify({"msg": "Not authorized"})
            response.status_code = 403
            return response

        return f(*args, **kwargs)

    return decorated_function
