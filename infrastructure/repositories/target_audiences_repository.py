from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from domain.models.audience.target_audience import TargetAudience
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class TargetAudiencesRepository:
    def __init__(self, logger : Logger, db: Session):
        self.logger=logger
        self.db = db

    def create_many(
        self,
        items: list[TargetAudience]
    ) -> list[TargetAudience]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for insight in items:
            self.db.refresh(insight)

        return items

    # 🔍 GET BY ID
    def find_by_id(
        self,
        id: int ,
    ) -> TargetAudience:

        return self.db.query(TargetAudience).filter(
            TargetAudience.id == id
        ).first()



    # 🔍 GET BY ID
    def find_for_knowledge(
        self,
        knowledge_id: int = None,
    ) -> list[TargetAudience]:

        if knowledge_id is None:
            return []

        return self.db.query(TargetAudience).filter(
            TargetAudience.knowledge_id == knowledge_id
        ).all()

