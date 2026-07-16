from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.sales_assets.sales_assets import SalesAsset
from infrastructure.logging.logger import Logger


class SalesAssetsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: SalesAsset) -> SalesAsset:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[SalesAsset]:
        return self.db.query(SalesAsset).filter(SalesAsset.id == id).first()

    # 🔍 GET BY KNOWLEDGE ID
    def get_by_knowledge_id(self, knowledge_id: int) -> List[SalesAsset]:
        return (
            self.db.query(SalesAsset)
            .filter(SalesAsset.knowledge_id == knowledge_id)
            .all()
        )
