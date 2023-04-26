resource "aws_cloudwatch_log_group" "ecs_logs" {
  name = "/ecs/ticketoverflow"
}

#resource "aws_cloudwatch_metric_alarm" "active_connection_count_alarm" {
#  for_each            = local.microservices
#  alarm_name          = "active-connection-count-alarm-${each.key}"
#  comparison_operator = "GreaterThanOrEqualToThreshold"
#  evaluation_periods  = "1"
#  metric_name         = "ActiveConnectionCount"
#
#}
