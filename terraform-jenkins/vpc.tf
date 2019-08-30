# Jenkins VPC
resource "aws_vpc" "rancorJenkinsVPC" {
  cidr_block           = var.rancor_jenkins_vpc_cidr
  instance_tenancy     = "default"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  enable_classiclink   = "false"
  tags = {
    Name = "rancorJenkinsVPC"
    CIDR = var.rancor_jenkins_vpc_cidr
  }
}

# rancorJenkinsVPC Public Subnet 1
resource "aws_subnet" "us-east-2a-public-rancorJenkinsVPC" {
  vpc_id                  = aws_vpc.rancorJenkinsVPC.id
  cidr_block              = var.public_subnet_1_cidr
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-2a"
  tags = {
    Name = "us-east-2a-public-rancorJenkinsVPC"
    CIDR = var.public_subnet_1_cidr
  }
}

# rancorJenkinsVPC Private Subnet 1
resource "aws_subnet" "us-east-2c-private-rancorJenkinsVPC" {
  vpc_id                  = aws_vpc.rancorJenkinsVPC.id
  cidr_block              = var.private_subnet_1_cidr
  map_public_ip_on_launch = "false"
  availability_zone       = "us-east-2c"
  tags = {
    Name = "us-east-2c-private-rancorJenkinsVPC"
    CIDR = var.private_subnet_1_cidr
  }
}

# rancorJenkinsIGW Internet Gateway
resource "aws_internet_gateway" "rancorJenkinsIGW" {
  vpc_id = aws_vpc.rancorJenkinsVPC.id
  tags = {
    Name = "rancorJenkinsIGW"
  }
}

# rancorJenkinsVPC Public Route Table
resource "aws_route_table" "rancorJenkinsPublicRouteTable" {
  vpc_id = aws_vpc.rancorJenkinsVPC.id
  route {
    cidr_block = var.public_cidr
    gateway_id = aws_internet_gateway.rancorJenkinsIGW.id
  }
  tags = {
    Name = "rancorJenkinsPublicRouteTable"
  }
}

# rancorJenkinsVPC Private Route Table
resource "aws_route_table" "rancorJenkinsPrivateRouteTable" {
  vpc_id = aws_vpc.rancorJenkinsVPC.id
  tags = {
    Name = "rancorJenkinsPrivateRouteTable"
  }
}

# rancorJenkinsVPC Public AZ2a Route Association
resource "aws_route_table_association" "rancorJenkinsPublic01RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-2a-public-rancorJenkinsVPC.id
  route_table_id = aws_route_table.rancorJenkinsPublicRouteTable.id
}

# rancorJenkinsVPC Private AZ2c Route Association
resource "aws_route_table_association" "rancorJenkinsPrivate01RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-2c-private-rancorJenkinsVPC.id
  route_table_id = aws_route_table.rancorJenkinsPrivateRouteTable.id
}
