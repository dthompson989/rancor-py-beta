terraform {
  backend "s3" {
    bucket  = "rancor-terraform-backend"
    encrypt = true
    key     = "terraform-jenkins/terraform.tfstate"
    region  = "us-east-2"
  }
}