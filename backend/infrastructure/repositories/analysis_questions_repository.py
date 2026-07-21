from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from domain.models.analysis.analysis_questions import AnalysisQuestion
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class AnalysisQuestionsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.logger=logger
        self.db = db

    def create_many(
        self,
        items: list[AnalysisQuestion]
    ) -> list[AnalysisQuestion]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for insight in items:
            self.db.refresh(insight)

        return items

    # 🔍 GET BY ID
    def find_for_analyse(
        self,
        analysis_id: int,
    ) -> list[AnalysisQuestion]:

        filters = []

        if analysis_id is not None:
            filters.append(
                AnalysisQuestion.analysis_id == analysis_id
            )


        if not filters:
            return []

        return self.db.query(AnalysisQuestion).filter(
            or_(*filters)
        ).all()

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[AnalysisQuestion]:
        return self.db.query(AnalysisQuestion).filter(AnalysisQuestion.id == id).first()

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(AnalysisQuestion).filter(AnalysisQuestion.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
