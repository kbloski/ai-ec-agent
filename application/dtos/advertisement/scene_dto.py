from typing import Optional

from common.mixins.json_serializable import JSONSerializable


class SceneDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        type: str,
        description: Optional[str],
        duration_seconds: Optional[int],
    ):
        self.id = id
        self.type = type
        self.description = description
        self.duration_seconds = duration_seconds

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "duration_seconds": self.duration_seconds,
        }

        return {k: v for k, v in data.items() if k not in exclude}
