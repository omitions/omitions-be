from bson import json_util, ObjectId
import json
import bcrypt


class Utils:
    def generate_token(self):
        return 'ini token'

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, hashed_password, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def parse_json(self, data):
        jsonData = json.loads(json_util.dumps(data))
        if 'password' in jsonData:
            del jsonData['password']
        if '_id' in jsonData:
            if not isinstance(jsonData['_id'], str):
                jsonData['_id'] = jsonData['_id']['$oid']
        return jsonData
