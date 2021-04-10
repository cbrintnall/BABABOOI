import json, random, string, os
import boto3
from boto3.dynamodb.conditions import Key
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_host(ddb):

    hosts_table = ddb.Table(os.environ['DDB_HOST_TABLE'])
    
    # query DDB to find a host that has capacity for a new session
    
    scan_kwargs = {
        'FilterExpression': Key('currentCapacity').gt(0),
        'ProjectionExpression':'currentCapacity, hostname, serverID'
    }
    
    scan_resp = hosts_table.scan(**scan_kwargs)
    hosts = scan_resp['Items']
    sorted_hosts = sorted(hosts, reverse=True, key=lambda k: k['currentCapacity'])
    
    if len(hosts) == 0:
        return None
    
    # Picking the least-busy host
    selected_host = sorted_hosts[0]
    
    server_hostname = selected_host['hostname']
    
    # update DDB entry for this host

    update_resp = hosts_table.update_item(
        Key={'serverID':selected_host['serverID']},
        UpdateExpression="set currentCapacity=:cap",
        ExpressionAttributeValues={
            ':cap': int(selected_host['currentCapacity']) - 1
        },
        ReturnValues="UPDATED_NEW"
    )

    # inform host this is happening?

    return server_hostname


def create_session(ddb, server_hostname):

    sid_length = int(os.environ['SESSION_ID_LENGTH'])
    valid_session = False

    session_table = ddb.Table(os.environ['DDB_GAME_SESSION_TABLE'])

    # create new game session ID, validate no collision
    session_id = ''

    while not valid_session:
        session_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(sid_length))

        check_collision_resp = session_table.get_item(
            Key={'GameSessionId':session_id}
        )

        if 'Item' not in check_collision_resp:
            logger.info(f'new session ID {session_id}')
            valid_session = True
        else:
            logger.warning(f'Collided on {session_id}')


    # insert into game session table
    put_response = session_table.put_item(
        Item={
            'GameSessionId':session_id,
            'Hostname':server_hostname
        }
    )

    return session_id



def lambda_handler(event, context):
    
    ddb = boto3.resource('dynamodb')

    server_hostname = get_host(ddb)

    if not server_hostname:
        return {
            'statusCode': 503,
            'error':'NoCapacity'
        } 
    
    # register new session and host pair in DDB
    logger.debug('entering session ID generation')
    session_id = create_session(ddb, server_hostname)
    
    resp = {
        'gameId':session_id,
        'host':server_hostname
    }
    
    # return session ID and hostname
    return {
        'statusCode': 200,
        'body': resp
    }


print(lambda_handler(None, None))