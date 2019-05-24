from flask import Flask, request, Response
from flask_cors import CORS
from process import Process
from .auth import authed
from .slack import fetch_slack_file, notify_error, notify_success
from .utils import clear_tmp

app = Flask(__name__)
CORS(app)

app.secret_key = b"SECRET_KEY"


@app.route("/", methods=["POST"])
@authed
def index():
    slack_message = request.json

    # This will never run if using eventsrouter...
    if slack_message.get("type") == "url_verification":
        return Response(slack_message.get("challenge"), status=200)

    event = slack_message.get("event", {})
    event_type = event.get("type", None)

    if event_type != "file_shared":
        return Response("Unsupported event type", status=401)

    file_id = event.get("file_id", None)

    if not file_id:
        return Response("No file id", status=401)

    try:
        local_file = fetch_slack_file(file_id)
        dataset = Process(local_file)
        dataset.etl()
    except Exception as e:
        notify_error(e)
        return Response("Error", status=500)

    notify_success()
    clear_tmp()
    return Response("OK", status=200)
