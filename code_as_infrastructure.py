
# Code as infrastructure

import pulumi
import pulumi_aws as aws

# Define the desired infrastructure as Python code

# 1. Create a  Virtual Private Cloud (VPC)
vpc = aws.ec2.Cpc("my-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "my-vpc",
    })

# 2. Create an Internet Gateway (IGW) to allow internet access
internet_gateway = aws.ec2.InternetGateway("my-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "my-internet-gateway",
    })

# 3. Create a Public Subnet
public_subnet = aws.ec2.Subnet("public-subnet-a",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "public-subnet-a",
    })

#4. Create a Route Table for the Public Subnet
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=internet_gateway.id,
    )],
    tags={
        "Name": "public-route-table",
    })

#5. Associate the Public Subnet with the Public Route Table
public_route_table_association = aws.ec2.RoutTableAssociation("public-subnet-a-association", 
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id)

#6. Create a Security Group for the EC2 Instance
web_sg = aws.ec2.SecurityGroup("web-sg", 
    vpc_id=vpc.id,
    description="Allow HTTP and SSH",
    ingress=[
      aws.ec2.SecurityGroupIngressArgs(
          protocol="tcp",
          from_port=80,
          to_port=80,
          cidr_blocks=["0.0.0.0/0"])])