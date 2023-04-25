#resource "aws_appautoscaling_target" "user" {
#  max_capacity       = 4
#  min_capacity       = 1
#  resource_id        = aws_ecs_service.user.id
#  scalable_dimension = "ecs:service:DesiredCount"
#  service_namespace  = "ecs"
#}
#
#resource "aws_appautoscaling_policy" "user-cpu" {
#  name               = "user-cpu"
#  policy_type        = "TargetTrackingScaling"
#  resource_id        = aws_appautoscaling_target.user.resource_id
#  scalable_dimension = aws_appautoscaling_target.user.scalable_dimension
#  service_namespace  = aws_appautoscaling_target.user.service_namespace
#  target_tracking_scaling_policy_configuration {
#    predefined_metric_specification {
#      predefined_metric_type = "ECSServiceAverageCPUUtilization"
#    }
#    target_value = 20
#  }
#}