from time import time
from functools import wraps
from toolbox.slack.verify import verify_signature


def slack_signed(f):
    """Authentication decorator.
    Verifies Slack Events API requests using signing secrets.
    Make sure `SLACK_SIGNING_SECRET` environment variable is set.
    See details:
    - https://api.slack.com/docs/verifying-requests-from-slack
    - https://www.django-rest-framework.org/api-guide/authentication/
    Example:
        ```
        @app.route("events-api/", methods=["POST"])
        @slack_signed
        def events_api():
            # ...
        ```
    """
    from flask import request, Response

    @wraps(f)
    def decorated_function(*args, **kwargs):
        req_signature = request.headers.get("X-Slack-Signature")
        req_timestamp = request.headers.get("X-Slack-Request-Timestamp")

        print("CHECKING SLACK SIGNED")
        print("Signature", req_signature)
        print("Timestamp", req_timestamp)

        # Check if timestamp is more than 5 minutes old
        if abs(time() - int(req_timestamp)) > 60 * 5:
            print("EXPIRED TIMESTAMP")
            return Response("", status=403)

        body = request.get_data()
        if isinstance(body, str):
            body = str.encode(body)

        if verify_signature(req_timestamp, req_signature, body):
            print("VERIFIED")
            return f(*args, **kwargs)
        print("UNVERIFIED")
        return Response("", status=403)

    return decorated_function
