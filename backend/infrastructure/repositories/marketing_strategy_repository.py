from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.marketing_strategy.marketing_strategy import MarketingStrategy
from infrastructure.logging.logger import Logger


class MarketingStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: MarketingStrategy) -> MarketingStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[MarketingStrategy]:
        return self.db.query(MarketingStrategy).filter(MarketingStrategy.id == id).first()

    # 🔍 GET BY BRAND MARKETING ID
    def get_by_brand_marketing_id(self, brand_marketing_id: int) -> List[MarketingStrategy]:
        return (
            self.db.query(MarketingStrategy)
            .filter(MarketingStrategy.brand_marketing_id == brand_marketing_id)
            .all()
        )
