data "template_cloudinit_config" "ec2-instance-update" {
  part {
    content_type = "text/x-shellscript"
    content      = "#!/bin/bash\nyum update"
  }
}