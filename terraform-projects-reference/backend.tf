terraform {
  backend "s3" {
    bucket  = "rancor-terraform-backend"
    encrypt = true
    key     = "terraform-projects-reference/terraform.tfstate"
    region  = "us-east-2"
  }
}