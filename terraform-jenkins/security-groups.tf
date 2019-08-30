# Allow Http/s traffic
resource "aws_security_group" "rancor-jenkins-default-sg" {
  vpc_id      = aws_vpc.rancorJenkinsVPC.id
  name        = "rancor-jenkins-default-sg"
  description = "All HTTP and HTTPS Traffic"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.public_cidr]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "TCP"
    cidr_blocks = [var.public_cidr]
  }
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "TCP"
    cidr_blocks = [var.public_cidr]
  }
  tags = {
    Name = "rancor-jenkins-default-sg"
  }
}