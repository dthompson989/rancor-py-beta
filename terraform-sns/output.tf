# The ARN of the SNS topic
output "rancor-sns-arn" {
  value = aws_sns_topic.rancor-sns.arn
}