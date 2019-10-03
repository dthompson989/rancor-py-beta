# Provider
variable "profile" {}
variable "region" { default = "us-east-2" }
# Lambda Config and Settings
variable "lamdba_runtime" {}
variable "lambda_handler" {}
variable "lambda_filename" {}
variable "lambda_function" {}