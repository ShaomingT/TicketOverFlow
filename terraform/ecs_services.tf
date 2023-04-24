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
}