from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.analysis.analysis_questions import AnalysisQuestion
from infrastructure.logging.logger import Logger

class AnalysisQuestionsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.logger=logger
        self.db = db

    # ➕ CREATE MANY
    def create_many(
        self,
        items: list[AnalysisQuestion]
    ) -> list[AnalysisQuestion]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for item in items:
            self.db.refresh(item)

        return items

    # 🔍 FIND FOR ANALYSE
    def find_for_analyse(
        self,
        analysis_id: int,
    ) -> list[AnalysisQuestion]:

        return self.db.query(AnalysisQuestion).filter(
            AnalysisQuestion.analysis_id == analysis_id
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

    # ❌ DELETE BY ANALYSIS ID
    def delete_by_analysis_id(self, analysis_id: int) -> int:
        deleted = (
            self.db.query(AnalysisQuestion)
            .filter(AnalysisQuestion.analysis_id == analysis_id)
            .delete()
        )
        self.db.commit()
        return deleted
