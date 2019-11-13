################# IAM POLICY DOCUMENTS #################
# This is the IAM Assume Role Policy Document
data "aws_iam_policy_document" "jenkins-assume-role-policy-document" {
  policy_id = "__assume_role_policy_ID"
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type = "Service"
      identifiers = [
        "ec2.amazonaws.com"
      ]
    }
  }
}

# This is the IAM Additional Permissions Document
data "aws_iam_policy_document" "jenkins-additional-policy-document" {
  policy_id = "__default_jenkins_policy_ID"

}

################# IAM POLICIES #################
# This is the Assume Role Policy
resource "aws_iam_policy" "jenkins-assume-role-policy" {
  name   = "jenkins-assume-role-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.jenkins-assume-role-policy-document.json
}

# This is the Additional Permissions Policy
resource "aws_iam_policy" "jenkins-additional-policy" {
  name   = "jenkins-additional-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.jenkins-additional-policy-document.json
}

################# IAM ROLE #################
resource "aws_iam_role" "rancor-jenkins-role" {
  name               = "rancor-jenkins-role"
  assume_role_policy = aws_iam_policy.jenkins-assume-role-policy.name
}

################# IAM ROLE POLICY ATTACHMENTS  #################
# Attach the Default SSM Policy
resource "aws_iam_role_policy_attachment" "jenkins-default-policy-attach" {
  name       = "jenkins-default-policy-attach"
  role       = aws_iam_role.rancor-jenkins-role.name
  policy_arn = var.jenkins_default_policy_arn
}

# Attach the Additional Permissions Policy
resource "aws_iam_role_policy_attachment" "jenkins-additional-policy-attach" {
  name       = "jenkins-additional-policy-attach"
  role       = aws_iam_role.rancor-jenkins-role.name
  policy_arn = aws_iam_policy.jenkins-additional-policy.arn
}