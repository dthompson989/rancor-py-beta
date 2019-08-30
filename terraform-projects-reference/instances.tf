# The generic web server EC2 instance
resource "aws_instance" "rancor-web01" {
  ami                    = var.ami_id[var.region]
  instance_type          = var.ec2_type
  subnet_id              = aws_subnet.us-east-1a-public-rancorMainVPC.id
  vpc_security_group_ids = [aws_security_group.rancor-main-default-sg.id]
  tags = {
    Name = "rancor-web01"
    OS   = "Linux"
    Type = var.ec2_type
  }
  # Add the root_block_device to make the root volume bigger.
  # You can also add additional storage volumes, using the mkfs.ext4 command to format (script).
  # and then mkdir to make a new directory for the volume.
  # and finally mount it to the file system.
}

# The EC2 instance used for VPC traffic mirroring.
resource "aws_instance" "rancor-mirror-01" {
  # This AMI should be baked with network packet analysis tools on it.
  ami                    = var.ami_id[var.region]
  # The t2.micro instance type will not actually work. This is a prototype. Use a t3.micro instead.
  instance_type          = var.ec2_mirror_type
  subnet_id              = aws_subnet.us-east-1d-private-rancorMainVPC.id
  vpc_security_group_ids = [aws_security_group.rancor-main-default-sg.id]
  tags = {
    Name = "rancor-mirror-01"
    OS   = "Linux"
    Type = var.ec2_type
  }
}