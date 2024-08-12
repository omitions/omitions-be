from common.database import mongo
from common.utils import Utils
from flask import jsonify, g
from bson import ObjectId
from pymongo import ReturnDocument


class CashflowsService:
    def __init__(self):
        self.utils_helper = Utils()

    def create(self, request):
        req_json = self.utils_helper.parse_json(request.json)
        req_json['user_id'] = ObjectId(g.user['_id'])
        req_json['workspaces_id'] = ObjectId(req_json['workspaces_id'])
        create_cashflow = mongo.db['cashflows'].insert_one(req_json)
        cashflow = mongo.db['cashflows'].find_one(
            {"_id": create_cashflow.inserted_id})
        return jsonify(self.utils_helper.parse_json(cashflow))

    def update(self, request):
        return True

    def list(self, request):
        user_id = ObjectId(g.user['_id'])
        workspace_id = request.args.get('workspace_id')
        date = request.args.get('date')
        print(workspace_id, user_id)
        if not workspace_id:
              return jsonify({'message': 'Workspace not found!!!'}), 400
        cashflow = mongo.db['cashflows'].find(
            {
                "user_id": user_id, 
                "workspaces_id": ObjectId(workspace_id),
                "date_time": {"$regex": date, "$options": "i"}
            }
        )
        return jsonify(self.utils_helper.parse_json(cashflow))
    def calendar(self, request):
        user_id = ObjectId(g.user['_id'])
        workspace_id = request.args.get('workspace_id')
        date = request.args.get('date')
        print(workspace_id, user_id)
        if not workspace_id:
            return jsonify({'message': 'Workspace not found!!!'}), 400
        cashflow = mongo.db['cashflows'].aggregate(
            [
                {
                    "$match": {
                        "user_id": user_id, 
                        "workspaces_id": ObjectId(workspace_id),
                        "date_time": {"$regex": date, "$options": "i"}
                    }
                },
                {
                "$addFields": {
                        "date_10": {"$substr": ["$date_time", 0, 10]}
                    }
                },
                {
                    "$group": {
                        "date": {
                            "$first": "$date_10"    
                        },
                        "_id": "$date_10",
                        "count": {"$sum": 1},
                        "amount": {"$sum": "$amount"}
                    }
                }
            ]
        )
        return jsonify(self.utils_helper.parse_json(cashflow))
