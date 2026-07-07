from domain.models.offers.offer import Offer
from application.dtos.offers.offer_dto import OfferDto

class OfferMapper:

    @staticmethod
    def to_dto(item : Offer) -> OfferDto:
        return OfferDto(
            id = item.id,
            name=item.name,
            buying_price=item.buying_price,
            selling_price=item.selling_price,
            details=item.details,  # lub offer.details jeśli zmienisz model
            target_audience=item.target_audience,
            pain_points=item.pain_points,
            offer_items=[] 
        )

