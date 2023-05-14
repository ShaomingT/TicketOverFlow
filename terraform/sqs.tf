resource "aws_sqs_queue" "hamilton" {
  name                      = "hamilton.fifo"
  fifo_queue                = true
  content_based_deduplication = true
  visibility_timeout_seconds = 180

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.hamilton_dead_letter.arn
    maxReceiveCount     = 1
  })
}

resource "aws_sqs_queue" "hamilton_dead_letter" {
  name = "hamilton_dead_letter.fifo"
  fifo_queue = true
}