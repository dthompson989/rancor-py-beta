resource "aws_instance" "rancor-web01" {
  ami           = var.ami_id[var.region]
  instance_type = var.ec2_type
  subnet_id     = aws_subnet.us-east-1a-public-rancorMainVPC.id
  tags {
    Name = "rancor-web01"
    OS   = "Linux"
    Type = var.ec2_type
  }
}