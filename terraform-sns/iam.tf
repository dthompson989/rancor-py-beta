# This is the IAM SNS Policy
data "aws_iam_policy_document" "rancor-sns-policy-document" {
  policy_id = "__default_policy_ID"
  statement {
    actions = [
      "sns:Subscribe",
      "sns:SetTopicAttributes",
      "sns:RemovePermission",
      "sns:Receive",
      "sns:Publish",
      "sns:ListSubscriptionsByTopic",
      "sns:GetTopicAttributes",
      "sns:DeleteTopic",
      "sns:AddPermission"
    ]
    principals {
      type = "AWS"
      identifiers = ["*"]
    }
    resources = [aws_sns_topic.rancor-sns.arn]
  }
}