output "iot_rule_name" {
  value = aws_iot_topic_rule.iot_rule.name
}

output "lambda_function_arn" {
  value = aws_lambda_function.iot_data_handler.arn
}
