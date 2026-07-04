from application.dtos.offers.offer_item_dto import OfferItemDto
from domain.models.offers.offer_item import OfferItem

class OfferItemMapper:

    @staticmethod
    def to_dto(item : OfferItem) -> OfferItemDto:
        return OfferItemDto(
            id = item.id,
            offer_id = item.offer_id,
            name = item.name,
            quantity = item.quantity,
            details = item.details,
        )

