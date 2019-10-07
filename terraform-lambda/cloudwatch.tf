# CloudWatch event to trigger auto_ami lambda weekly
resource "aws_cloudwatch_event_rule" "rancor-weekly-ami-event" {
  name                = "rancor-weekly-ami-event"
  description         = "Fires every Sunday at 10AM"
  schedule_expression = "cron(0 10 * * 0)"
  tags = {
    Name = "rancor-weekly-ami-event"
    Type = "CloudWatch Event"
  }
}

# CloudWatch event target, rancor-lambda handler.py
resource "aws_cloudwatch_event_target" "rancor-weekly-ami-target" {
  rule      = aws_cloudwatch_event_rule.rancor-weekly-ami-event.name
  target_id = "rancor-auto-ami"
  arn       = aws_lambda_function.rancor-auto-ami.arn
}

# Allow CloudWatch permission to call the Lambda
resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.rancor-auto-ami.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.rancor-weekly-ami-event.arn
}