![](https://www.politico.com/interactives/cdn/images/badge.svg)

# Setting up your AWS Lambda environment

Once you deploy your Lambda instance, make sure at minimum you set these variables in its environment.

##### `API_VERIFICATION_TOKEN`

Verification token from [eventsrouter app](https://github.com/The-Politico/django-slack-events-router).

##### `SLACK_API_TOKEN`

OAuth token for your Slack app. Your app will need these permissions at minimum:

- `chat:write:bot`
- `files:read`
- `files:write:user`
- `groups:history`
- `groups:write`
- `im:write`
- `mpim:write`
- `team:read`
- `users:read`
- `users:read.email`


##### `SLACK_CHANNEL`

Slack Channel ID, e.g., `G123456789`.

##### `SLACK_BOT_USER`

Slack User ID, e.g., `U123456789`.

##### `LAMBDA`

This variable should already be set for you as part of the deployment pipeline.
