from common.database import mongo
from common.utils import Utils
from flask import jsonify
from bson import ObjectId
from pymongo import ReturnDocument


class CashflowsService:
    def __init__(self):
        self.utils_helper = Utils()

    def create(self, request):
        req_json = self.utils_helper.parse_json(request.json)
        create_workspaces = mongo.db['workspaces'].insert_one(req_json)
        workspaces = mongo.db['workspaces'].find_one(
            {"_id": create_workspaces.inserted_id})
        return jsonify(self.utils_helper.parse_json(workspaces))

    def update(self, request):
        req_json = self.utils_helper.parse_json(request.json)
        workspaces = mongo.db['workspaces'].find_one_and_update(
            {"_id": ObjectId(req_json['_id'])}, {"$set": {
                **req_json, '_id': ObjectId(req_json['_id'])
            }}, upsert=True, return_document=ReturnDocument.AFTER)
        print(workspaces)
        return jsonify(self.utils_helper.parse_json(workspaces))
