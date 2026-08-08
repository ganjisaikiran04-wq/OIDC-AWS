terraform {
  backend "s3" {
    bucket = "Bucketforpracise44"
    key    = "multi-cloud-devops/terraform.tfstate"
    region = "ap-southeast-1"
    use_lockfile = true   # Enable S3-native state locking
    encrypt = true  # Optional: encrypt Terraform state at rest
  }
}

