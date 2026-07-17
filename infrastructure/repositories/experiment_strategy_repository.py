from typing import Optional

from sqlalchemy.orm import Session

from domain.models.experiment_strategy.experiment_strategy import ExperimentStrategy
from infrastructure.logging.logger import Logger


class ExperimentStrategyRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: ExperimentStrategy) -> ExperimentStrategy:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[ExperimentStrategy]:
        return self.db.query(ExperimentStrategy).filter(ExperimentStrategy.id == id).first()
