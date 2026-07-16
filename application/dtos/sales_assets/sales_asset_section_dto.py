from typing import List, Optional

from common.mixins.json_serializable import JSONSerializable
from application.dtos.sales_assets.sales_asset_section_visualization_dto import (
    SalesAssetSectionVisualizationDto,
)


class SalesAssetSectionDto(JSONSerializable):
    visualizations: List[SalesAssetSectionVisualizationDto] = []

    def __init__(
        self,
        id: int,
        sales_asset_id: int,
        type: str,
        position: int,
        name: str,
        goal: Optional[str],
        headline: Optional[str],
        subheadline: Optional[str],
        content: Optional[str],
    ):
        self.id = id
        self.sales_asset_id = sales_asset_id
        self.type = type
        self.position = position
        self.name = name
        self.goal = goal
        self.headline = headline
        self.subheadline = subheadline
        self.content = content

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "id": self.id,
            "sales_asset_id": self.sales_asset_id,
            "type": self.type,
            "position": self.position,
            "name": self.name,
            "goal": self.goal,
            "headline": self.headline,
            "subheadline": self.subheadline,
            "content": self.content,
            "visualizations": [item.to_dict() for item in self.visualizations],
        }

        return {k: v for k, v in data.items() if k not in exclude}
