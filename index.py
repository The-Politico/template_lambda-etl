import awsgi
from server import app


def handler(event, context):
    print("EVENT", event.get("body", "NO BODY"))
    print("CONTEXT", context)
    return awsgi.response(app, event, context)
