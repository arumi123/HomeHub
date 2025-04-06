provider "aws" {
  region = "us-east-1"  # 適宜リージョンを設定
}

# IAMロール
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  # Lambda関数にDynamoDBやIoT Coreへのアクセス権を付与
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:*",
          "iot:*"
        ]
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}

# AWS IoT Core
resource "aws_iot_topic_rule" "iot_rule" {
  name = "sensor_data_rule"
  
  sql = "SELECT * FROM 'sensor/data'"
  
  lambda {
    function_arn = aws_lambda_function.iot_data_handler.arn
  }
}

# Lambda関数
resource "aws_lambda_function" "iot_data_handler" {
  filename         = "lambda/function.zip"
  function_name    = "iot_data_handler"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "index.handler"
  runtime          = "nodejs14.x"
  
  source_code_hash = filebase64sha256("lambda/function.zip")
  
  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.sensor_data.name
    }
  }
}

# DynamoDBテーブル
resource "aws_dynamodb_table" "sensor_data" {
  name         = "SensorData"
  hash_key     = "device_id"
  
  attribute {
    name = "device_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  billing_mode = "PAY_PER_REQUEST"
}
