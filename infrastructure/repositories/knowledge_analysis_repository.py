from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from domain.models.analysis.knowledge_analysis import KnowledgeAnalysis
from infrastructure.logging.logger import Logger


class KnowledgeAnalysisRepository:
    def __init__(self, logger: Logger, db: Session):
        self.db = db
        self.logger = logger

    # ➕ UPSERT
    def upsert(self, analysis: KnowledgeAnalysis) -> KnowledgeAnalysis:
        existing = (
            self.db.query(KnowledgeAnalysis)
            .filter(
                and_(
                    KnowledgeAnalysis.knowledge_id == analysis.knowledge_id,
                    KnowledgeAnalysis.analysis_id == analysis.analysis_id
                )
            )
            .first()
        )

        if existing:
            existing.content = analysis.content
            existing.updated_at = analysis.updated_at

            self.db.commit()
            self.db.refresh(existing)
            return existing

        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    # 🔍 GET BY KNOWLEDGE ID
    def find_by_knowledge_id(self, knowledge_id: int) -> List[KnowledgeAnalysis]:
        return (
            self.db.query(KnowledgeAnalysis)
            .filter(KnowledgeAnalysis.knowledge_id == knowledge_id)
            .all()
        )