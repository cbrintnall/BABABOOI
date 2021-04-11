import logging, os, sys
import boto3

logger = logging.getLogger()

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

DDB_GAME_SESSION_TABLE = os.environ['DDB_GAME_SESSION_TABLE']
GAMEID_LENGTH = os.environ['GAMEID_LENGTH']

ddb = boto3.resource('dynamodb')