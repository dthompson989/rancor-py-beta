resource "aws_sns_topic" "rancor-sns" {
  name = "rancor-sns"
}

resource "aws_sns_topic_policy" "rancor-sns-policy" {
  arn    = aws_sns_topic.rancor-sns.arn
  policy = file("rancor-sns-policy.json")
}

resource "aws_sns_topic_subscription" "rancor-sns-lambda-subscription" {
  topic_arn = aws_sns_topic.rancor-sns.arn
  protocol  = "lambda"
  endpoint  = var.lambda_arn
}