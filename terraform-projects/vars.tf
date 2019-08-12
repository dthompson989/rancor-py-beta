# Provider
variable "profile" {}
variable "region" { default = "us-east-1" }
# Instances
variable "ec2_type" {}
variable "ec2_mirror_type" {}
# Auto Scaling
variable "asg_min_size" { default = 1 }
variable "asg_max_size" { default = 2 }
variable "asg_health_check_type" { default = "ELB" }
# S3
variable "s3_bucket_arn" {}
# Networking
variable "public_cidr" {}
variable "rancormainvpc_cidr" {}
variable "public_subnet_1_cidr" {}
variable "public_subnet_2_cidr" {}
variable "private_subnet_1_cidr" {}
variable "private_subnet_2_cidr" {}
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