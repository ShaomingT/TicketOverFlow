resource "aws_lb" "ticketoverflow" {
  name               = "ticketoverflow"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.main.id]
  subnets            = data.aws_subnets.private.ids
}


resource "aws_lb_target_group" "concert" {
  name        = "concert"
  port        = 7777
  protocol    = "HTTP"
  vpc_id      = aws_security_group.main.vpc_id
  target_type = "ip"

  health_check {
    path     = "/api/v1/concerts/health"
    port     = "7777"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
  depends_on = [aws_lb.ticketoverflow]
}
resource "aws_lb_target_group" "ticket" {
  name        = "ticket"
  port        = "9999"
  protocol    = "HTTP"
  vpc_id      = aws_security_group.main.vpc_id
  target_type = "ip"

  health_check {
    path     = "/api/v1/tickets/health"
    port     = "9999"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
  depends_on = [aws_lb.ticketoverflow]
}

resource "aws_lb_target_group" "user" {
  name        = "user"
  port        = 8888
  protocol    = "HTTP"
  vpc_id      = aws_security_group.main.vpc_id
  target_type = "ip"

  health_check {
    path     = "/api/v1/users/health"
    port     = "8888"
    protocol = "HTTP"

    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 30
    interval            = 60
  }
  depends_on = [aws_lb.ticketoverflow]
}

resource "aws_lb_listener" "ticketoverflow" {
  load_balancer_arn = aws_lb.ticketoverflow.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = "Loadbalancer: Not Found"
      status_code  = "404"
    }
  }

  depends_on = [
    aws_lb_target_group.concert,
    aws_lb_target_group.ticket,
    aws_lb_target_group.user
  ]
}

resource "aws_lb_listener_rule" "user" {
  listener_arn = aws_lb_listener.ticketoverflow.arn
  priority     = 100

  condition {
    path_pattern {
      values = [
        "/api/v1/users/*",
        "/api/v1/users"
      ]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.user.arn
  }
}

resource "aws_lb_listener_rule" "ticket" {
  listener_arn = aws_lb_listener.ticketoverflow.arn
  priority     = 200

  condition {
    path_pattern {
      values = [
        "/api/v1/tickets/*",
        "/api/v1/tickets"
      ]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ticket.arn
  }
}

resource "aws_lb_listener_rule" "concert" {
  listener_arn = aws_lb_listener.ticketoverflow.arn
  priority     = 300

  condition {
    path_pattern {
      values = [
        "/api/v1/concerts/*",
        "/api/v1/concerts"
      ]
    }
  }
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.concert.arn
  }
}
