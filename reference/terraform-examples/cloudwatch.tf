# CloudWatch CRON event to trigger the security audit SSM Automation Document
resource "aws_cloudwatch_event_rule" "ssm-security-auditor-cloudwatch-rule" {
  name                = "ssm-security-auditor-cloudwatch-rule"
  description         = "Fires every day at 10AM GTM (5AM EST)"
  schedule_expression = "cron(0 10 * * ? *)"
  tags = {
    AssetID       = var.asset_id
    AssetName     = var.asset_name
    AssetAreaName = var.asset_area_name
    ControlledBy  = "terraform"
  }
}

# CloudWatch event target, ec2-security-audit automation document
resource "aws_cloudwatch_event_target" "ssm-security-auditor-cloudwatch-target" {
  rule      = aws_cloudwatch_event_rule.ssm-security-auditor-cloudwatch-rule.name
  target_id = "ec2-security-audit-automation"
  # We need to use replace() because CloudWatch will think this is a regular SSM document, not an automation.
  arn       = replace(aws_ssm_document.ec2-security-audit.arn, "document/", "automation-definition/")
  role_arn  = aws_iam_role.ec2-security-audit-master-role.arn
}

########################## ALARMS ##########################
# CloudWatch Alarm for SSM Event failure
resource "aws_cloudwatch_event_rule" "ssm-security-auditor-failed-rule" {
  name          = "ssm-security-auditor-failed-rule"
  description   = "Alarm when (ANY) SSM Automations fail"
  event_pattern = <<PATTERN
  {
    "source": [
      "aws.ssm"
    ],
    "detail-type": [
      "EC2 Automation Step Status-change Notification",
      "EC2 Automation Execution Status-change Notification"
    ],
    "detail": {
      "Status": [
        "Failed",
        "TimedOut"
      ]
    }
  }
  PATTERN
  tags = {
    AssetID       = var.asset_id
    AssetName     = var.asset_name
    AssetAreaName = var.asset_area_name
    ControlledBy  = "terraform"
  }
}

# CloudWatch SNS Topic Target for SSM Event failure
resource "aws_cloudwatch_event_target" "ssm-security-auditor-failed-target" {
  rule      = aws_cloudwatch_event_rule.ssm-security-auditor-failed-rule.name
  target_id = "ssm-security-auditor-failed-sns-topic"
  arn       = var.sns_topic
}