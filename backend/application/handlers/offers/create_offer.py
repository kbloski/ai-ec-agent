from di.container import Container
from domain.models.offers.offer import Offer
from application.mappers.offer_mapper import OfferMapper


def create_offer(
    name: str,
    buying_price: float,
    selling_price: float | None = None,
    details: str | None = None,
):
    container = Container()
    offers_repository = container.offers_repository()

    offer = Offer(
        name=name,
        buying_price=buying_price,
        selling_price=selling_price,
        details=details,
    )

    created_offer = offers_repository.create(offer)

    return OfferMapper.to_dto(item=created_offer)
