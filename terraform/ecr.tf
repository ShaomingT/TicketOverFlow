data "aws_ecr_authorization_token" "ecr_token" {}

provider "docker" {
  registry_auth {
    address  = data.aws_ecr_authorization_token.ecr_token.proxy_endpoint
    username = data.aws_ecr_authorization_token.ecr_token.user_name
    password = data.aws_ecr_authorization_token.ecr_token.password
  }
}

resource "aws_ecr_repository" "concert" {
  name = "concert"
}

resource "aws_ecr_repository" "ticket" {
  name = "ticket"
}

resource "aws_ecr_repository" "user" {
  name = "user"
}

resource "docker_image" "user" {
  name = "${aws_ecr_repository.user.repository_url}:${var.image_version}"
  build {
    context = "../service_user"
    platform  = "linux/amd64"
  }
}

resource "docker_image" "ticket" {
  name = "${aws_ecr_repository.ticket.repository_url}:${var.image_version}"
  build {
    context = "../service_ticket"
    platform  = "linux/amd64"
  }
}
resource "docker_image" "concert" {
  name = "${aws_ecr_repository.concert.repository_url}:${var.image_version}"
  build {
    context = "../service_concert"
    platform  = "linux/amd64"
  }
}

resource "docker_registry_image" "user" {
  name = docker_image.user.name
}
resource "docker_registry_image" "ticket" {
  name = docker_image.ticket.name
}

resource "docker_registry_image" "concert" {
  name = docker_image.concert.name
}