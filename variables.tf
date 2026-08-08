# ============================================================
# VARIABLES
# ============================================================

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "ap-southeast-1"
}

variable "ami_id" {
  description = "Amazon Linux AMI ID"
  type        = string
}

variable "key_name" {
  description = "Existing AWS EC2 Key Pair name"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}
