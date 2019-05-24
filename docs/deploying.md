![](https://www.politico.com/interactives/cdn/images/badge.svg)

# Deploying infrastructure

This project comes with Terraform scripts to build an AWS CodePipeline connecting your GitHub repository to your AWS infrastructure. That means once you setup the pipeline you can simply push code to the master branch of your repository and see it deployed automatically.

Outside the pipeline all infrastructure is created using AWS CloudFormation. That way you can change the configuration of your Lambda function or API Gateway by simply committing your changes as code in `aws.build.yml`.

Here's how to build your pipeline and infrastructure:

### Pre-requisites

You should already have committed your code to a GitHub repository.

You should have your AWS credentials in a user profile at `~/.aws/credentials`. Be sure you're using the profile you specified when creating this project. (You can update your profile in `terraform/config/config.tfvars`.)

The pipeline will also need access to a GitHub personal access token that has access to your repository. You can add it to `terraform/config/config.tfvars.secret`. Alternatively, clear out the `github_token` key in that file and export a `TF_VAR_github_token` environment variable.

Make any necessary adjustments to the CloudFormation configuration in `aws.build.yml`. For example, you could change the timeout on your Lambda function by setting `Timeout: 4`.

### Building your pipeline

Once you're ready to build your pipeline, use the make commands to initialize and trigger Terraform's build step.

```
$ make init
$ make build
```

### Tearing down

```
$ make destroy
```
