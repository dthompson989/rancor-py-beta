# Provider
variable "profile" {}
variable "region" { default = "us-east-2" }
# Instances
variable "ec2_type" {}
# Networking
variable "public_cidr" {}
variable "rancor_jenkins_vpc_cidr" {}
variable "public_subnet_1_cidr" {}
variable "private_subnet_1_cidr" {}
# AMI's
variable "ami_id" {
  type    = "map"
  default = {
    us-east-1 = "ami-0c6b1d09930fac512"
    us-east-2 = "ami-02f706d959cedf892"
    us-west-1 = "ami-0fcdcdb074d2bac5f"
    us-west-2 = "ami-0f2176987ee50226e"
  }
}