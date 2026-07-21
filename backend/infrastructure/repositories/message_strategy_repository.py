from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.message_strategy.message_strategy import MessageStrategy
from infrastructure.logging.logger import Logger


class MessageStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: MessageStrategy) -> MessageStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[MessageStrategy]:
        return self.db.query(MessageStrategy).filter(MessageStrategy.id == id).first()

    # 🔍 GET BY OFFER STRATEGY ID
    def get_by_offer_strategy_id(self, offer_strategy_id: int) -> List[MessageStrategy]:
        return (
            self.db.query(MessageStrategy)
            .filter(MessageStrategy.offer_strategy_id == offer_strategy_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(MessageStrategy).filter(MessageStrategy.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
