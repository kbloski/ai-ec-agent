from application.mappers.offer_item_mapper import OfferItemMapper
from di.container import Container
from domain.models.offers.offer_item import OfferItem


def create_offer_item_handler(
    offer_id: int,
    name: str,
    quantity: int = 1,
    details: str | None = None,
):
    container = Container()
    offers_repository = container.offers_repository()
    offer_items_repository = container.offer_items_repository()

    if offers_repository.get_by_id(offer_id) is None:
        raise ValueError(f"Offer {offer_id} not found")

    item = OfferItem(
        offer_id=offer_id,
        name=name,
        quantity=quantity,
        details=details,
    )
    created = offer_items_repository.create(item)
    return OfferItemMapper.to_dto(created).to_dict()
