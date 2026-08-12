import json

from infrastructure.logging.logger import Logger
from infrastructure.repositories.offers_repository import OffersRepository
from application.mappers.offer_mapper import OfferMapper
from application.assemblers.offer_assembler import OfferAssembler


class OfferService:

    def __init__(
        self,
        logger: Logger,
        offers_repository: OffersRepository,
        offer_assembler: OfferAssembler,
    ):
        self.logger = logger
        self.offers_repository = offers_repository
        self.offer_assembler = offer_assembler

    def build_llm_context(self, offer_id: int) -> str:
        offer = self.offers_repository.get_by_id(offer_id)
        offer_dto = OfferMapper.to_dto(item=offer)
        offer_assembled = self.offer_assembler.assemble_dto(item=offer_dto)
        
        offer_assembled_dict = offer_assembled.to_dict()

        return json.dumps(offer_assembled.to_dict())
