################# IAM POLICY DOCUMENTS #################
# This is the IAM Assume Role Policy Document
data "aws_iam_policy_document" "jenkins-assume-role-policy-document" {
  policy_id = "__assume_role_policy_ID"
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

# This is the IAM Additional Permissions Document
# NOTE: This can probably be rewritten using a for loop and a mapping of actions and resources
data "aws_iam_policy_document" "jenkins-additional-policy-document" {
  policy_id = "__default_jenkins_policy_ID"
  statement {
    actions   = ["sns:Publish"]
    resources = [var.sns_arn]
  }
  statement {
    actions   = ["logs:CreateLogStream"]
    resources = [var.cw_log_stream_arn]
  }
  statement {
    actions   = ["logs:PutLogEvents"]
    resources = [var.cw_put_log_arn]
  }
  statement {
    actions   = ["s3:*"]
    resources = [
      var.prod_website,
      var.dev_website
    ]
  }
  statement {
    actions   = [
      "s3:Get*",
      "s3:List*"
    ]
    resources = [var.tf_backend]
  }
}

################# IAM POLICIES #################
# This is the Additional Permissions Policy
resource "aws_iam_policy" "jenkins-additional-policy" {
  name   = "jenkins-additional-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.jenkins-additional-policy-document.json
}

################# IAM ROLE #################
# NOTE: for assume_role_policy, aws_iam_policy cannot be used. Instead use aws_iam_policy_document directly
resource "aws_iam_role" "rancor-jenkins-role" {
  name               = "rancor-jenkins-role"
  assume_role_policy = data.aws_iam_policy_document.jenkins-assume-role-policy-document.json
}

################# IAM ROLE POLICY ATTACHMENTS  #################
# Attach the Default SSM Policy
resource "aws_iam_role_policy_attachment" "jenkins-default-policy-attach" {
  role       = aws_iam_role.rancor-jenkins-role.name
  policy_arn = var.jenkins_default_policy_arn
}

# Attach the Additional Permissions Policy
resource "aws_iam_role_policy_attachment" "jenkins-additional-policy-attach" {
  role       = aws_iam_role.rancor-jenkins-role.name
  policy_arn = aws_iam_policy.jenkins-additional-policy.arn
}