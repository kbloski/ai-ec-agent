from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.creative_strategy.creative_strategy import CreativeStrategy
from infrastructure.logging.logger import Logger


class CreativeStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: CreativeStrategy) -> CreativeStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[CreativeStrategy]:
        return self.db.query(CreativeStrategy).filter(CreativeStrategy.id == id).first()

    # 🔍 GET BY AD STRATEGY ID
    def get_by_ad_strategy_id(self, ad_strategy_id: int) -> List[CreativeStrategy]:
        return (
            self.db.query(CreativeStrategy)
            .filter(CreativeStrategy.ad_strategy_id == ad_strategy_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(CreativeStrategy).filter(CreativeStrategy.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
