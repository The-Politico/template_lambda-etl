import slack
import time
import os

from process import ALLOWED_FILE_TYPES
from .utils import download_file
from .conf import settings


class DataFileNotFound(Exception):
    pass


class UnsupportedFileType(Exception):
    pass


def ensure_bot_access(func):
    """Ensures our bot has access to channel."""

    def wrapper(*args, **kwargs):
        client = slack.WebClient(token=settings.SLACK_API_TOKEN)
        client.groups_invite(
            channel=settings.SLACK_CHANNEL, user=settings.SLACK_BOT_USER
        )
        return func(*args, **kwargs)

    return wrapper


@ensure_bot_access
def fetch_slack_file(file_id):
    """Requests Slack make a file upload publically available, downloads """
    client = slack.WebClient(token=settings.SLACK_API_TOKEN)
    try:
        client.files_sharedPublicURL(id="", file=file_id)
    except Exception:
        pass
    response = client.files_info(id="", file=file_id)
    if not response["ok"]:
        raise DataFileNotFound("Slack API errored")
    url = response.get("file", {}).get("url_download", None)
    if not url:
        url = response.get("file", {}).get("url_private_download", None)
    if not url:
        raise DataFileNotFound("No download URL for file")

    # unescape URL
    url = url.replace("\\/", "/")

    # A quick check based only on the extension
    try:
        extension = os.path.splitext(os.path.basename(url))[1][1:].upper()
    except Exception:
        raise UnsupportedFileType("File must have a valid extension")
    if extension not in ALLOWED_FILE_TYPES:
        raise UnsupportedFileType(
            'File of type "{}" is not supported'.format(extension)
        )

    local_file = download_file(url)
    return local_file


def notify_error(exception):
    """Send an error message to a Slack channel."""
    error_name = exception.__class__.__name__
    client = slack.WebClient(token=settings.SLACK_API_TOKEN)
    client.chat_postMessage(
        channel=settings.SLACK_CHANNEL,
        username="ETL bot",
        attachments=[
            {
                "fallback": "Processing error: {}".format(error_name),
                "color": "#AC0825",
                "pretext": (
                    "<!here|here> :rotating_light: "
                    "PROCESSING ERROR :rotating_light:"
                ),
                "author_name": "Error message:",
                "title": error_name,
                "text": str(exception),
                "image_url": "http://my-website.com/path/to/image.jpg",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "ETL Bot",
                "footer_icon": (
                    "https://pbs.twimg.com/profile_images/998954486205898753/"
                    "gbb2psb__400x400.jpg"
                ),
                "ts": int(time.time()),
            }
        ],
    )


def notify_success():
    """Send an error message to a Slack channel."""
    client = slack.WebClient(token=settings.SLACK_API_TOKEN)
    client.chat_postMessage(
        channel=settings.SLACK_CHANNEL,
        username="ETL bot",
        text="<!here|here> :thumbsup: Processed data OK",
    )
