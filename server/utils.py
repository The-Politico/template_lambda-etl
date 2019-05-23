import os
import requests
from uuid import uuid4
import glob
from werkzeug.utils import secure_filename


class DataFileDownloadError(Exception):
    pass


TEMP_DIR = (
    "/tmp/downloads" if os.getenv("LAMBDA", False) else "./.tmp/downloads"
)


def ensure_tmp():
    os.makedirs(TEMP_DIR, exist_ok=True)


def clear_tmp():
    files = glob.glob("{}/*".format(TEMP_DIR))
    for file in files:
        os.remove(file)


def get_filepath(url_or_path):
    filename = os.path.basename(url_or_path)
    extension = os.path.splitext(filename)[1]
    clean_filename = secure_filename(
        "datafile_{}{}".format(uuid4().hex[:10], extension.lower())
    )
    return os.path.join(TEMP_DIR, clean_filename)


def download_file(url):
    ensure_tmp()
    filepath = get_filepath(url)
    headers = {
        "Authorization": "Bearer {}".format(os.getenv("SLACK_API_TOKEN"))
    }
    try:
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except Exception as e:
        raise DataFileDownloadError(str(e))
    return filepath
