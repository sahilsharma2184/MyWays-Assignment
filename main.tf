provider "aws" {
    region = "us-east-1" 
}

resource "aws_instance" "myways_instance" {
    ami ="ami-0866a3c8686eaeeba"
    instance_type = "t2.micro"
    key_name = "ec2_myways_KP"
    vpc_security_group_ids = ["sg-058d2104aa47f4ad3"]
    tags = {
      Name = "My_ways_instance"
    }
}

resource "aws_s3_bucket" "myways_s3_bucket" {
  bucket = "myways-s3-bucket-2184"
}

resource "aws_secretsmanager_secret" "api_credentials" {
  name        = "api_credentials_2184"
  description = "API credentials for document processing."
}

resource "aws_sqs_queue" "document_queue" {
  name = "document-processing-queue_2184"
}