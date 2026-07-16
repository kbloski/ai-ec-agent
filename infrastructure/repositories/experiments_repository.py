from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.experiment.experiment import Experiment
from infrastructure.logging.logger import Logger


class ExperimentsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: Experiment) -> Experiment:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[Experiment]:
        return self.db.query(Experiment).filter(Experiment.id == id).first()

    # 🔍 GET BY KNOWLEDGE ID
    def get_by_knowledge_id(self, knowledge_id: int) -> List[Experiment]:
        return (
            self.db.query(Experiment)
            .filter(Experiment.knowledge_id == knowledge_id)
            .all()
        )

    # ✏️ UPDATE
    def update(self, experiment: Experiment) -> Experiment:
        self.db.commit()
        self.db.refresh(experiment)
        return experiment

    # 🗑️ DELETE
    def delete(self, id: int) -> bool:
        item = self.get_by_id(id)
        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
