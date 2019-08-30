# The ENI used for VPC traffic mirroring.
resource "aws_network_interface" "rancor-eni-mirror-01" {
  description     = "ENI for VPC Traffic Mirror"
  subnet_id       = aws_subnet.us-east-1d-private-rancorMainVPC.id
  security_groups = [aws_security_group.rancor-main-default-sg.id]
  attachment {
    device_index = 1
    instance     = aws_instance.rancor-mirror-01.id
  }
  tags = {
    Name = "rancor-eni-mirror-01"
    Type = "ENI Mirror"
  }
}
# NOTE: This is just the mirror target, the AWS CLI would need to finish setting this up as a
# VPC Traffic Mirror (ref. https://docs.aws.amazon.com/AWSEC2/latest/APIReference/OperationList-query-vpc.html)