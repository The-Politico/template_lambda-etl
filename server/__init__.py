import os
from uuid import uuid4

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from process import Process
from .auth import token_authed

import glob

ALLOWED_EXTENSIONS = ["xlsx"]

app = Flask(__name__)
CORS(app)

app.secret_key = b"SECRET_KEY"

app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB limit
app.config["UPLOAD_FOLDER"] = (
    "/tmp/uploads" if os.getenv("LAMBDA", False) else "./.tmp/uploads"
)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def ensure_tmp():
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def get_filename():
    return secure_filename("data_{}.xlsx".format(uuid4().hex))


def clear_uploads():
    files = glob.glob("{}/*".format(app.config["UPLOAD_FOLDER"]))
    for file in files:
        os.remove(file)


@app.route("/", methods=["GET", "POST"])
@token_authed
def index():
    # # Server check
    if request.method == "GET":
        response = jsonify({"message": "API OK"})
        response.status_code = 200
        return response

    # check if the post request has the file part
    if "file" not in request.files:
        print("files", request.files.to_dict())
        print("method", request.method)
        print("form", request.form.to_dict())
        print("data", request.data.to_dict())
        response = jsonify({"message": "No file submitted"})
        response.status_code = 500
        return response

    file = request.files["file"]

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        response = jsonify({"message": "File submitted has no filename"})
        response.status_code = 500
        return response

    ensure_tmp()
    if file and allowed_file(file.filename):
        filename = get_filename()
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        try:
            dataset = Process(file_path)
            dataset.etl()
        except Exception as e:
            response = jsonify(
                {
                    "message": "Error while processing data",
                    "error": "{} Error: {}".format(e.__class__.__name__, e),
                }
            )
            response.status_code = 500
            return response
        clear_uploads()
        response = jsonify({"message": "OK"})
        response.status_code = 200
        return response
