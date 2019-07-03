# ASG launch config example
resource "aws_launch_configuration" "rancor-ec2-launchconfig" {
  name_prefix     = "rancor-asg-launchconfig-"
  image_id        = var.ami_id[var.region]
  instance_type   = var.ec2_type
  security_groups = [[aws_security_group.rancor-main-default-sg.id]]
}
resource "aws_autoscaling_group" "rancor-ec2-asg-01" {
  name                      = "rancor-ec2-asg-01"
  vpc_zone_identifier       = [aws_subnet.us-east-1a-public-01-rancorMainVPC.id, aws_subnet.us-east-1b-public-01-rancorMainVPC.id]
  launch_configuration      = aws_launch_configuration.rancor-ec2-launchconfig.name
  min_size                  = 1
  max_size                  = 2
  health_check_type         = "EC2"
  health_check_grace_period = 300
  force_delete              = true
  tag {
    key                 = "Name"
    value               = "rancor-ec2-asg-01"
    propagate_at_launch = true
  }
}
resource "aws_autoscaling_policy" "ec2-scale-up" {
  name                   = "ec2-scale-up"
  autoscaling_group_name = aws_autoscaling_group.rancor-ec2-asg-01.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = "1"
  cooldown               = "300"
  policy_type            = "SimpleScaling"
}
resource "aws_autoscaling_policy" "ec2-scale-down" {
  name                   = "ec2-scale-down"
  autoscaling_group_name = aws_autoscaling_group.rancor-ec2-asg-01.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = "-1"
  cooldown               = "300"
  policy_type            = "SimpleScaling"
}

# Add aws_cloudwatch_metric_alarm
# Optional: Add notification, maybe a slack notification