#resource "aws_api_gateway_rest_api" "hamilton" {
#  name = "hamilton_api"
#}
#
#resource "aws_api_gateway_resource" "hamilton" {
#  rest_api_id = aws_api_gateway_rest_api.hamilton.id
#  parent_id   = aws_api_gateway_rest_api.hamilton.root_resource_id
#  path_part   = "hamilton"
#}
#
#resource "aws_api_gateway_method" "hamilton" {
#  rest_api_id   = aws_api_gateway_rest_api.hamilton.id
#  resource_id   = aws_api_gateway_resource.hamilton.id
#  http_method   = "POST"
#  authorization = "NONE"
#}
#resource "aws_api_gateway_integration" "hamilton" {
#  rest_api_id             = aws_api_gateway_rest_api.hamilton.id
#  resource_id             = aws_api_gateway_resource.hamilton.id
#  http_method             = aws_api_gateway_method.hamilton.http_method
#  integration_http_method = "POST"
#  type                    = "AWS"
#  uri                     = aws_lambda_function.hamilton.invoke_arn
#
#  request_parameters = {
#    "integration.request.header.X-Amz-Invocation-Type" = "'Event'"
#  }
#}
#
#resource "aws_api_gateway_method_response" "hamilton" {
#  rest_api_id = aws_api_gateway_rest_api.hamilton.id
#  resource_id = aws_api_gateway_resource.hamilton.id
#  http_method = aws_api_gateway_method.hamilton.http_method
#  status_code = "202"
#
#  response_models = {
#    "application/json" = "Empty"
#  }
#}
#resource "aws_api_gateway_integration_response" "hamilton" {
#  rest_api_id = aws_api_gateway_rest_api.hamilton.id
#  resource_id = aws_api_gateway_resource.hamilton.id
#  http_method = aws_api_gateway_method.hamilton.http_method
#  status_code = aws_api_gateway_method_response.hamilton.status_code
#
#  depends_on         = [aws_api_gateway_integration.hamilton]
#  response_templates = {
#    "application/json" = ""
#  }
#}