
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
          cidr_blocks=["0.0.0.0/0"],
          ),
      aws.ec2.SecurityGroupIngressArgs(
          protocol="tcp",
          from_port=22,
          to_port=22,
          cidr_blocks=["YOUR_PUBLIC_IP/32"], #Replace with your actual public IP for security
          ),
      ],
      egress=[aws.ec2.SecurityGroupEgressArgs(
          protocol="-1",
          from_port=0,
          to_port=0,
          cidr_blocks=["0.0.0.0/0"],
      )],
      tags={
          "Name": "web-sg",
      })

#7. Create an EC2 Instance
web_instance = aws.ec2.Instance("web-instance", 
    ami="ami-xxxxxxxxxxxxxx", # Replace with a valid AWS AMI ID for your region
    instance_type="t2.micro",
    subnet_id=public_subnet.id,
    vpc_security_group_ids=[web_sg.id],
    user_data="""#!/bin/bash
    sudo apt update
    sudo apt install -y apache2
    sudo systemctl start apache2
    echo '<h1>Hello from Pulumi!</h>' | sudo tee /var/www/html/index.html
    """,
    tags={
        "Name": "web-server",
    })

# Output the Public IP of the EC2 Instance
pulumi.export("public_ip", web_instance.public_ip)
pulumi.export("public_dns", web_instance.public_dns)
pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet_id", public_subnet.id)
pulumi.export("security_group_id", web_sg.id)

# Pulumi is an open source infrastructure as code tools to manage cloud infrastructure
# the whole idea is to avoid configuration using web console for vms, databases, networks e
# instead write code to define desired infrastructure state, code is then auto provisioned and managed

# COde above provisions the following:
# VPC - virtual private cloud, logically isolated section of the AWS cloud to launch AWS resources 
# in a virtual network that you define
# internet gateway: a gateway that allows instances in VPC to communicate with the internet

# public subnet, public route table, route table association
# security group - acts as a virtual firewall for EC2 instance

# EC2 instance
# ami - amazon machine image
# instance_type - hardware configuration
# user_data - script that is executed when the instance is launched






