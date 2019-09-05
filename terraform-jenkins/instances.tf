# The Jenkins EC2 instance
resource "aws_instance" "rancor-jenkins" {
  ami                    = var.ami_id[var.region]
  instance_type          = var.ec2_type
  subnet_id              = aws_subnet.us-east-2a-public-rancorJenkinsVPC.id
  vpc_security_group_ids = [aws_security_group.rancor-jenkins-default-sg.id]
  user_data              = data.template_cloudinit_config.cloudinit-jenkins.rendered
  tags = {
    Name = "rancor-jenkins"
    OS   = "Linux"
    Type = var.ec2_type
  }
}

# The Jenkins EBS Volume ::: THIS SHOULD ONLY BE UNCOMMENTED IF THIS IS A NEW TERRAFORM PROJECT
/*
resource "aws_ebs_volume" "rancor-jenkins-data" {
  availability_zone = "us-east-2a"
  size              = 12
  type              = "gp2"
  tags = {
    Name     = "rancor-jenkins-data"
    Size     = "12Gb"
    Type     = "GP2"
    Attached = "rancor-jenkins"
  }
}

# Attach rancor-jenkins-data to rancor-jenkins
resource "aws_volume_attachment" "rancor-jenkins-attachment" {
  device_name  = "rancor-jenkins-data-ebs"
  volume_id    = aws_ebs_volume.rancor-jenkins-data.id
  instance_id  = aws_instance.rancor-jenkins.id
  skip_destroy = true
}
*/