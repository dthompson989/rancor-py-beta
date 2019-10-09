resource "aws_sns_topic" "rancor-sns" {
  name = "rancor-sns"
  tags = {
    Name = "rancor-sns"
    Type = "SNS"
  }
}

# IAM topic policy from iam.tf
resource "aws_sns_topic_policy" "rancor-sns-policy" {
  arn    = aws_sns_topic.rancor-sns.arn
  policy = data.aws_iam_policy_document.rancor-sns-policy-document.json
}

# This uses the serverless-post-to-slack lambda as its endpoint
resource "aws_sns_topic_subscription" "rancor-sns-lambda-subscription" {
  topic_arn = aws_sns_topic.rancor-sns.arn
  protocol  = "lambda"
  endpoint  = var.lambda_arn
}