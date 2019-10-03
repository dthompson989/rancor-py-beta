terraform {
  backend "s3" {
    bucket  = "rancor-terraform-backend"
    encrypt = true
    key     = "terraform-sns/terraform.tfstate"
    region  = "us-east-2"
  }
}