resource "aws_instance" "rancor-web01" {
  ami                    = var.ami_id[var.region]
  instance_type          = var.ec2_type
  subnet_id              = aws_subnet.us-east-1a-public-01-rancorMainVPC.id
  vpc_security_group_ids = [aws_security_group.rancor-main-default-sg.id]
  tags = {
    Name = "rancor-web01"
    OS   = "Linux"
    Type = var.ec2_type
  }
  # Add the root_block_device to make the root volume bigger
  # You can also add additional storage volumes, using the mkfs.ext4 command to format (script)
  # and then mkdir to make a new directory for the volume
  # and finally mount it to the file system.
}