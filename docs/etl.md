![](https://www.politico.com/interactives/cdn/images/badge.svg)

# Building your ETL pipeline

### The pipeline

The pipeline for your ETL process begins with a channel in Slack. When users upload a file of a specified type to that channel, Slack will trigger your ETL process in AWS Lambda, first downloading the file from Slack and then processing it using your custom code.

Between Slack and your Lambda instance is [django-slack-events-router](https://github.com/The-Politico/django-slack-events-router), which takes care of routing just [`file_shared`](https://api.slack.com/events/file_shared) events from Slack to your ETL process' API. (You can also cut out the middleman, see these [docs](eventsrouter.md).)

### The Process

Build your ETL process in the `process/` directory. That module should export a `Process` class that has at minimum an `etl` method. It also **must** export an `ALLOWED_FILE_TYPES` variable.

The server will create a new `Process` instance, passing to it the path to the file downloaded from Slack. Then it will call the `etl` method.

Use `pipenv` to install any dependencies your process needs. For example:

```
$ pipenv install requests
```

### Pro-tips

You can write whatever code you need to process your data, but remember, outside checking the filetype (dumbly, by file extension), it's up to your code to determine whether the data it receives from Slack is valid.

We recommend writing methods to check the validity of your data schema. Often, it's useful to have a good version of a XLSX file to compare to, for example. You can see an example of this in the boilerplate of this code.

If your code raises any errors while processing, the server will post your exception message in the Slack channel. So it's a great idea to write custom exceptions that will help your user troubleshoot or report back to you what's wrong with their data.


### Testing

We recommend testing your ETL process directly using both examples of good and bad data. See the `test/` directory for an example.

To test, run `pytest`:

```
$ pipenv run pytest
```
