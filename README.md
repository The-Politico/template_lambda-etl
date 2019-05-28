![](https://www.politico.com/interactives/cdn/images/badge.svg)

# template_lambda-etl


This is a [POLITICO interactive template](https://github.com/The-Politico/politico-interactive-templates) to create a Python-based, AWS Lambda & Slack-backed ETL pipeline.

### Why this?

At POLITICO, we build ETL scripts to process recurring data like polls and trackers. An automated pipeline helps cut our developers out of the loop when data sources are predictable, which saves us time and lets us include more people from our newsroom when building the databases that run our pages.

This template creates a fully-formed ETL pipeline. Your users can upload raw data sources in Slack, which will trigger your custom data cleaning and loading process in AWS Lambda.

Using serverless architecture means ETL processes can scale to whatever size you need at the absolute minimum cost. It also means you don't ever need to worry about server availability for occasional processing.

### What's in it?

The template includes an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template for creating an ETL pipeline hosted by AWS Lambda and triggered by file uploads in Slack. It also includes [Terraform](https://www.terraform.io/) scripts to build a deployment pipeline for continuous integration with a GitHub repository.

The template contains boilerplate for your ETL process and the Lambda server that calls it, with Python libraries like [numpy](https://www.numpy.org/) and [pandas](https://pandas.pydata.org/) included out-of-the-box.

### Assumptions

We assume you have access to create an app in your Slack workspace and that you will create a dedicated channel for each ETL pipeline you create. We assume file uploads into that channel will trigger your ETL process and that your ETL script will handle verifying the data uploaded by your users.

We also assume you're using [django-slack-events-router](https://github.com/The-Politico/django-slack-events-router) as a middleman between Slack and your ETL pipeline. It's especially useful if you're limited by free Slack or don't otherwise want to create a new Slack app for each pipeline. **However**, you can easily point your ETL process directly at Slack, skipping the middleman, by rewriting the authentication included with the Flask server Lambda runs. Read the docs included with the template.

## Quickstart

1. Install the template using [POLITICO interactive templates](https://github.com/The-Politico/politico-interactive-templates).

  ```
  $ pit register https://github.com/The-Politico/template_lambda-etl
  ```

2. Use PIT to create a new project from this template.

  ```
  $ mkdir new-project
  $ cd new-project
  $ pit new
  ```

3. Follow the guide in the created README to build out your project from the template.
