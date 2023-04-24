locals {
  rds_uri           = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.taskoverflow.endpoint}"
  rds_endpoint      = aws_db_instance.taskoverflow.endpoint
  hamilton_endpoint = "${aws_api_gateway_deployment.hamilton.invoke_url}/hamilton"
  ticket_endpoint   = "ticket_endpoint"
  concert_endpoint  = "concert_endpoint"
  user_endpoint     = "user_endpoint"
}
