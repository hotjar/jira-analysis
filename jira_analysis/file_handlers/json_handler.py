import json

from datetime import date, datetime
from enum import Enum
from typing import Any, IO, Optional


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Optional[Any]:
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        return None


def dump(obj: Any, to: IO[str]) -> None:
    return json.dump(obj, to, cls=_Encoder, indent=2)
