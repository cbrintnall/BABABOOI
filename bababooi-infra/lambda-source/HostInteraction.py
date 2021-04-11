import requests, os, random
import Core
from Core import logger, ddb

def query_hosts(hostList):
    selected_host = ''

    for hostname in [x['hostname'] for x in hostList]:
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

def find_host(userId):
    table = ddb.Table(os.environ['DDB_HOST_TABLE'])

    scan_kwargs = {
        'ProjectionExpression':'hostname'
    }

    response = table.scan(**scan_kwargs)
    servers = response['Items']
    random.shuffle(servers)

    logger.debug(servers)

    return(query_hosts(servers))

def join_session(hostname, userId, gameId, create):

    post_string = f'http://{hostname}:5000/create?username={userId}&sessionId={gameId}'
    if create:
        post_string += '&create=true'

    r = requests.post(post_string)
    logger.debug(r.text)

    return r.status_code