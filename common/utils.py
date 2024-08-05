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
        def convert_objectid_to_string(obj):
            if isinstance(obj, dict):
                if "$oid" in obj:
                    return str(obj["$oid"])
                else:
                    return {k: convert_objectid_to_string(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_objectid_to_string(item) for item in obj]
            else:
                return obj

        def cunsad(jsonData):
            serialize = convert_objectid_to_string(jsonData)
            if 'password' in serialize:
                del serialize['password']
            return serialize

        payload = json.loads(json_util.dumps(data))
        if not isinstance(payload, list):
            return cunsad(payload)
        return list(map(cunsad, payload))
