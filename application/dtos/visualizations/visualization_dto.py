from common.mixins.json_serializable import JSONSerializable


class VisualizationDto(JSONSerializable):
    def __init__(
        self,
        id: int,
        format: str,
        name: str,
        description: str,
    ):
        self.id = id
        self.format = format
        self.name = name
        self.description = description

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "format": self.format,
            "name": self.name,
            "description": self.description,
        }

        return {k: v for k, v in data.items() if k not in exclude}
