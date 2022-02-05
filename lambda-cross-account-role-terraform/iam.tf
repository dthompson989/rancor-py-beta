################# IAM POLICY DOCUMENTS #################
# This is the IAM Assume Role Policy Document
data "aws_iam_policy_document" "lambda-cross-account-assume-role-policy-document" {
  policy_id = "__assume_role_policy_ID"
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = [var.cross_account_iam]
    }
  }
}

# This is the IAM Additional Permissions Document needed for the Lambda in the other account to access IAM Roles
data "aws_iam_policy_document" "lambda-cross-account-iam-policy-document" {
  policy_id = "__lambda_cross_account_iam_policy_ID"
  statement {
    actions = [
      "iam:ListRoles",
      "iam:ListAttachedRolePolicies",
      "iam:ListRolePolicies",
      "iam:ListPolicyVersions",
      "iam:GetPolicyVersion",
      "iam:GetRolePolicy"
    ]
    resources = ["*"]
  }
}

################# IAM POLICIES #################
# This is the Lambda Cross Account IAM Permissions Policy
resource "aws_iam_policy" "lambda-cross-account-iam-policy" {
  name   = "lambda-cross-account-iam-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.lambda-cross-account-iam-policy-document.json
}

################# IAM ROLE #################
# NOTE: for assume_role_policy, aws_iam_policy cannot be used. Instead use aws_iam_policy_document directly
resource "aws_iam_role" "lambda-cross-account-role" {
  name               = "lambda-cross-account-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-cross-account-assume-role-policy-document.json
  tags = {
    AssetID       = var.asset_id
    AssetAreaName = var.asset_area_name
    AssetName     = var.asset_name
    ControlledBy  = "terraform"
  }
}

################# IAM ROLE POLICY ATTACHMENT #################
# Attach the Lambda Cross Account IAM Permissions Policy
resource "aws_iam_role_policy_attachment" "lambda-cross-account-iam-policy-attach" {
  role       = aws_iam_role.lambda-cross-account-role.name
  policy_arn = aws_iam_policy.lambda-cross-account-iam-policy.arn
}