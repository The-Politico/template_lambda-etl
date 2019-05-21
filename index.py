import awsgi
from server import app


def handler(event, context):
    print("EVENT", event)
    print("CONTEXT", context)
    return awsgi.response(app, event, context)
