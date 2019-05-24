provider "aws" {
  region = "${var.aws_region}"
  profile = "<%=aws_profile%>"
}



terraform {
  backend "s3" {
    bucket = "politico-terraform-configs"
    key = "configs/<%=project_slug%>/terraform.tfstate"
    region = "us-east-1"
    profile = "<%=aws_profile%>"
    encrypt = true
  }
}


module "pipeline" {
  source = "./modules/pipeline"
  aws_region = "${var.aws_region}"
  github_org = "${var.github_org}"
  github_repo = "${var.github_repo}"
  github_token = "${var.github_token}"
  project_slug = "${var.project_slug}"
}
