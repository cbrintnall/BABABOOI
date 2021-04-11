#Primary declaration of terraform properties

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws"{
    region = "us-west-2"
}