import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)