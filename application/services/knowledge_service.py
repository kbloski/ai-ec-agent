from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser

class KnowledgeService:

    def __init__(
            self, 
            logger : Logger,
            docx_parser : DocxParser
            # parser, 
            # llm, 
            # storage
        ):
        self.logger = logger
        self.docx_parser = docx_parser


    def build_knowledge_from_materials_raw( self ):
        self.logger.info("Bild knowledge from materials raw start")

        return {
            "Dzialania sa wykonywane "
        }