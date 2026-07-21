from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from domain.models.offers.offer_insight import OfferInsight
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class OfferInsightsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.logger=logger
        self.db = db

    def create_many(
        self,
        items: list[OfferInsight]
    ) -> list[OfferInsight]:

        if not items:
            return []

        self.db.add_all(items)
        self.db.commit()

        for insight in items:
            self.db.refresh(insight)

        return items

    # 🔍 GET BY ID
    def find_by_offer(
        self,
        offer_id: Optional[int] = None,
    ) -> list[OfferInsight]:

        filters = []

        if offer_id is not None:
            filters.append(
                OfferInsight.offer_id == offer_id
            )


        if not filters:
            return []

        return self.db.query(OfferInsight).filter(
            or_(*filters)
        ).all()

    # 🔍 GET BY ID
    def get_by_id(self, id: int) -> Optional[OfferInsight]:
        return self.db.query(OfferInsight).filter(OfferInsight.id == id).first()

    # ❌ DELETE
    def delete(self, id: int) -> bool:
        item = self.db.query(OfferInsight).filter(OfferInsight.id == id).first()

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True
