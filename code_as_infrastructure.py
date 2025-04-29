
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

