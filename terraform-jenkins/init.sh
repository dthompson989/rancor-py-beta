#!/bin/bash
# remove java 7 and install java 8
sudo yum remove java-1.7.0-openjdk -y
sudo yum install java-1.8.0 -y

# update everything, if needed
sudo yum update -y

# install ssm agent
sudo yum install https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm -y

# enable and start ssm service
sudo start amazon-ssm-agent

# download jenkins and jenkins key
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
sudo rpm --import http://pkg.jenkins.io/redhat-stable/jenkins.io.key

# install jenkins
sudo yum install jenkins -y

# start jenkins
sudo service jenkins start
