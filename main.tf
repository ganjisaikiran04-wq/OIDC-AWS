provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "main-vpc"
  }
}

# resource "aws_subnet" "subnet_a" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.1.0/24"
#   availability_zone = "ap-southeast-1a"
#   tags = {
#     Name = "subnet-a"
#   }
# }

# resource "aws_subnet" "subnet_b" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = "10.0.2.0/24"
#   availability_zone = "ap-southeast-1b"
#   tags = {
#     Name = "subnet-b"
#   }
# }
