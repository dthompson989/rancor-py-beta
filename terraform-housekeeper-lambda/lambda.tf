resource "aws_lambda_function" "rancor-housekeeper" {
  runtime          = var.lamdba_runtime
  handler          = var.lambda_handler
  function_name    = var.lambda_function
  filename         = var.lambda_filename
  source_code_hash = filebase64sha256(var.lambda_filename)
  role             = aws_iam_role.rancor-python-housekeeper-role.arn
  timeout          = "60"
  memory_size      = "128"
  description      = "Used to handle basic housekeeping of AWS environment"
  tags             = {
    Name    = var.lambda_function
    OS      = "Lambda"
    Type    = var.lamdba_runtime
    Version = "1.0"
  }
}