resource "aws_iam_role" "rancor-python-ami-role" {
  name = "rancor-python-ami-role"
  # Assume the role policy
  assume_role_policy = file("rancor-python-policy.json")
}