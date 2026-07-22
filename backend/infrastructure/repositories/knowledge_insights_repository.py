from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.knowledge.knowledge_insight import KnowledgeInsight
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class KnowledgeInsightsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    # ➕ CREATE MANY
    def create_many(
        self,
        items: list[KnowledgeInsight]
    ) -> list[KnowledgeInsight]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for insight in items:
            self.db.refresh(insight)

        return items

    # 🔍 GET BY ID
    def find_by_knowledge_id(
        self,
        knowledge_id: int
    ) -> list[KnowledgeInsight]:

        return self.db.query(KnowledgeInsight).filter(
            KnowledgeInsight.knowledge_id == knowledge_id
        ).all()

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[KnowledgeInsight]:
        return self.db.query(KnowledgeInsight).filter(KnowledgeInsight.id == id).first()

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(KnowledgeInsight).filter(KnowledgeInsight.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True

    # def search(self, page: int = 1, page_size: int = 20) -> PaginatedResult[Offer]:
    #         page = max(1, page)
    #         page_size = max(1, page_size)

    #         total_items = self.db.query(func.count(Offer.id)).scalar()

    #         items = (
    #             self.db.query(Offer)
    #             .offset((page - 1) * page_size)
    #             .limit(page_size)
    #             .all()
    #         )

    #         return PaginatedResult(
    #             items=items,
    #             page=page,
    #             page_size=page_size,
    #             total_items=total_items,
    #         )
