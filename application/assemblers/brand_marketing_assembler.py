from infrastructure.logging.logger import Logger
from application.dtos.brand_marketing.brand_marketing_response_dto import BrandMarketingDto


class BrandMarketingAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: BrandMarketingDto) -> BrandMarketingDto:
        return item
