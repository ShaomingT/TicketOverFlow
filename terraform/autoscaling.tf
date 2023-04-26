locals {
  cluster_name = aws_ecs_cluster.ticketoverflow.name

  microservices = {
    "user" : {
      name : "user",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.user.name}",
      resource_label : "${aws_lb.ticketoverflow.arn_suffix}/${aws_lb_target_group.user.arn_suffix}",
    },
    "concert" : {
      name : "concert",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.concert.name}",
        resource_label : "${aws_lb.ticketoverflow.arn_suffix}/${aws_lb_target_group.concert.arn_suffix}",
    },
    "ticket" : {
      name : "ticket",
      resource_id : "service/${local.cluster_name}/${aws_ecs_service.ticket.name}",
        resource_label : "${aws_lb.ticketoverflow.arn_suffix}/${aws_lb_target_group.ticket.arn_suffix}",
    },
  }
  target_connection_per_task = 50
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
    target_value       = 10
    scale_in_cooldown  = 120
    scale_out_cooldown = 120
  }
}

resource "aws_appautoscaling_policy" "connection_count" {
  for_each = local.microservices

  name               = "${each.value.name}-connection-count"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = each.value.resource_label
    }
    target_value       = local.target_connection_per_task
    scale_in_cooldown  = 120
    scale_out_cooldown = 120
  }

}