from bson import ObjectId
from json import JSONEncoder

class JSONEncoderCustom(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)
