# S3 BUCKET
# Make sure this bucket exists for your region
data "aws_s3_bucket" "codepipeline" {
  bucket = "politico-codepipeline-deployments-${var.aws_region}"
}

# ROLES
module "codepipeline_role" {
  source = "./roles/codepipeline"
  project_slug = "${var.project_slug}"
  s3_bucket_arn = "${data.aws_s3_bucket.codepipeline.arn}"
}

module "cloudformation_role" {
  source = "./roles/cloudformation"
  project_slug = "${var.project_slug}"
}

module "codedeploy_role" {
  source = "./roles/codedeploy"
  project_slug = "${var.project_slug}"
}


# CODEBUILD PROJECT
resource "aws_codebuild_project" "project" {
  name = "${var.project_slug}"
  description = "${var.project_slug} CodeBuild Project"
  build_timeout = "10"
  service_role = "${module.codepipeline_role.id}"

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "aws/codebuild/standard:1.0"
    type = "LINUX_CONTAINER"

    environment_variable {
      "name" = "S3_BUCKET"
      "value" = "${data.aws_s3_bucket.codepipeline.id}"
    }

    environment_variable {
      "name" = "PROJECT_SLUG"
      "value" = "${var.project_slug}"
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "aws.build.yml"
  }

  artifacts {
    type = "CODEPIPELINE"
  }
}

# CODEPIPELINE
resource "aws_codepipeline" "codepipeline" {
  name = "${var.github_repo}__pipeline"
  role_arn = "${module.codepipeline_role.arn}"

  artifact_store {
    location = "${data.aws_s3_bucket.codepipeline.id}"
    type = "S3"
  }

  stage {
    name = "Source"

    action {
      name = "Source"
      category = "Source"
      owner = "ThirdParty"
      provider = "GitHub"
      version = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner = "${var.github_org}"
        Repo = "${var.github_repo}"
        Branch = "${var.github_branch}"
        OAuthToken = "${var.github_token}"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name = "Build"
      category = "Build"
      owner = "AWS"
      provider = "CodeBuild"
      input_artifacts = ["source_output"]
      output_artifacts = ["build_output"]
      version = "1"

      configuration = {
        ProjectName = "${var.project_slug}"
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name = "GenerateChangeSet"
      provider = "CloudFormation"
      category = "Deploy"
      owner = "AWS"
      run_order = 1

      input_artifacts = ["build_output"]
      version = "1"

      configuration {
        ActionMode = "CHANGE_SET_REPLACE"
        Capabilities = "CAPABILITY_NAMED_IAM"
        StackName = "${var.project_slug}"
        TemplatePath = "build_output::template-export.yml"
        RoleArn = "${module.cloudformation_role.arn}"
        ChangeSetName = "pipeline-changeset"
        ParameterOverrides = "${jsonencode(map(
          "ProjectId", aws_codebuild_project.project.name,
          "CodeDeployRole", module.codedeploy_role.arn
        ))}"
      }
    }

    action {
      name = "ExecuteChangeSet"
      provider = "CloudFormation"
      category = "Deploy"
      owner = "AWS"
      run_order = 2
      version = "1"

      configuration {
        ActionMode = "CHANGE_SET_EXECUTE"
        ChangeSetName = "pipeline-changeset"
        StackName = "${var.project_slug}"
        RoleArn = "${module.cloudformation_role.arn}"
      }
    }
  }
}
