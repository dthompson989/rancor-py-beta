resource "aws_instance" "rancor-web01" {
  ami                    = var.ami_id
  instance_type          = var.ec2_type
  vpc_security_group_ids = [var.vpc_sg]
  tags                   = {
    Name = "rancor-web01"
    OS   = "Linux"
    Type = var.ec2_type
  }
}