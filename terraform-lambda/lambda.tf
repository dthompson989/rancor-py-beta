resource "aws_lambda_function" "rancor-terminate-interupt" {
  runtime          = var.lamdba_runtime
  handler          = var.lambda_handler
  function_name    = var.lambda_function
  filename         = var.lambda_filename
  source_code_hash = filebase64sha256(var.lambda_filename)
  role             = aws_iam_role.rancor-python-role.arn

  tags ={

  }
}