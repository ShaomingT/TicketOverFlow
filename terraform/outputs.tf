output "default_vpc_id" {
    value = data.aws_vpc.default.id
}


output "rds_endpoint" {
  value = aws_db_instance.taskoverflow.endpoint
}

output "rds_username" {
  sensitive = true
  value = var.db_username
}

output "rds_password" {
  sensitive = true
  value = var.db_password
}

output "rds_uri" {
  sensitive = true
  value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.taskoverflow.endpoint}/${aws_db_instance.taskoverflow.db_name}"
}

output "api_gateway_endpoint_url" {
  value = join("", ["https://", substr(aws_api_gateway_rest_api.hamilton.execution_arn, 19, -1), "/prod/hamilton"])
}
