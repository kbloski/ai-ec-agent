from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.ad_execution.ad_execution import AdExecution
from infrastructure.logging.logger import Logger


class AdExecutionRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: AdExecution) -> AdExecution:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[AdExecution]:
        return self.db.query(AdExecution).filter(AdExecution.id == id).first()

    # 🔍 GET BY CREATIVE STRATEGY ID
    def get_by_creative_strategy_id(self, creative_strategy_id: int) -> List[AdExecution]:
        return (
            self.db.query(AdExecution)
            .filter(AdExecution.creative_strategy_id == creative_strategy_id)
            .all()
        )

    def update(self, item: AdExecution) -> AdExecution:
        existing_item = self.db.query(AdExecution).filter(AdExecution.id == item.id).first()

        if not existing_item:
            raise ValueError(f"AdExecution with id {item.id} not found")

        for key, value in item.__dict__.items():
            if key != "_sa_instance_state":
                setattr(existing_item, key, value)

        self.db.commit()
        self.db.refresh(existing_item)

        return existing_item

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(AdExecution).filter(AdExecution.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
