from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from domain.models.offers.offer_insight import OfferInsight
from infrastructure.logging.logger import Logger
from common.results.paginated_result import PaginatedResult

class OfferInsightsRepository:
    def __init__(self, logger : Logger, db: Session):
        self.db = db

    def create_many(
        self,
        insights: list[OfferInsight]
    ) -> list[OfferInsight]:

        if not insights:
            return []

        self.db.add_all(insights)
        self.db.commit()

        for insight in insights:
            self.db.refresh(insight)

        return insights

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
    
    

