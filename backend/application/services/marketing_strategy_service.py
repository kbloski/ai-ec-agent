import json

from typing import List

from infrastructure.logging.logger import Logger
from domain.models.marketing_strategy.marketing_strategy import MarketingStrategy
from application.dtos.marketing_strategy.marketing_strategy_response_dto import MarketingStrategyDto
from infrastructure.repositories.marketing_strategy_repository import MarketingStrategyRepository
from application.mappers.marketing_strategy_mapper import MarketingStrategyMapper
from application.assemblers.marketing_strategy_assembler import MarketingStrategyAssembler
from application.services.llm_context_builder import build_llm_section
from domain.enums.context_section_purpose import ContextSectionPurpose


class MarketingStrategyService:

    def __init__(
        self,
        logger: Logger,
        marketing_strategy_repository: MarketingStrategyRepository,
        marketing_strategy_assembler: MarketingStrategyAssembler,
    ):
        self.logger = logger
        self.marketing_strategy_repository = marketing_strategy_repository
        self.marketing_strategy_assembler = marketing_strategy_assembler

    def create_marketing_strategy(self, marketing_strategy: MarketingStrategy) -> MarketingStrategyDto:
        created = self.marketing_strategy_repository.create(marketing_strategy)
        return self.get_marketing_strategy_by_id(id=created.id)

    def get_marketing_strategy_by_id(self, id: int) -> MarketingStrategyDto:
        marketing_strategy_db = self.marketing_strategy_repository.get_by_id(id)

        if not marketing_strategy_db:
            raise ValueError(f"Marketing strategy {id} not found")

        marketing_strategy_dto = MarketingStrategyMapper.to_dto(marketing_strategy_db)
        return self.marketing_strategy_assembler.assemble_dto(marketing_strategy_dto)

    def get_marketing_strategies_by_brand_marketing(self, brand_marketing_id: int) -> List[MarketingStrategyDto]:
        items = self.marketing_strategy_repository.get_by_brand_marketing_id(brand_marketing_id)
        dtos = [MarketingStrategyMapper.to_dto(item) for item in items]
        return [self.marketing_strategy_assembler.assemble_dto(dto) for dto in dtos]

    def build_llm_context(self, marketing_strategy_id: int) -> str:
        marketing_strategy_json = json.dumps(
            self.get_marketing_strategy_by_id(id=marketing_strategy_id).to_content_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )

        return build_llm_section("marketing-strategy", marketing_strategy_json, purpose=ContextSectionPurpose.MARKETING_STRATEGY.value)
