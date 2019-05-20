data "aws_iam_policy_document" "role_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["cloudformation.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "role" {
  name = "${var.project_slug}__CloudFormation_role"
  assume_role_policy = "${data.aws_iam_policy_document.role_document.json}"
}

data "aws_iam_policy_document" "policy_document" {
  statement {
    actions = [
      "apigateway:*",
      "cloudformation:*",
      "codedeploy:*",
      "config:*",
      "dynamodb:*",
      "ec2:*",
      "events:*",
      "iam:*",
      "kinesis:*",
      "kms:*",
      "lambda:*",
      "s3:*",
      "sns:*",
      "ssm:*",
      "sqs:*"
    ]
    resources = ["*"]
  }
}


resource "aws_iam_role_policy" "role_policy" {
  name = "cloudformation_policy"
  role = "${aws_iam_role.role.id}"
  policy = "${data.aws_iam_policy_document.policy_document.json}"
}
