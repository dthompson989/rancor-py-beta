# Provider
variable "profile" {}
variable "region" { default = "us-east-2" }
# IAM
variable jenkins_default_policy_arn {}
# SNS ARN
variable sns_arn {}
# CloudWatch
variable cw_log_stream_arn {}
variable cw_put_log_arn {}