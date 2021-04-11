import logging, os, sys
import boto3

logger = logging.getLogger()

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger.addHandler(handler)
logger.setLevel(logging.INFO)

DDB_GAME_SESSION_TABLE = os.environ['DDB_GAME_SESSION_TABLE']
GAMEID_LENGTH = os.environ['GAMEID_LENGTH']
DDB_HOST_TABLE = os.environ['DDB_HOST_TABLE']

ddb = boto3.resource('dynamodb')
session_table = ddb.Table(DDB_GAME_SESSION_TABLE)
host_table = ddb.Table(DDB_HOST_TABLE)