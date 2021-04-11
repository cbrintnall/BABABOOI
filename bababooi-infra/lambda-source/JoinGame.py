import json, re, os, random
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()

id_match = re.compile("[0-9A-Z]{6}")
ddb = boto3.resource('dynamodb')

def find_host(userId):
    table = ddb.Table(os.environ['DDB_HOST_TABLE'])

    scan_kwargs = {
        'ProjectionExpression':'hostname'
    }

    response = table.scan(**scan_kwargs)
    servers = response['Items']
    random.shuffle(servers)

    logger.debug(servers)

    # query each server to find availability, for testing we're just grabbing the first one
    # eventually we'll need to handle 503-type scenarios

    return(servers[0]['hostname'])

def join_session(userId, gameId):

    # query DDB to find game session
    session_table = ddb.Table(os.environ['DDB_GAME_SESSION_TABLE'])

    get_session_resp = session_table.get_item(
            Key={'GameSessionId':gameId}
        )

    if 'Item' not in get_session_resp:
        return None
    else:
        return get_session_resp['Item']['hostname']

def lambda_handler(event, context):
    print(event)
    userId = event['userId']

    session_hostname = ''
    
    # No gameId means we're requesting a new session
    if 'gameId' not in event or event['gameId'] == '':

        # check with game servers to find a host
        session_hostname = find_host(userId)
        if not session_hostname:
            return {
                'statusCode': 503,
                'error':'NoHostFound'
            }

    # gameId present, let's try to find the hostname for that session
    else:
        gameId = event['gameId']

        logging.info(f'parsed game ID {gameId}')

        # validate that it's a good gameId
        if not id_match.match(gameId):
            return {
                'statusCode': 400,
                'error': 'InvalidGameId'
            }

        session_hostname = join_session(userId, gameId)

        if not session_hostname:
            return {
                'statusCode': 404,
                'error': 'GameIdNotFound'
            }


    # If we got this far, we have a hostname
    return {
        'statusCode': 200,
        'host':session_hostname
    }


print(lambda_handler({'userId':'test','gameId':'YD9C6G'}, None))