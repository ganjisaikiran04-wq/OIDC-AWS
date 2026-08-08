



# ============================================================
# DATA - AVAILABILITY ZONES
# ============================================================

data "aws_availability_zones" "available" {
  state = "available"
}


# ============================================================
# VPC
# ============================================================

resource "aws_vpc" "main" {

  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "multicloud-devops-vpc"
  }
}


# ============================================================
# INTERNET GATEWAY
# ============================================================

resource "aws_internet_gateway" "main" {

  vpc_id = aws_vpc.main.id

  tags = {
    Name = "multicloud-devops-igw"
  }
}


# ============================================================
# PUBLIC SUBNET 1
# ============================================================

resource "aws_subnet" "public_1" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.1.0/24"

  availability_zone = data.aws_availability_zones.available.names[0]

  map_public_ip_on_launch = true

  tags = {
    Name = "multicloud-public-subnet-1"
    Type = "Public"
  }
}


# ============================================================
# PUBLIC SUBNET 2
# ============================================================

resource "aws_subnet" "public_2" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.2.0/24"

  availability_zone = data.aws_availability_zones.available.names[1]

  map_public_ip_on_launch = true

  tags = {
    Name = "multicloud-public-subnet-2"
    Type = "Public"
  }
}


# ============================================================
# PRIVATE SUBNET 1
# ============================================================

resource "aws_subnet" "private_1" {

  vpc_id = aws_vpc.main.id

  cidr_block = "10.0.10.0/24"

  availability_zone = data.aws_availability_zones.available.names[0]

  map_public_ip_on_launch = false

  tags = {
    Name = "multicloud-private-subnet-1"
    Type = "Private"
  }
}


# ============================================================
# PUBLIC ROUTE TABLE
# ============================================================

resource "aws_route_table" "public" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "multicloud-public-route-table"
  }
}


# ============================================================
# PUBLIC SUBNET 1 ROUTE ASSOCIATION
# ============================================================

resource "aws_route_table_association" "public_1" {

  subnet_id = aws_subnet.public_1.id

  route_table_id = aws_route_table.public.id
}


# ============================================================
# PUBLIC SUBNET 2 ROUTE ASSOCIATION
# ============================================================

resource "aws_route_table_association" "public_2" {

  subnet_id = aws_subnet.public_2.id

  route_table_id = aws_route_table.public.id
}


# ============================================================
# ELASTIC IP FOR NAT GATEWAY
# ============================================================

resource "aws_eip" "nat" {

  domain = "vpc"

  tags = {
    Name = "multicloud-nat-eip"
  }

  depends_on = [
    aws_internet_gateway.main
  ]
}


# ============================================================
# NAT GATEWAY
# ============================================================

resource "aws_nat_gateway" "main" {

  allocation_id = aws_eip.nat.id

  subnet_id = aws_subnet.public_1.id

  tags = {
    Name = "multicloud-devops-nat"
  }

  depends_on = [
    aws_internet_gateway.main
  ]
}


# ============================================================
# PRIVATE ROUTE TABLE
# ============================================================

resource "aws_route_table" "private" {

  vpc_id = aws_vpc.main.id

  route {

    cidr_block = "0.0.0.0/0"

    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "multicloud-private-route-table"
  }
}


# ============================================================
# PRIVATE SUBNET ROUTE ASSOCIATION
# ============================================================

resource "aws_route_table_association" "private_1" {

  subnet_id = aws_subnet.private_1.id

  route_table_id = aws_route_table.private.id
}


# ============================================================
# ONE SECURITY GROUP
# SSH + HTTP + HTTPS
# ============================================================

resource "aws_security_group" "multicloud" {

  name = "multicloud-devops-sg"

  description = "SSH HTTP HTTPS"

  vpc_id = aws_vpc.main.id


  # ----------------------------------------------------------
  # SSH
  # ----------------------------------------------------------

  ingress {

    description = "SSH"

    from_port = 22

    to_port = 22

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }


  # ----------------------------------------------------------
  # HTTP
  # ----------------------------------------------------------

  ingress {

    description = "HTTP"

    from_port = 80

    to_port = 80

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }


  # ----------------------------------------------------------
  # HTTPS
  # ----------------------------------------------------------

  ingress {

    description = "HTTPS"

    from_port = 443

    to_port = 443

    protocol = "tcp"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }


  # ----------------------------------------------------------
  # OUTBOUND
  # ----------------------------------------------------------

  egress {

    description = "Allow all outbound"

    from_port = 0

    to_port = 0

    protocol = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "multicloud-devops-sg"
  }
}


# ============================================================
# BASTION EC2
# ============================================================

resource "aws_instance" "bastion" {

  ami = var.ami_id

  instance_type = var.instance_type

  subnet_id = aws_subnet.public_1.id

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.multicloud.id
  ]

  associate_public_ip_address = true

  tags = {

    Name = "multicloud-bastion"

    Role = "Bastion"
  }
}


# ============================================================
# PRIVATE APPLICATION EC2
# ============================================================

resource "aws_instance" "application" {

  ami = var.ami_id

  instance_type = var.instance_type

  subnet_id = aws_subnet.private_1.id

  key_name = var.key_name

  vpc_security_group_ids = [
    aws_security_group.multicloud.id
  ]

  associate_public_ip_address = false

  tags = {

    Name = "multicloud-private-app"

    Role = "Application"
  }
}


# ============================================================
# APPLICATION LOAD BALANCER
# ============================================================

resource "aws_lb" "application" {

  name = "multicloud-devops-alb"

  load_balancer_type = "application"

  internal = false

  security_groups = [
    aws_security_group.multicloud.id
  ]

  # ALB needs at least 2 AZs
  subnets = [
    aws_subnet.public_1.id,
    aws_subnet.public_2.id
  ]

  tags = {

    Name = "multicloud-devops-alb"
  }
}


# ============================================================
# ALB TARGET GROUP
# ============================================================

resource "aws_lb_target_group" "application" {

  name = "multicloud-devops-tg"

  port = 80

  protocol = "HTTP"

  vpc_id = aws_vpc.main.id

  target_type = "instance"


  health_check {

    enabled = true

    protocol = "HTTP"

    port = "80"

    path = "/"

    interval = 30

    timeout = 5

    healthy_threshold = 2

    unhealthy_threshold = 3
  }

  tags = {

    Name = "multicloud-devops-target"
  }
}


# ============================================================
# REGISTER PRIVATE EC2 WITH ALB
# ============================================================

resource "aws_lb_target_group_attachment" "application" {

  target_group_arn = aws_lb_target_group.application.arn

  target_id = aws_instance.application.id

  port = 80
}


# ============================================================
# ALB HTTP LISTENER
# ============================================================

resource "aws_lb_listener" "http" {

  load_balancer_arn = aws_lb.application.arn

  port = 80

  protocol = "HTTP"

  default_action {

    type = "forward"

    target_group_arn = aws_lb_target_group.application.arn
  }
}


