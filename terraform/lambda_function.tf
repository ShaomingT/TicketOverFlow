# define a variable of filepath to the lambda function

resource "aws_lambda_function" "hamilton" {
  filename         = var.lambda_function_payload
  function_name    = "hamilton"
  role             = data.aws_iam_role.lab.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = base64sha256(filebase64(var.lambda_function_payload))
  runtime          = "python3.9"
  timeout          = "180"
  memory_size      = "1024"

  environment {
    variables = {
      "DB_HOST" = aws_db_instance.taskoverflow.endpoint
      "DB_NAME" = aws_db_instance.taskoverflow.db_name
      "DB_USER" = aws_db_instance.taskoverflow.username
      "DB_PASS" = aws_db_instance.taskoverflow.password

    }
  }
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.hamilton.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.hamilton.execution_arn}/*/POST/hamilton"
}

resource "aws_api_gateway_deployment" "hamilton" {
  depends_on = [aws_lambda_permission.allow_api_gateway]
  rest_api_id = aws_api_gateway_rest_api.hamilton.id
  stage_name = "prod"
}