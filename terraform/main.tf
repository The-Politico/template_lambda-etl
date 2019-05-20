provider "aws" {
  region = "${var.aws_region}"
  profile = "interactives"
}



terraform {
  backend "s3" {
    bucket = "politico-terraform-configs"
    key = "configs/template-lambda-etl/terraform.tfstate"
    region = "us-east-1"
    profile = "interactives"
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
