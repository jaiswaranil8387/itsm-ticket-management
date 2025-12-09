provider "aws" {
  region = "ap-south-1"
}

terraform {
  backend "s3" {
    bucket = "terraform-for-kubernetes"   # Your created bucket
    key    = "state/terraform.tfstate"    # Path inside bucket
    region = "ap-south-1"
  }
}