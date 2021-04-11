import json, re, os
import boto3
from boto3.dynamodb.conditions import Key
import logging

id_match = re.compile("[0-9A-Z]{6}")

def lambda_handler(event, context):

    ddb = boto3.resource('dynamodb')
    session_table = ddb.Table(os.environ['DDB_GAME_SESSION_TABLE'])
    
    gameId = event['gameId']
    logging.info(f'parsed game ID {gameId}')

    if not id_match.match(gameId):
        return {
            'statusCode': 400,
            'error': 'InvalidGameId'
        }

    
    # query DDB to find game session

    get_session_resp = session_table.get_item(
            Key={'GameSessionId':gameId}
        )
    if 'Item' not in get_session_resp:
        return {
            'statusCode': 404,
            'error': 'SessionNotFound'
        }
    
    
    session_hostname = get_session_resp['Item']['hostname']

    resp = {
        'host':session_hostname
    }
    
    return {
        'statusCode': 200,
        'body': resp
    }