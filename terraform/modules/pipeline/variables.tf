variable "aws_region" {
  type = "string"
  default = "us-east-1"
}

variable "github_org" {
  type = "string"
}

variable "github_repo" {
  type = "string"
}

variable "github_branch" {
  type = "string"
  default = "master"
}

variable "github_token" {
  type = "string"
}

variable "project_slug" {
  type = "string"
}
