# Configure the AWS provider
provider "aws" {
  region = "us-east-1"  #default region
}

# This code will create AWS API Gateway
resource "aws_api_gateway_rest_api" "ssl_expiration_api" {
  name = "SSL Expiration API"
}

# block for the path  ssl expiration. this resource is under the root resource (parent)
resource "aws_api_gateway_resource" "ssl_expiration" {
  rest_api_id = aws_api_gateway_rest_api.ssl_expiration_api.id
  parent_id = aws_api_gateway_rest_api.ssl_expiration_api.root_resource_id
  path_part = "ssl-expiration"
}

# block for GET method
resource "aws_api_gateway_method" "get_ssl_expiration" {
  rest_api_id = aws_api_gateway_rest_api.ssl_expiration_api.id
  resource_id = aws_api_gateway_resource.ssl_expiration.id
  http_method = "GET"
  authorization = "NONE"  # do not require any authorization 
}

# create an integration. it indicate that the lambda function should use POST
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.ssl_expiration_api.id
  resource_id = aws_api_gateway_resource.ssl_expiration.id
  http_method = aws_api_gateway_method.get_ssl_expiration.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789012:function:check_ssl_expiration/invocations"
# uri is supposed to be the Amazon Resource Nmae (ARN) of the lambda function. I chose 123456789012 randomly 
}

# Create a deployment of the API with the name prod
resource "aws_api_gateway_deployment" "api_deployment" {
  depends_on = [aws_api_gateway_integration.lambda_integration]
  rest_api_id = aws_api_gateway_rest_api.ssl_expiration_api.id
  stage_name = "prod"
}

# Create a stage of the API with the name prod
resource "aws_api_gateway_stage" "api_stage" {
  depends_on = [aws_api_gateway_deployment.api_deployment]
  rest_api_id = aws_api_gateway_rest_api.ssl_expiration_api.id
  stage_name = "prod"
  deployment_id = aws_api_gateway_deployment.api_deployment.id
}

# block to create a plan that require a key a request limit of 1000
resource "aws_api_gateway_usage_plan" "usage_plan" {
  name = "SSL Expiration API Usage Plan"
  gateway_api_key_required = true
  usage_plan_quota {
    limit = 1000
    period = "MONTH"
  }
  usage_plan_throttle {
    rate_limit = 10
    burst_limit = 10
  }
}

# Blck to specify the API_KEY
resource "aws_api_gateway_usage_plan_key" "usage_plan_key" {
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan.id
  key_id = aws_api_gateway_api_key.api_key.id
  key_type = "API_KEY"
}

