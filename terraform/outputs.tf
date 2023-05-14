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
#
#output "hamilton_endpoint" {
#  value = "${aws_api_gateway_deployment.hamilton.invoke_url}/hamilton"
#}

output "user_url" {
  value = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/users"
}

output "ticket_url" {
  value = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/tickets"
}

output "concert_url" {
  value = "http://${aws_lb.ticketoverflow.dns_name}/api/v1/concerts"
}

output "hamilton_sqs" {
    value = aws_sqs_queue.hamilton.arn
}

output "api_url" {
  value = "http://${aws_lb.ticketoverflow.dns_name}/api/v1"
}

#output "container_image_concert_url" {
#    value = "${aws_ecr_repository.concert.repository_url}:latest"
#}
#
#output "container_image_ticket_url" {
#    value = "${aws_ecr_repository.ticket.repository_url}:latest"
#}
#
#output "container_image_user_url" {
#    value = "${aws_ecr_repository.user.repository_url}:latest"
#}