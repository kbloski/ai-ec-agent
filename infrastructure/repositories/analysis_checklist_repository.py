from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from domain.models.analysis.analysis_checklist import AnalysisChecklist
from infrastructure.logging.logger import Logger


class AnalysisChecklistRepository:
    def __init__(self, logger: Logger, db: Session):
        self.db = db
        self.logger = logger

    # ➕ UPSERT
    def upsert(self, analysis_checklist: AnalysisChecklist) -> AnalysisChecklist:
        existing = (
            self.db.query(AnalysisChecklist)
            .filter(
                and_(
                    AnalysisChecklist.analysis_id == analysis_checklist.analysis_id,
                    AnalysisChecklist.checklist_id == analysis_checklist.checklist_id,
                )
            )
            .first()
        )

        if existing:
            return existing

        self.db.add(analysis_checklist)
        self.db.commit()
        self.db.refresh(analysis_checklist)
        return analysis_checklist

    # 🔍 GET BY ANALYSIS ID
    def find_by_analysis_id(self, analysis_id: int) -> List[AnalysisChecklist]:
        return (
            self.db.query(AnalysisChecklist)
            .filter(AnalysisChecklist.analysis_id == analysis_id)
            .all()
        )

    # 🔍 GET BY CHECKLIST ID
    def find_by_checklist_id(self, checklist_id: int) -> List[AnalysisChecklist]:
        return (
            self.db.query(AnalysisChecklist)
            .filter(AnalysisChecklist.checklist_id == checklist_id)
            .all()
        )

    # 🔍 FIND RELATION
    def find_relation(
        self,
        analysis_id: int,
        checklist_id: int,
    ) -> Optional[AnalysisChecklist]:
        return (
            self.db.query(AnalysisChecklist)
            .filter(
                and_(
                    AnalysisChecklist.analysis_id == analysis_id,
                    AnalysisChecklist.checklist_id == checklist_id,
                )
            )
            .first()
        )