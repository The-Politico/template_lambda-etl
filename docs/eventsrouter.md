![](https://www.politico.com/interactives/cdn/images/badge.svg)

# Configuring the eventsrouter

1. Go to the Django admin for your [eventsrouter](https://github.com/The-Politico/django-slack-events-router).
2. Create a new Channel object using your Slack channel ID.
3. Create a new Route object using the URL for your Lambda instance's API gateway and filter by your channel and the `file_shared` event type.

### Want to connect to Slack directly?

If you're coming to this template and are not really interested in using [django-slack-events-router](https://github.com/The-Politico/django-slack-events-router), you'll simply need to rewrite the `authed` decorator in `server/auth.py`.

If you'd like to connect directly to your Slack app, you can use some of the methods in our [`politico-toolbox`](https://github.com/The-Politico/politico-toolbox) to shortcut Slack's [signed secret verification](https://api.slack.com/docs/verifying-requests-from-slack) steps.
