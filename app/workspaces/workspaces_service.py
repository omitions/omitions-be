from common.database import mongo
from common.utils import Utils
from flask import jsonify, g
from bson import ObjectId
from pymongo import ReturnDocument


class WorkspacesService:
    def __init__(self):
        self.utils_helper = Utils()

    def create(self, request):
        print(g, "ini global")
        user_id = ObjectId(g.user['_id'])
        req_json = self.utils_helper.parse_json(request.json)
        create_workspaces = mongo.db['workspaces'].insert_one(
            {**req_json, "user_id": user_id})
        workspaces = mongo.db['workspaces'].find_one(
            {"_id": create_workspaces.inserted_id})
        return jsonify(self.utils_helper.parse_json(workspaces))

    def update(self, request):
        req_json = self.utils_helper.parse_json(request.json)
        workspaces = mongo.db['workspaces'].find_one_and_update(
            {"_id": ObjectId(req_json['_id'])}, {"$set": {
                **req_json, '_id': ObjectId(req_json['_id'])
            }}, return_document=ReturnDocument.AFTER)
        if not workspaces:
            return jsonify({'message': 'Workspaces not found'}), 404

        return jsonify(self.utils_helper.parse_json(workspaces))

    def delete(self, request):
        req_json = self.utils_helper.parse_json(request.json)
        workspaces = mongo.db['workspaces'].delete_one(
            {"_id": ObjectId(req_json['_id'])})
        print(workspaces.deleted_count)
        if not workspaces.deleted_count:
            return jsonify({'message': 'Workspaces not found'}), 404
        return jsonify({'message': 'Delete success'})

    def list(self, request):
        user_id = ObjectId(g.user['_id'])
        workspaces = mongo.db['workspaces'].find(
            {"user_id": user_id}
        )
        return jsonify(self.utils_helper.parse_json(workspaces))
