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

  max_capacity       = 4
  min_capacity       = 1
  resource_id        = each.value.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "user-cpu" {
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
    target_value = 20
  }
}