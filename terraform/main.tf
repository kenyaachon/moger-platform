terraform {
  backend "s3" {
    bucket = "moger-terraform-state"
    key = "terraform.tfstate"
    region = "us-west-2"
    encrypt = true
  }

  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
    region = "us-west-2"
}