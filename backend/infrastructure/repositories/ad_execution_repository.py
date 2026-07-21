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
