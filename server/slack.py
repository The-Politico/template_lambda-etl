import slack
import time
import os
from .utils import download_file


ALLOWED_FILE_TYPES = ["XLS", "XLSX", "CSV"]


class MissingSlackConfig(Exception):
    pass


class DataFileNotFound(Exception):
    pass


class UnsupportedFileType(Exception):
    pass


def check_env(func):
    """Checks if user has required env variables set.
    """

    def wrapper(*args, **kwargs):
        if not os.getenv("SLACK_API_TOKEN", False):
            raise MissingSlackConfig(
                "No SLACK_API_TOKEN environment variable set"
            )
        if not os.getenv("SLACK_CHANNEL", False):
            raise MissingSlackConfig(
                "No SLACK_CHANNEL environment variable set"
            )
        return func(*args, **kwargs)

    return wrapper


def ensure_bot_access(func):
    """Ensures our bot has access to channel."""

    def wrapper(*args, **kwargs):
        bot_user = os.getenv("SLACK_BOT_USER", False)
        if not bot_user:
            raise MissingSlackConfig(
                "No SLACK_BOT_USER environment variable set"
            )
        client = slack.WebClient(token=os.getenv("SLACK_API_TOKEN"))
        client.groups_invite(
            channel=os.getenv("SLACK_CHANNEL"),
            user=os.getenv("SLACK_BOT_USER"),
        )
        return func(*args, **kwargs)

    return wrapper


@ensure_bot_access
@check_env
def fetch_slack_file(file_id):
    print("FETCHING FILE: ", file_id)
    """Requests Slack make a file upload publically available, downloads """
    client = slack.WebClient(token=os.getenv("SLACK_API_TOKEN"))
    client.files_sharedPublicURL(id=file_id)
    response = client.files_info(id=file_id)
    if not response["ok"]:
        raise DataFileNotFound("Slack API errored")
    url = response.get("file", {}).get("url_download", None)
    if not url:
        url = response.get("file", {}).get("url_private_download", None)
    if not url:
        raise DataFileNotFound("No download URL for file")

    # A quick check based only on the extension
    try:
        extension = os.path.splitext(os.bath.basename(url))[1][1:].upper()
    except Exception:
        raise UnsupportedFileType("File must have a valid extension")
    if extension not in ALLOWED_FILE_TYPES:
        raise UnsupportedFileType(
            'File of type "{}" is not supported'.format(extension)
        )

    local_file = download_file(url)
    print("DOWNLOADED FILE")
    return local_file


@check_env
def notify_error(exception):
    """Send an error message to a Slack channel."""
    error_name = exception.__class__.__name__
    client = slack.WebClient(token=os.getenv("SLACK_API_TOKEN"))
    client.chat_postMessage(
        channel=os.getenv("SLACK_CHANNEL"),
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


@check_env
def notify_success():
    """Send an error message to a Slack channel."""
    client = slack.WebClient(token=os.getenv("SLACK_API_TOKEN"))
    client.chat_postMessage(
        channel=os.getenv("SLACK_CHANNEL"),
        username="ETL bot",
        text="<!here|here> :thumbsup: Processed data OK",
    )
