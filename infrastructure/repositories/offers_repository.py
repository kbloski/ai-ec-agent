from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from domain.models.offers.offer import Offer
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class OffersRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    # ➕ CREATE
    def create(self, offer : Offer) -> Offer:
        self.db.add(offer)
        self.db.commit()
        self.db.refresh(offer)
        return offer

    # 🔍 GET BY ID
    def get_by_id(self, offer_id: int) -> Optional[Offer]:
        return self.db.query(Offer).filter(Offer.id == offer_id).first()

    def search(self, page: int = 1, page_size: int = 20) -> PaginatedResult[Offer]:
            page = max(1, page)
            page_size = max(1, page_size)

            total_items = self.db.query(func.count(Offer.id)).scalar()

            items = (
                self.db.query(Offer)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )

            return PaginatedResult(
                items=items,
                page=page,
                page_size=page_size,
                total_items=total_items,
            )

    # # ✏️ UPDATE
    # def update(self, offer_id: int, name: str = None, price: float = None) -> Optional[offer]:
    #     offer = self.get_by_id(offer_id)
    #     if not offer:
    #         return None

    #     if name is not None:
    #         offer.name = name
    #     if price is not None:
    #         offer.price = price

    #     self.db.commit()
    #     self.db.refresh(offer)
    #     return offer

    # # ❌ DELETE
    # def delete(self, offer_id: int) -> bool:
    #     offer = self.get_by_id(offer_id)
    #     if not offer:
    #         return False

    #     self.db.delete(offer)
    #     self.db.commit()
    #     return True

    def delete_all(self) -> int:
        deleted = self.db.query(Offer).delete()
        self.db.commit()
        return deleted