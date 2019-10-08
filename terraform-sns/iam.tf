data "aws_iam_policy_document" "rancor-sns-policy-document" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogStream"]
    resources = ["arn:aws:logs:us-east-2:627948436154:log-group:/aws/sns/terraform-sns:*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["logs:PutLogEvents"]
    resources = ["arn:aws:logs:us-east-2:627948436154:log-group:/aws/sns/terraform-sns:*:*"]
  }
}

# Used in sns.tf
resource "aws_iam_policy" "rancor-sns-policy" {
  name        = "rancor-sns-policy"
  description = "The SNS IAM policy to allow CloudWatch logging"
  policy      = data.aws_iam_policy_document.rancor-sns-policy-document.json
}