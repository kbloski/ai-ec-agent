from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.offer_strategy.offer_strategy import OfferStrategy
from infrastructure.logging.logger import Logger


class OfferStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: OfferStrategy) -> OfferStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[OfferStrategy]:
        return self.db.query(OfferStrategy).filter(OfferStrategy.id == id).first()

    # 🔍 GET BY MARKETING STRATEGY ID
    def get_by_marketing_strategy_id(self, marketing_strategy_id: int) -> List[OfferStrategy]:
        return (
            self.db.query(OfferStrategy)
            .filter(OfferStrategy.marketing_strategy_id == marketing_strategy_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(OfferStrategy).filter(OfferStrategy.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
