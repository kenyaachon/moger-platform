terraform {
  backend "s3" {
    bucket  = "moger-terraform-state"
    key     = "terraform.tfstate"
    region  = "us-west-2"
    encrypt = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.1.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.5.1"
    }
  }

  required_version = ">= 1.2.0"
}