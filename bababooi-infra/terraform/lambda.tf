module "lambda_function" {
    source = "terraform-aws-modules/lambda/aws"

    function_name = "JoinGame"
    handler = "JoinGame.lambda_handler"
    runtime = "python3.8"
    publish = true

    source_path = [
        {
            path = "../lambda-source",
            
        },
        {
            path = "../lambda-source/package"
        }
    ]
    store_on_s3 = true
    s3_bucket = "bababooi-lambda-sources"

    environment_variables = {
        DDB_GAME_SESSION_TABLE = "GamesManagerTable",
        DDB_HOST_TABLE = "ActiveHosts",
        GAMEID_LENGTH = 6
    } 
    allowed_triggers = {
        APIGatewayAny = {
        service    = "apigateway"
        source_arn = "arn:aws:execute-api:us-west-2:797805152351:*"
        }
    }

    timeout = 15
    create_role = false
    lambda_role = aws_iam_role.JoinSessionRole.arn
}