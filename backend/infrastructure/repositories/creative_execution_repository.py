from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.creative_execution.creative_execution import CreativeExecution
from infrastructure.logging.logger import Logger


class CreativeExecutionRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: CreativeExecution) -> CreativeExecution:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[CreativeExecution]:
        return self.db.query(CreativeExecution).filter(CreativeExecution.id == id).first()

    # 🔍 GET BY AD EXECUTION ID
    def get_by_ad_execution_id(self, ad_execution_id: int) -> List[CreativeExecution]:
        return (
            self.db.query(CreativeExecution)
            .filter(CreativeExecution.ad_execution_id == ad_execution_id)
            .all()
        )

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(CreativeExecution).filter(CreativeExecution.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
