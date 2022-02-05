# CloudWatch event to trigger auto_ami lambda weekly
resource "aws_cloudwatch_event_rule" "rancor-weekly-housekeeping-event" {
  name                = "rancor-weekly-housekeeping-event"
  description         = "Fires every Friday at 9AM"
  schedule_expression = "cron(0 9 * * 5)"
  tags = {
    Name = var.lambda_function
    Type = "CloudWatch CRON Event"
  }
}

# CloudWatch event target, rancor-lambda handler.py
resource "aws_cloudwatch_event_target" "rancor-weekly-housekeeping-target" {
  rule      = aws_cloudwatch_event_rule.rancor-weekly-housekeeping-event.name
  target_id = "rancor-housekeeper"
  arn       = aws_lambda_function.rancor-housekeeper.arn
}

# Allow CloudWatch permission to call the Lambda
resource "aws_lambda_permission" "allow-cloudwatch-to-call-lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rancor-housekeeper.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.rancor-weekly-housekeeping-event.arn
}

# Cloudwatch Log Group for  Lambda to log to
resource "aws_cloudwatch_log_group" "rancor-weekly-housekeeping-log-group" {
  name              = "/aws/lambda/${aws_lambda_function.rancor-housekeeper.function_name}"
  retention_in_days = 30
  tags              = {
    Name = var.lambda_function
    Type = "CloudWatch Log Group"
  }
}