# Scale up alarm
resource "aws_cloudwatch_metric_alarm" "ec2-scale-up-cpu-alarm" {
  alarm_name                = "ec2-scale-up-cpu-alarm"
  alarm_description         = "CPU utilization has risen above 80%"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  statistic                 = "Average"
  threshold                 = "80"
  alarm_actions             = [aws_autoscaling_policy.ec2-scale-up.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.rancor-ec2-asg-01.name
  }
  #insufficient_data_actions = []
}

# Scale down alarm
resource "aws_cloudwatch_metric_alarm" "ec2-scale-down-cpu-alarm" {
  alarm_name                = "ec2-scale-down-cpu-alarm"
  alarm_description         = "CPU utilization has fallen below 10%"
  comparison_operator       = "LessThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  statistic                 = "Average"
  threshold                 = "10"
  alarm_actions             = [aws_autoscaling_policy.ec2-scale-down.arn]
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.rancor-ec2-asg-01.name
  }
  #insufficient_data_actions = []
}