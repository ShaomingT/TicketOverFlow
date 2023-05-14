locals {
  rds_uri           = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.taskoverflow.endpoint}"
  rds_endpoint      = aws_db_instance.taskoverflow.endpoint
#  hamilton_endpoint = "${aws_api_gateway_deployment.hamilton.invoke_url}/hamilton"
  ticket_endpoint   = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/tickets"
  concert_endpoint  = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/concerts"
  user_endpoint     = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/users"
}
