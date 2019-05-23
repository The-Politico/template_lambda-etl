import os
from functools import wraps
from flask import request, Response


def token_authed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.headers.get("Authorization").split()[1]
        except Exception:
            return Response("", status=403)
        if token == os.getenv("API_VERIFICATION_TOKEN"):
            return f(*args, **kwargs)

        return Response("", status=403)

    return decorated_function
