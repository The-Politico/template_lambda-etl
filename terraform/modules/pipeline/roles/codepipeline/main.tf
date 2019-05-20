data "aws_iam_policy_document" "role_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = [
        "codepipeline.amazonaws.com",
        "s3.amazonaws.com",
        "codebuild.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "role" {
  name = "${var.project_slug}__CodePipeline_role"
  assume_role_policy = "${data.aws_iam_policy_document.role_document.json}"
}

data "aws_iam_policy_document" "policy_document" {
  statement {
    actions = ["s3:*"]
    resources = [
      "${var.s3_bucket_arn}",
      "${var.s3_bucket_arn}/*"
    ]
  }

  statement {
    actions = [
      "codecommit:GitPull",
      "codebuild:*",
      "logs:*",
      "cloudformation:*",
      "iam:PassRole",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "role_policy" {
  name = "codepipeline_policy"
  role = "${aws_iam_role.role.id}"
  policy = "${data.aws_iam_policy_document.policy_document.json}"
}
