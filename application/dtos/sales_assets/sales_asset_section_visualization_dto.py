from typing import Optional

from common.mixins.json_serializable import JSONSerializable
from application.dtos.visualizations.visualization_dto import VisualizationDto


class SalesAssetSectionVisualizationDto(JSONSerializable):
    visualization: Optional[VisualizationDto] = None

    def __init__(
        self,
        sales_asset_section_id: int,
        visualization_id: int,
        position: int,
    ):
        self.sales_asset_section_id = sales_asset_section_id
        self.visualization_id = visualization_id
        self.position = position

    def to_dict(self, exclude=None):
        exclude = set(exclude or [])

        data = {
            "sales_asset_section_id": self.sales_asset_section_id,
            "visualization_id": self.visualization_id,
            "position": self.position,
            "visualization": self.visualization.to_dict() if self.visualization else None,
        }

        return {k: v for k, v in data.items() if k not in exclude}
