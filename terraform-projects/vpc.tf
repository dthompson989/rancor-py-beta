# Internet VPC
resource "aws_vpc" "rancorMainVPC" {
  cidr_block           = var.rancormainvpc_cidr
  instance_tenancy     = "default"
  enable_dns_support   = "true"
  enable_dns_hostnames = "true"
  enable_classiclink   = "false"
  tags = {
    Name = "rancorMainVPC"
    CIDR = var.rancormainvpc_cidr
  }
}

# rancorMainVPC Public Subnet 1
resource "aws_subnet" "us-east-1a-public-rancorMainVPC" {
  vpc_id                  = aws_vpc.rancorMainVPC.id
  cidr_block              = var.public_subnet_1_cidr
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-1a"
  tags = {
    Name = "us-east-1a-public-rancorMainVPC"
    CIDR = var.public_subnet_1_cidr
  }
}

# rancorMainVPC Public Subnet 2
resource "aws_subnet" "us-east-1b-public-rancorMainVPC" {
  vpc_id                  = aws_vpc.rancorMainVPC.id
  cidr_block              = var.public_subnet_2_cidr
  map_public_ip_on_launch = "true"
  availability_zone       = "us-east-1b"
  tags = {
    Name = "us-east-1b-public-rancorMainVPC"
    CIDR = var.public_subnet_1_cidr
  }
}

# rancorMainVPC Private Subnet 1
resource "aws_subnet" "us-east-1c-private-rancorMainVPC" {
  vpc_id                  = aws_vpc.rancorMainVPC.id
  cidr_block              = var.private_subnet_1_cidr
  map_public_ip_on_launch = "false"
  availability_zone       = "us-east-1c"
  tags = {
    Name = "us-east-1c-private-rancorMainVPC"
    CIDR = var.private_subnet_1_cidr
  }
}

# rancorMainVPC Private Subnet 2
resource "aws_subnet" "us-east-1d-private-rancorMainVPC" {
  vpc_id                  = aws_vpc.rancorMainVPC.id
  cidr_block              = var.private_subnet_2_cidr
  map_public_ip_on_launch = "false"
  availability_zone       = "us-east-1d"
  tags = {
    Name = "us-east-1d-private-rancorMainVPC"
    CIDR = var.private_subnet_2_cidr
  }
}

# rancorMainVPC Internet Gateway
resource "aws_internet_gateway" "rancorMainIGW" {
  vpc_id = aws_vpc.rancorMainVPC.id
  tags = {
    Name = "rancorMainIGW"
  }
}

# rancorMainVPC Public Route Table
resource "aws_route_table" "rancorMainPublicRouteTable" {
  vpc_id = aws_vpc.rancorMainVPC.id
  route {
    cidr_block = var.public_cidr
    gateway_id = aws_internet_gateway.rancorMainIGW.id
  }
  tags = {
    Name = "rancorMainPublicRouteTable"
  }
}

# rancorMainVPC Private Route Table
resource "aws_route_table" "rancorMainPrivateRouteTable" {
  vpc_id = aws_vpc.rancorMainVPC.id
  tags = {
    Name = "rancorMainPrivateRouteTable"
  }
}

# rancorMainVPC Public AZ1a Route Association
resource "aws_route_table_association" "rancorMainPublic01RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-1a-public-rancorMainVPC.id
  route_table_id = aws_route_table.rancorMainPublicRouteTable.id
}

# rancorMainVPC Public AZ1b Route Association
resource "aws_route_table_association" "rancorMainPublic02RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-1b-public-rancorMainVPC.id
  route_table_id = aws_route_table.rancorMainPublicRouteTable.id
}

# rancorMainVPC Private AZ1c Route Association
resource "aws_route_table_association" "rancorMainPrivate01RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-1c-private-rancorMainVPC.id
  route_table_id = aws_route_table.rancorMainPrivateRouteTable.id
}

# rancorMainVPC Private AZ1d Route Association
resource "aws_route_table_association" "rancorMainPrivate02RouteTableAssociation" {
  subnet_id      = aws_subnet.us-east-1d-private-rancorMainVPC.id
  route_table_id = aws_route_table.rancorMainPrivateRouteTable.id
}