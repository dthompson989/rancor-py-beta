# The ARN of the IAM Role
output "lambda-cross-account-role" {
  value = aws_iam_role.lambda-cross-account-role.arn
}