#!/bin/bash
sudo yum update -y

# install ssm agent
sudo yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm

# enable and start ssm service
sudo start amazon-ssm-agent

# download jenkins and jenkins key
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

# install dependencies
sudo yum install -y python3 openjdk-8-jre
update-java-alternatives --set java-1.8.0-openjdk-amd64

# install jenkins
sudo yum install -y jenkins

# start jenkins
sudo service jenkins start