from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.offers.offer_knowledge import OfferKnowledge
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class OfferKnowledgeRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[OfferKnowledge]:
        return self.db.query(OfferKnowledge).filter(OfferKnowledge.id == id).first()

    # 🔍 GET BY ID
    def get_by_offer_id(self, offer_id: int) -> Optional[OfferKnowledge]:
        return self.db.query(OfferKnowledge).filter(OfferKnowledge.offer_id == offer_id).all()

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
