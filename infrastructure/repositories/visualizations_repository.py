from typing import List, Optional

from sqlalchemy.orm import Session

from domain.models.visualizations.vusualization import Visualization
from infrastructure.logging.logger import Logger


class VisualizationsRepository:
    def __init__(self, logger: Logger, db: Session):
        self.logger = logger
        self.db = db

    # ➕ CREATE
    def create(self, item: Visualization) -> Visualization:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[Visualization]:
        return self.db.query(Visualization).filter(Visualization.id == id).first()

    # 🔍 GET BY IDS
    def get_by_ids(self, ids: List[int]) -> List[Visualization]:
        return (
            self.db.query(Visualization)
            .filter(Visualization.id.in_(ids))
            .all()
        )
