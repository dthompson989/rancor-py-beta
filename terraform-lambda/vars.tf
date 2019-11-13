# Provider
variable "profile" {}
variable "region" { default = "us-east-2" }
# Lambda Config and Settings
variable "lamdba_runtime" {}
variable "lambda_handler" {}
variable "lambda_filename" {}
variable "lambda_function" {}
# SNS ARN
variable "sns_arn" {}
# CloudWatch ARN's
variable cw_log_stream_arn {}
variable cw_put_log_arn {}