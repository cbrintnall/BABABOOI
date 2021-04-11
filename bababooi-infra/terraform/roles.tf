#Defining IAM role for the Lambda function

resource "aws_iam_role" "JoinSessionRole" {
  name = "JoinSessionLambdaRole"

  assume_role_policy = data.aws_iam_policy_document.lambda_assume_policy.json
  managed_policy_arns = [ aws_iam_policy.lambda_exec_log_write.arn,  "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"]
}


data "aws_iam_policy_document" "lambda_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "lambda_exec_log_write" {
  name        = "lambda_exec_log_write"
  path        = "/"
  description = "Policy for allowing Lambda functions to write to CW"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:us-west-2:797805152351:log-group:/aws/lambda/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:us-west-2:797805152351:*"
      },
    ]
  })
}