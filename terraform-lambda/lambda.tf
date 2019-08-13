resource "aws_lambda_function" "rancor-terminate-interrupt" {
  runtime          = var.lamdba_runtime
  handler          = var.lambda_handler
  function_name    = var.lambda_function
  filename         = var.lambda_filename
  source_code_hash = filebase64sha256(var.lambda_filename)
  role             = aws_iam_role.rancor-python-role.arn

  tags ={

  }
}
# A CloudWatch Event invokes this Lambda when a lifecycle action occurs.
# Use the aws_autoscaling_lifecycle_hook resource