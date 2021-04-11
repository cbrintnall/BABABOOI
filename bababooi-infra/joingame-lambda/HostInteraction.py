import requests, os, random
from boto3.dynamodb.conditions import Key
import Core
from Core import logger, ddb

def query_hosts(hostList):
    selected_host = ''

    for hostname in hostList:
        r = requests.get(f'http://{hostname}:5000/status')
        if r.status_code != 200:
            logger.warning(f'host {hostname} returned non-200 response {r.status_code}')
            continue
        
        resp = r.json()
        logger.debug(resp)
        capacity = resp['maxRooms'] - len(resp['rooms'])
        logger.info(f'host {hostname} has {capacity} slots')
        
        if capacity > 0:
            selected_host = hostname
            break
        
    return selected_host

def cleanup_old_sessions(hostList):
    for hostname in hostList:
        scan_kwargs = {
            'ProjectionExpression':'GameSessionId',
            'FilterExpression':Key('hostname').eq(hostname)
        }
        database_records = Core.session_table.scan(**scan_kwargs)
        database_sessions = [x['GameSessionId'] for x in database_records['Items']]
        logger.info(database_sessions)

        r = requests.get(f'http://{hostname}:5000/status')
        active_sessions = [x['sessionId'] for x in r.json()['rooms']]
        print(active_sessions)

        for db_sess in database_sessions:
            if db_sess not in active_sessions:
                logger.info(f'Unregistered {db_sess}')
                Core.session_table.delete_item(
                    Key={'GameSessionId':db_sess}
                )


def find_host(userId):
    scan_kwargs = {
        'ProjectionExpression':'hostname'
    }

    response = Core.host_table.scan(**scan_kwargs)
    print(response['Items'])
    hostnames = [x['hostname'] for x in response['Items']]

    random.shuffle(hostnames)
    logger.debug(hostnames)

    cleanup_old_sessions(hostnames)
    return(query_hosts(hostnames))

def join_session(hostname, userId, gameId, create):

    post_string = f'http://{hostname}:5000/create?username={userId}&sessionId={gameId}'
    if create:
        post_string += '&create=true'

    r = requests.post(post_string)
    logger.debug(r.text)

    return r.status_code