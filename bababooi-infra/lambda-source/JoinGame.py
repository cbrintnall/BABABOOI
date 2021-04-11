import re, string, random
import boto3
import Core
from Core import logger, ddb

from HostInteraction import query_hosts, find_host, join_session

def register_new_game(gameId, session_hostname):
    Core.session_table.put_item(
        Item={
            'GameSessionId':gameId,
            'hostname': session_hostname
        }
    )


def lambda_handler(event, context):
    print(event)
    userId = event['userId']

    session_hostname = ''

    createGame = False
    
    # No gameId means we're requesting a new session
    if 'gameId' not in event or len(event['gameId']) == 0:

        # create a new gameId
        gid_length = int(Core.GAMEID_LENGTH)
        gameId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(gid_length))

        # check with game servers to find a host
        session_hostname = find_host(userId)
        if not session_hostname:
            return {
                'statusCode': 503,
                'error':'NoHostFound'
            }

        createGame = True


    # gameId present, let's try to find the hostname for that session
    else:
        gameId = event['gameId']
        id_match = re.compile("[0-9A-Z]{6}")
        logger.info(f'parsed game ID {gameId}')

        # validate that it's a good gameId
        if not id_match.match(gameId):
            return {
                'statusCode': 400,
                'error': 'InvalidGameId'
            }

        # query DDB to find game session host

        get_session_resp = Core.session_table.get_item(
            Key={'GameSessionId':gameId}
        )

        if 'Item' not in get_session_resp:
            return {
                'statusCode': 404,
                'error': 'GameIdNotFound'
            }

        session_hostname = get_session_resp['Item']['hostname']

    
    # By the time we get here, the above logic will have defined:
    # gameId
    # userId (mandatory input)
    # session_hostname: determined either by a) finding the host associated with a session, or b) finding a brand new host
    # createGame: default false, only set to True if gameId is null
    
    
    resp_code = join_session(session_hostname, userId, gameId, createGame)


    if resp_code == 200:
        if createGame == True:
            register_new_game(gameId, session_hostname)

        return {
            'statusCode': 200,
            'host':session_hostname+':5000',
            'gameId':gameId
        }
    elif resp_code == 404:
        return {
            'statusCode': 404,
            'error': 'GameIdNotFound'
        }
    else:
        return {
            'statusCode': 500,
            'error': 'UnknownError'
        }


    # If we got this far, we have a hostname
    


print(lambda_handler({'userId':'test3'}, None))