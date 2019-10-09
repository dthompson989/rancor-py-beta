# This is the IAM SNS Policy
data "aws_iam_policy_document" "rancor-sns-policy-document" {
  policy_id = "__default_policy_ID"
  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission"
    ]
    principals {
      type = "AWS"
      identifiers = ["*"]
    }
    resources = [aws_sns_topic.rancor-sns.arn]
  }
}