from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.page_strategy.page_strategy import PageStrategy
from infrastructure.logging.logger import Logger


class PageStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: PageStrategy) -> PageStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[PageStrategy]:
        return self.db.query(PageStrategy).filter(PageStrategy.id == id).first()

    # 🔍 GET BY OFFER STRATEGY ID
    def get_by_offer_strategy_id(self, offer_strategy_id: int) -> List[PageStrategy]:
        return (
            self.db.query(PageStrategy)
            .filter(PageStrategy.offer_strategy_id == offer_strategy_id)
            .all()
        )
