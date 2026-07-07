from infrastructure.repositories.offers_repository import OffersRepository
from infrastructure.repositories.offer_items_repository import OfferItemsRepository
from application.dtos.offers.offer_dto import OfferDto
from application.mappers.offer_item_mapper import OfferItemMapper
from infrastructure.logging.logger import Logger

class OfferAssembler:
    def __init__(
        self,
        logger : Logger,
        offers_repository : OffersRepository,
        offer_items_repository : OfferItemsRepository 
    ):
        self.offers_repository = offers_repository
        self.offer_items_repository = offer_items_repository

    def assemble_dto(self, item : OfferDto) -> OfferDto:
        offer_items = self.offer_items_repository.get_by_offer_id(item.id)

        item.offer_items = [
            OfferItemMapper.to_dto(i)
            for i in offer_items
        ]
        
        return item
    

