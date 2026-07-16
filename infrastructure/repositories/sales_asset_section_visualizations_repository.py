from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from domain.models.sales_assets.sales_asset_section_visualization import (
    SalesAssetSectionVisualization,
)
from infrastructure.logging.logger import Logger


class SalesAssetSectionVisualizationsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ UPSERT
    def upsert(self, item: SalesAssetSectionVisualization) -> SalesAssetSectionVisualization:
        existing = (
            self.db.query(SalesAssetSectionVisualization)
            .filter(
                and_(
                    SalesAssetSectionVisualization.sales_asset_section_id
                    == item.sales_asset_section_id,
                    SalesAssetSectionVisualization.visualization_id == item.visualization_id,
                )
            )
            .first()
        )

        if existing:
            return existing

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 FIND BY SECTION ID
    def find_by_section_id(
        self, sales_asset_section_id: int
    ) -> List[SalesAssetSectionVisualization]:
        return (
            self.db.query(SalesAssetSectionVisualization)
            .filter(
                SalesAssetSectionVisualization.sales_asset_section_id
                == sales_asset_section_id
            )
            .all()
        )

    # 🔍 FIND RELATION
    def find_relation(
        self, sales_asset_section_id: int, visualization_id: int
    ) -> Optional[SalesAssetSectionVisualization]:
        return (
            self.db.query(SalesAssetSectionVisualization)
            .filter(
                and_(
                    SalesAssetSectionVisualization.sales_asset_section_id
                    == sales_asset_section_id,
                    SalesAssetSectionVisualization.visualization_id == visualization_id,
                )
            )
            .first()
        )
