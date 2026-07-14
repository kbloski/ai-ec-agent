from typing import Optional, List
from common.mixins.json_serializable import JSONSerializable

class AnalysisDto(JSONSerializable):
    def __init__(
        self,
        id: int,
    ):
        self.id = id

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
        }

        return {k: v for k, v in data.items() if k not in exclude}