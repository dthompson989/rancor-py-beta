resource "aws_elb" "rancor-elb-01" {
  name            = "rancor-elb-01"
  subnets         = [aws_subnet.us-east-1a-public-rancorMainVPC.id, aws_subnet.us-east-1b-public-rancorMainVPC.id]
  security_groups = [aws_security_group.rancor-main-default-sg.id]
  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }
  health_check {
    healthy_threshold   = 2
    interval            = 30
    target              = "HTTP:80/"
    timeout             = 3
    unhealthy_threshold = 2
  }
  cross_zone_load_balancing   = true
  connection_draining         = true
  connection_draining_timeout = 300
  tags = {
    Name = "rancor-elb-01"
    Type = "ELB"
  }
}

# ELB should be in public sg/subnet, ec2 instances can be private