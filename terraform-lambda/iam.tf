resource "aws_iam_role" "rancor-python-role" {
  name = "rancor-python-role"
  # Assume the role policy
  assume_role_policy = {
    "Version": "2012-10-17"
    "Statement": [
      {
        Action: "sts:AssumeRole",
        Principal: {
          Service: "lambda.amazonaws.com"
        },
        Effect: "Allow",
        Sid: ""
      }
    ]
  }

}