# ============================================================
# OUTPUTS
# ============================================================

output "vpc_id" {

  value = aws_vpc.main.id
}


output "public_subnet_1" {

  value = aws_subnet.public_1.id
}


output "public_subnet_2" {

  value = aws_subnet.public_2.id
}


output "private_subnet" {

  value = aws_subnet.private_1.id
}


output "bastion_public_ip" {

  value = aws_instance.bastion.public_ip
}


output "bastion_public_dns" {

  value = aws_instance.bastion.public_dns
}


output "private_ec2_ip" {

  value = aws_instance.application.private_ip
}


output "alb_dns_name" {

  value = aws_lb.application.dns_name
}


output "application_url" {

  value = "http://${aws_lb.application.dns_name}"
}