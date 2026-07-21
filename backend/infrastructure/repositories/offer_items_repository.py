from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.offers.offer_item import OfferItem
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class OfferItemsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    # ➕ CREATE
    def create(self, offer : OfferItem) -> OfferItem:
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

# 🔍 GET BY OFFER ID
    def get_by_offer_id(self, offer_id: int) -> list[OfferItem]:
        return self.db.query(OfferItem).filter(OfferItem.offer_id == offer_id).all()

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[OfferItem]:
        return self.db.query(OfferItem).filter(OfferItem.id == id).first()

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        offer_item = self.db.query(OfferItem).filter(OfferItem.id == id).first()

        if not offer_item:
            return False

        self.db.delete(offer_item)
        self.db.commit()
        return True

    # def search(self, page: int = 1, page_size: int = 20) -> PaginatedResult[Offer]:
    #         page = max(1, page)
    #         page_size = max(1, page_size)

    #         total_items = self.db.query(func.count(OfferItem.id)).scalar()

    #         items = (
    #             self.db.query(OfferItem)
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