import os


class MissingRequiredConfig(Exception):
    pass


class Settings:
    pass


Settings.LAMBDA = os.getenv("LAMBDA", False)

Settings.API_VERIFICATION_TOKEN = os.getenv("API_VERIFICATION_TOKEN", None)
if not Settings.API_VERIFICATION_TOKEN:
    raise MissingRequiredConfig(
        "No API_VERIFICATION_TOKEN environment variable set"
    )

Settings.SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN", None)
if not Settings.SLACK_API_TOKEN:
    raise MissingRequiredConfig("No SLACK_API_TOKEN environment variable set")

Settings.SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", None)
if not Settings.SLACK_CHANNEL:
    raise MissingRequiredConfig("No SLACK_CHANNEL environment variable set")

Settings.SLACK_BOT_USER = os.getenv("SLACK_BOT_USER", None)
if not Settings.SLACK_BOT_USER:
    raise MissingRequiredConfig("No SLACK_BOT_USER environment variable set")


settings = Settings
