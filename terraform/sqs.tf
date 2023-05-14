resource "aws_sqs_queue" "hamilton" {
  name                        = "hamilton.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  visibility_timeout_seconds  = 180
}
