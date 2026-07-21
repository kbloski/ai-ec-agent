from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.brand_marketing.brand_marketing import BrandMarketing
from infrastructure.logging.logger import Logger


class BrandMarketingRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: BrandMarketing) -> BrandMarketing:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[BrandMarketing]:
        return self.db.query(BrandMarketing).filter(BrandMarketing.id == id).first()

    # 🔍 GET BY KNOWLEDGE ID
    def get_by_knowledge_id(self, knowledge_id: int) -> List[BrandMarketing]:
        return (
            self.db.query(BrandMarketing)
            .filter(BrandMarketing.knowledge_id == knowledge_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(BrandMarketing).filter(BrandMarketing.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
