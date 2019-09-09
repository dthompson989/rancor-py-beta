# The public DNS of rancor-jenkins EC2 instance
output "rancor-jenkins-dns" {
  value = aws_instance.rancor-jenkins.public_dns
}