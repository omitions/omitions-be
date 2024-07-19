from common.config import config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = config['PROD']['DB_URI']
mongo = MongoClient(uri, server_api=ServerApi('1'))
try:
    mongo.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)