import re, os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

id_match = re.compile("[0-9A-Z]{6}")

def lambda_handler(event, context):
    
    auth_token = os.environ['SECRET_SERVER_TOKEN']
    
    if event['bababooi-auth'] != auth_token:
        return {
            'statusCode': 403,
            'error':'AccessDenied'
        }

    ddb = boto3.resource('dynamodb')
    session_table = ddb.Table(os.environ['DDB_GAME_SESSION_TABLE'])
    
    gameId = event['gameId']
    logger.info(f'parsed game ID {gameId}')

    if not id_match.match(gameId):
        return {
            'statusCode': 400,
            'error': 'InvalidGameId'
        }
    
    # delete from DB - we don't really do any checks here cause I'm lazy

    delete_session_resp = session_table.delete_item(
        Key={'GameSessionId':gameId}
    )
    
    return {
        'statusCode': 200
    }