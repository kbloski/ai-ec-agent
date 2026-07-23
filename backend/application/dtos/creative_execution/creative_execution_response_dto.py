from common.mixins.json_serializable import JSONSerializable


class CreativeExecutionDto(JSONSerializable):

    def __init__(
        self,
        id: int,
        ad_execution_id: int,
        content_json: dict,
    ):
        self.id = id
        self.ad_execution_id = ad_execution_id
        self.content_json = content_json

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "ad_execution_id": self.ad_execution_id,
            "content_json": self.content_json,
        }

        return {k: v for k, v in data.items() if k not in exclude}
