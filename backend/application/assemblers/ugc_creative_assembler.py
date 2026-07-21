from infrastructure.logging.logger import Logger
from application.dtos.ugc_creatives.ugc_creative_response_dto import UgcCreativeDto


class UgcCreativeAssembler:
    def __init__(self, logger: Logger):
        self.logger = logger

    def assemble_dto(self, item: UgcCreativeDto) -> UgcCreativeDto:
        return item
