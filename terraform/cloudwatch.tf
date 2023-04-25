resource "aws_cloudwatch_log_group" "ecs_logs" {
  name = "/ecs/ticketoverflow"
}

resource "aws_cloudwatch_log_group" "connections_per_five_second" {
  name = "connections_per_five_second"
}

resource "aws_cloudwatch_log_metric_filter" "connections_per_five_second" {
  name           = "connections_per_five_second"
  pattern        = "{ $.event = \"connection\" }" # Replace this with a pattern that matches your log events
  log_group_name = aws_cloudwatch_log_group.connections_per_five_second.name

  metric_transformation {
    name      = "ConnectionsPerFiveSecond"
    namespace = "MyApp"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "connections_per_five_second" {
  alarm_name           = "connections_per_five_second"
  comparison_operator  = "GreaterThanOrEqualToThreshold"
  evaluation_periods   = "1"
  metric_name          = "ConnectionsPerSecond"
  namespace            = "MyApp"
  period               = 10               # Check the metric every 5 seconds
  statistic            = "SampleCount"
  threshold            = 300             # Set the threshold to 100 connections
  alarm_description    = "This metric checks for 100 connections per 5 seconds"
  alarm_actions        = [aws_sns_topic.connections_per_five_second.arn]
}

resource "aws_sns_topic" "connections_per_five_second" {
  name = "connections_per_five_second"
}
