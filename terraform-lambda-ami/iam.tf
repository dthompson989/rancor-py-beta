################# IAM POLICY DOCUMENTS #################
# This is the IAM Assume Role Policy Document
data "aws_iam_policy_document" "python-ami-assume-role-policy-document" {
  policy_id = "__assume_lambda_role_policy_ID"
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# This is the IAM Additional Permissions Document
data "aws_iam_policy_document" "python-ami-additional-policy-document" {
  policy_id = "__additional_python_ami_policy_ID"
  statement {
    actions   = ["ec2:*"]
    resources = ["*"]
  }
  statement {
    actions   = ["sns:Publish"]
    resources = [var.sns_arn]
  }
  statement {
    actions   =["logs:CreateLogStream"]
    resources = [var.cw_log_stream_arn]
  }
  statement {
    actions   =["logs:PutLogEvents"]
    resources = [var.cw_put_log_arn]
  }
}

################# IAM POLICIES #################
# This is the Additional Permissions Policy
resource "aws_iam_policy" "python-ami-additional-policy" {
  name   = "python-ami-additional-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.python-ami-additional-policy-document.json
}

################# IAM ROLE #################
# NOTE: for assume_role_policy, aws_iam_policy cannot be used. Instead use aws_iam_policy_document directly
resource "aws_iam_role" "rancor-python-ami-role" {
  name               = "rancor-python-ami-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.python-ami-assume-role-policy-document.json
}

################# IAM ROLE POLICY ATTACHMENTS  #################
# Attach the Default SSM Policy
resource "aws_iam_role_policy_attachment" "jenkins-default-policy-attach" {
  role       = aws_iam_role.rancor-python-ami-role.name
  policy_arn = aws_iam_policy.python-ami-additional-policy.arn
}
