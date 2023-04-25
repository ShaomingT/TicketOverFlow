resource "aws_ecs_service" "concert" {
  name            = "concert"
  cluster         = aws_ecs_cluster.ticketoverflow.id
  task_definition = aws_ecs_task_definition.concert.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.concert.arn
    container_name = "concert"
    container_port = "7777"
  }
  depends_on = [aws_lb_listener.ticketoverflow]
}

resource "aws_ecs_service" "user" {
  name            = "user"
  cluster         = aws_ecs_cluster.ticketoverflow.id
  task_definition = aws_ecs_task_definition.user.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.user.arn
    container_name = "user"
    container_port = "8888"
  }
  depends_on = [aws_lb_listener.ticketoverflow]
}

resource "aws_ecs_service" "ticket" {
  name            = "ticket"
  cluster         = aws_ecs_cluster.ticketoverflow.id
  task_definition = aws_ecs_task_definition.ticket.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.ticket.arn
    container_name = "ticket"
    container_port = "9999"
  }
  depends_on = [aws_lb_listener.ticketoverflow]
}