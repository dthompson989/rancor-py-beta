################# IAM POLICY DOCUMENTS #################
# This is the IAM Assume Role Policy Document
data "aws_iam_policy_document" "python-housekeeper-assume-role-policy-document" {
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
data "aws_iam_policy_document" "python-housekeeper-additional-policy-document" {
  policy_id = "__additional_python_housekeeper_policy_ID"
  statement {
    actions   = [
      "acm:DescribeCertificate",
      "acm:ListCertificates",
      "lambda:InvokeFunction"
    ]
    resources = ["*"]
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
resource "aws_iam_policy" "python-housekeeper-additional-policy" {
  name   = "python-housekeeper-additional-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.python-housekeeper-additional-policy-document.json
}

################# IAM ROLE #################
# NOTE: for assume_role_policy, aws_iam_policy cannot be used. Instead use aws_iam_policy_document directly
resource "aws_iam_role" "rancor-python-housekeeper-role" {
  name               = "rancor-python-housekeeper-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.python-housekeeper-assume-role-policy-document.json
  tags               = {
    Name = var.lambda_function
  }
}

################# IAM ROLE POLICY ATTACHMENTS  #################
# Attach the Additional IAM Policy
resource "aws_iam_role_policy_attachment" "rancor-python-housekeeper-additional-policy-attach" {
  role       = aws_iam_role.rancor-python-housekeeper-role.name
  policy_arn = aws_iam_policy.python-housekeeper-additional-policy.arn
}
