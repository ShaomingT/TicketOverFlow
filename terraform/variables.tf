variable "db_username" {
  description = "Database administrator username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database administrator password"
  type        = string
  sensitive   = true
}

variable "lambda_function_payload" {
  default = "../lambda_hamilton/lambda_function_payload.zip"
}

variable "image_version" {
    default = "1.66"
}
