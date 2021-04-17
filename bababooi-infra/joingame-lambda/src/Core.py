import logging, os, sys, boto3

logger = logging.getLogger()

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
logger.setLevel(logging.INFO)

GAMEID_LENGTH = os.environ.get('GAMEID_LENGTH', 6)
DDB_GAME_SESSION_TABLE = os.environ.get('DDB_GAME_SESSION_TABLE', 'GamesManagerTable')
DDB_HOST_TABLE = os.environ.get('DDB_HOST_TABLE', 'ActiveHosts')
DYNAMO_URL = os.environ.get('DYNAMO_URL', 'https://dynamodb.us-west-2.amazonaws.com')
DYNAMO_REGION = os.environ.get('DYNAMO_REGION', 'us-west-2')

ddb = boto3.resource('dynamodb', endpoint_url=DYNAMO_URL, region_name=DYNAMO_REGION)

print("HELLO?!?!?")

if os.environ.get("ENV") == "development":
    print("creating in-memory tables.. this should only run locally")
    ddb.create_table(
        TableName=DDB_HOST_TABLE,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[{ 'AttributeName': 'hostname', 'KeyType': 'HASH' }],
        AttributeDefinitions=[{ 'AttributeName': 'hostname', 'AttributeType': 'S' }]
    )
    print(f'created table {DDB_HOST_TABLE}')
    ddb.create_table(
        TableName=DDB_GAME_SESSION_TABLE,
        BillingMode="PAY_PER_REQUEST",
        KeySchema=[{ 'AttributeName': 'GameSessionId', 'KeyType': 'HASH' }],
        AttributeDefinitions=[
            { 'AttributeName': 'GameSessionId', 'AttributeType': 'S' }
        ]
    )
    print(f'created table {DDB_GAME_SESSION_TABLE}')

session_table = ddb.Table(DDB_GAME_SESSION_TABLE)
host_table = ddb.Table(DDB_HOST_TABLE)

if os.environ.get("ENV") == "development":
    host_table.put_item(
        Item={
            'hostname': os.environ['GAME_SERVER_HOST']
        }
    )