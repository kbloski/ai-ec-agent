from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.ad_strategy.ad_strategy import AdStrategy
from infrastructure.logging.logger import Logger


class AdStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: AdStrategy) -> AdStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[AdStrategy]:
        return self.db.query(AdStrategy).filter(AdStrategy.id == id).first()

    # 🔍 GET BY MESSAGE STRATEGY ID
    def get_by_message_strategy_id(self, message_strategy_id: int) -> List[AdStrategy]:
        return (
            self.db.query(AdStrategy)
            .filter(AdStrategy.message_strategy_id == message_strategy_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(AdStrategy).filter(AdStrategy.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
