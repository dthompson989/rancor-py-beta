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
# AMI's ::: Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type
variable "ami_id" {
  type    = "map"
  default = {
    us-east-1 = "ami-00eb20669e0990cb4"
    us-east-2 = "ami-0c64dd618a49aeee8"
    us-west-1 = "ami-0bce08e823ed38bdd"
    us-west-2 = "ami-08d489468314a58df"
  }
}