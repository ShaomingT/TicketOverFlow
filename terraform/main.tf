terraform {
   required_providers {
      aws = {
         source = "hashicorp/aws"
         version = "~> 4.0"
      }
      docker = {
         source = "kreuzwerker/docker"
         version = "3.0.2"
      }
   }
}

provider "aws" {
   region = "us-east-1"
   shared_credentials_files = ["./credentials"]
}

data "aws_iam_role" "lab" {
   name = "LabRole"
}

data "aws_vpc" "default" {
   default = true
}

data "aws_subnets" "private" {
   filter {
      name = "vpc-id"
      values = [data.aws_vpc.default.id]
   }
}

#resource "aws_servicequotas_service_quota" "lambda_concurrent" {
#  quota_code   = "L-B99A9384"
#  service_code = "lambda"
#  value        = 1000
#}

