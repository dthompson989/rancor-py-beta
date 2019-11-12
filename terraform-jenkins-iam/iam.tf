# This is the IAM SNS Policy
data "aws_iam_policy_document" "rancor-jenkins-policy-document" {
  policy_id = "__default_jenkins_policy_ID"

}

resource "aws_iam_policy" "jenkins-additional-policy" {
  name   = "jenkins-additional-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.rancor-jenkins-policy-document.json
}

data "aws_iam_policy" "jenkins-default-policy" {
  name = "jenkins-default-policy"
  arn  = var.jenkins_default_policy_arn
}

data "aws_iam_role" "rancor-jenkins-iam-role" {
  name = "rancor-jenkins-iam-role"
}

resource "aws_iam_role_policy_attachment" "jenkins-default-policy-attach" {
  name = "jenkins-default-policy-attach"
  role = ""
  policy_arn = ""
}

data "aws_iam_instance_profile" "rancor-jenkins-profile" {
  name      = "rancor-jenkins-profile"
  role_name = data.aws_iam_role.rancor-jenkins-iam-role.name
}