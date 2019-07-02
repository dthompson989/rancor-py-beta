data "template_cloudinit_config" "ec2-instance-update" {
  package_upgrade: true

  part {
    content_type = "text/x-shellscript"
    content      = "#!/bin/bash\nyum update"
  }
}