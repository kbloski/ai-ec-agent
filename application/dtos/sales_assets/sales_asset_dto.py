from typing import List, Optional

from common.mixins.json_serializable import JSONSerializable
from application.dtos.sales_assets.sales_asset_section_dto import SalesAssetSectionDto


class SalesAssetDto(JSONSerializable):
    sections: List[SalesAssetSectionDto] = []

    def __init__(
        self,
        id: int,
        knowledge_id: int,
        type: str,
        name: str,
        main_angle: Optional[str],
        content_status: str,
        version: int,
    ):
        self.id = id
        self.knowledge_id = knowledge_id
        self.type = type
        self.name = name
        self.main_angle = main_angle
        self.content_status = content_status
        self.version = version

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "knowledge_id": self.knowledge_id,
            "type": self.type,
            "name": self.name,
            "main_angle": self.main_angle,
            "content_status": self.content_status,
            "version": self.version,
            "sections": [item.to_dict() for item in self.sections],
        }

        return {k: v for k, v in data.items() if k not in exclude}
