provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"

  default_tags {
    tags = {
      Environment = "dev"
      Terraform   = true
    }
  }
}