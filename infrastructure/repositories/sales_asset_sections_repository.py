from typing import List

from sqlalchemy.orm import Session

from domain.models.sales_assets.sales_asset_sections import SalesAssetSection
from infrastructure.logging.logger import Logger


class SalesAssetSectionsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE MANY
    def create_many(self, items: List[SalesAssetSection]) -> List[SalesAssetSection]:
        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 FIND FOR SALES ASSET
    def find_for_sales_asset(self, sales_asset_id: int) -> List[SalesAssetSection]:
        return (
            self.db.query(SalesAssetSection)
            .filter(SalesAssetSection.sales_asset_id == sales_asset_id)
            .all()
        )
