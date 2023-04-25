locals {
  cluster_name = aws_ecs_cluster.ticketoverflow.name

  microservices = {
    "user" : {
      name : "user",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.user.name}",
    },
    "concert" : {
      name : "concert",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.concert.name}",
    },
    "ticket" : {
      name : "ticket",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.ticket.name}",
    },
  }
}


resource "aws_appautoscaling_target" "main" {
  for_each = local.microservices

  max_capacity       = 10
  min_capacity       = 1
  resource_id        = each.value.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ticketoverflow" {
  for_each = local.microservices

  name               = "${each.value.name}-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 10
  }
}

resource "aws_appautoscaling_policy" "connections_scaling" {
  for_each = local.microservices

  name               = "${each.value.name}-connections"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace
  target_tracking_scaling_policy_configuration {
    customized_metric_specification {
      metric_name = aws_cloudwatch_metric_alarm.connections_per_five_second.metric_name # Custom metric name
      namespace   = aws_cloudwatch_metric_alarm.connections_per_five_second.namespace
      # Custom metric namespace
      statistic   = "SampleCount"          # Use "SampleCount" for the number of connections
      unit        = "Count"                # Unit for the metric
    }
    target_value = 30 # Scale up when the average is 30 connections per second (300 connections per 10 seconds)
  }
}
