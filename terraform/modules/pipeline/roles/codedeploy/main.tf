data "aws_iam_policy_document" "role_document" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["codedeploy.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "role" {
  name = "${var.project_slug}__CodeDeploy_role"
  assume_role_policy = "${data.aws_iam_policy_document.role_document.json}"
}

data "aws_iam_policy" "CodeDeployLambda" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRoleForLambda"
}

resource "aws_iam_role_policy_attachment" "role_policy_attachment" {
  role = "${aws_iam_role.role.id}"
  policy_arn = "${data.aws_iam_policy.CodeDeployLambda.arn}"
}
