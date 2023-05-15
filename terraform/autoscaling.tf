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
  target_connection_per_task = 300
}


resource "aws_appautoscaling_target" "main" {
  for_each = local.microservices

  max_capacity       = 50
  min_capacity       = 1
  resource_id        = each.value.resource_id
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

#resource "aws_appautoscaling_policy" "ticketoverflow" {
#  for_each = local.microservices
#
#  name               = "${each.value.name}-cpu"
#  policy_type        = "TargetTrackingScaling"
#  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
#  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
#  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace
#  target_tracking_scaling_policy_configuration {
#    predefined_metric_specification {
#      predefined_metric_type = "ECSServiceAverageCPUUtilization"
#    }
#    target_value       = 10
#    scale_in_cooldown  = 120
#    scale_out_cooldown = 30
#  }
#}

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
    target_value       = 80
    scale_in_cooldown  = 240
    scale_out_cooldown = 15
  }

}

resource "aws_cloudwatch_metric_alarm" "cpu_alarm_high" {
  for_each = local.microservices

  alarm_name          = "${each.value.name}-high-cpu-utilization"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = "8"
  alarm_description   = "This metric checks cpu utilization"
  alarm_actions       = [aws_appautoscaling_policy.cpu_scale_up[each.key].arn]
  dimensions          = {
    ClusterName = local.cluster_name
    ServiceName = each.value.name
  }
}

resource "aws_appautoscaling_policy" "cpu_scale_up" {
  for_each = local.microservices

  name               = "${each.value.name}-cpu"
  policy_type        = "StepScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 30
    metric_aggregation_type = "Average"

    step_adjustment {
      scaling_adjustment          = 2
      metric_interval_lower_bound = 0
    }
  }
}


resource "aws_cloudwatch_metric_alarm" "cpu_alarm_low" {
  for_each = local.microservices

  alarm_name          = "${each.value.name}-low-cpu-utilization"
  comparison_operator = "LessThanOrEqualToThreshold"
  evaluation_periods  = "3"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "60"
  statistic           = "Average"
  threshold           = "5"
  alarm_description   = "This metric checks cpu utilization"
  alarm_actions       = [aws_appautoscaling_policy.cpu_scale_down[each.key].arn]
  dimensions          = {
    ClusterName = local.cluster_name
    ServiceName = each.value.name
  }
}


resource "aws_appautoscaling_policy" "cpu_scale_down" {
  for_each = local.microservices

  name               = "${each.value.name}-cpu-scale-down"
  policy_type        = "StepScaling"
  resource_id        = aws_appautoscaling_target.main[each.key].resource_id
  scalable_dimension = aws_appautoscaling_target.main[each.key].scalable_dimension
  service_namespace  = aws_appautoscaling_target.main[each.key].service_namespace

  step_scaling_policy_configuration {
    adjustment_type         = "ChangeInCapacity"
    cooldown                = 240
    metric_aggregation_type = "Average"

    step_adjustment {
      scaling_adjustment          = -2
      metric_interval_upper_bound = 0
    }
  }
}