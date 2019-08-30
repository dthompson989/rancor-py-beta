# The init.sh script to install jenkins
data "template_file" "jenkins-init" {
  template = file("init.sh")
}

# Create a cloud config file
data "template_cloudinit_config" "cloudinit-jenkins" {
  gzip          = false
  base64_encode = false
  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.jenkins-init.rendered
  }
}