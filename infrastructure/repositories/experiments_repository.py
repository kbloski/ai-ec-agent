from typing import List

from sqlalchemy.orm import Session

from domain.models.experiments.experiment import Experiment
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

    # 🔍 GET BY EXPERIMENT STRATEGY ID
    def get_by_experiment_strategy_id(self, experiment_strategy_id: int) -> List[Experiment]:
        return (
            self.db.query(Experiment)
            .filter(Experiment.experiment_strategy_id == experiment_strategy_id)
            .all()
        )
