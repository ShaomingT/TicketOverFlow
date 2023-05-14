resource "aws_sqs_queue" "hamilton" {
  name                       = "hamilton"
  visibility_timeout_seconds = 180
}
