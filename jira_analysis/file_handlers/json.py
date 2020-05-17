import json

from datetime import date, datetime


class _Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


def dump(obj, to):
    return json.dump(obj, to, cls=_Encoder, indent=2)
