import boto3
from boto3.dynamodb.conditions import Key

import code

ddb = boto3.resource('dynamodb')

table = ddb.Table('ActiveHosts')

scan_kwargs = {
    'FilterExpression': Key('currentCapacity').gt(0),
    'ProjectionExpression':'currentCapacity, hostname, serverID'
}

response = table.scan(**scan_kwargs)
items = response['Items']
if len(items) == 0:
    print('uh oh')

print(sorted(items, reverse=True, key=lambda k: k['currentCapacity'])[0])



