provider "aws" {
  profile    = var.profile
  region     = var.region
}

resource "aws_instance" "rancor-web01" {
  ami           = "ami-0c6b1d09930fac512"
  instance_type = "t2.micro"
}