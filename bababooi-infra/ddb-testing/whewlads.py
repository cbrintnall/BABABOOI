import boto3
from boto3.dynamodb.conditions import Key

import random, os

ddb = boto3.resource('dynamodb')

table = ddb.Table(os.environ['DDB_HOST_TABLE'])

scan_kwargs = {
    'ProjectionExpression':'hostname'
}

response = table.scan(**scan_kwargs)
servers = response['Items']
random.shuffle(servers)

print(servers)



