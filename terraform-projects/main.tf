provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

resource "aws_instance" "main" {
  ami           = "ami-0c6b1d09930fac512"
  instance_type = "t2.micro"

  vpc_security_group_ids = ["sg-05ab90c413f24716d"]
}