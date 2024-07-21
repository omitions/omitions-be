from common.config import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import json_util
import json

uri = config['PROD']['DB_URI']
mongo = MongoClient(uri, server_api=ServerApi('1'))
try:
    mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def parse_json(data):
    return json.loads(json_util.dumps(data))
