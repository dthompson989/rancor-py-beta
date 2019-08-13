resource "aws_iam_role" "rancor-python-role" {
  name = "rancor-python-role"
  # Assume the role policy
  assume_role_policy = file("rancor-python-policy.json")
}