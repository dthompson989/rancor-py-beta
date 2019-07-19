variable "profile" {}
variable "ec2_type" {}
variable "public_cidr" {}
variable "asg_min_size" {
  default = 1
}
variable "asg_max_size" {
  default = 2
}
variable "asg_health_check_type" {
  default = "ELB"
}
variable "region" {
  default = "us-east-1"
}
variable "ami_id" {
  type    = "map"
  default = {
    us-east-1 = "ami-0c6b1d09930fac512"
    us-east-2 = "ami-02f706d959cedf892"
    us-west-1 = "ami-0fcdcdb074d2bac5f"
    us-west-2 = "ami-0f2176987ee50226e"
  }
}
