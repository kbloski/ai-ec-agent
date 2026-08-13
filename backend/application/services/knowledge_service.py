import json

from infrastructure.services.path_service import PathService
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser
from infrastructure.parsers.txt_parser import TxtParser
from application.services.ai_service import AiService
from application.dtos.knowledge.knowledge_dto import KnowledgeDto
from infrastructure.repositories.knowledge_repository import KnowledgeRepository
from application.mappers.knowledge_mapper import KnowledgeMapper
from application.assemblers.knowledge_assembler import KnowledgeAssembler
from application.services.llm_context_builder import build_llm_section
from domain.enums.context_section_purpose import ContextSectionPurpose

class KnowledgeService:

    def __init__(
        self,
        logger: Logger,
        docx_parser: DocxParser,
        txt_parser: TxtParser,
        ai_service: AiService,
        path_service: PathService,
        knowledge_repository : KnowledgeRepository,
        knowledge_assembler : KnowledgeAssembler
    ):
        self.logger = logger
        self.docx_parser = docx_parser
        self.path_service = path_service
        self.txt_parser = txt_parser
        self.ai_service = ai_service
        self.knowledge_repository = knowledge_repository
        self.knowledge_assembler = knowledge_assembler



    def get_knowledge_details_by_id(self, knowledge_id : int ) -> KnowledgeDto :
        knowledge_db = self.knowledge_repository.get_by_id( id=knowledge_id)
        knowledge_dto = KnowledgeMapper.to_dto(item=knowledge_db)
        assembled_knowledge = self.knowledge_assembler.assemble_dto(item=knowledge_dto)
        return assembled_knowledge



    def build_llm_context(self, knowledge_id: int) -> str:
        assembled_knowledge = self.get_knowledge_details_by_id(knowledge_id=knowledge_id)

        knowledge_json = json.dumps(
            assembled_knowledge.to_content_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )

        return build_llm_section("knowledge", knowledge_json, purpose=ContextSectionPurpose.KNOWLEDGE.value)



    def build_knowledge_from_materials_raw(self):
        self.logger.info("Build knowledge from materials raw start")

        # 🔹 folder RAW
        raw_folder = self.path_service.RAW_ECOMMERCE_KNOWLEDGE

        # 🔹 zbieranie plików (AI-friendly)
        allowed_ext = {".docx", ".txt"}
        files = [
            f for f in raw_folder.iterdir()
            if f.is_file() and f.suffix in allowed_ext
        ]
        self.logger.info(f"Found {len(files)} raw files")

        # 🔹 parsing (DOCX na razie)
        parsed_documents = []

        for file in files:
            try:
                if file.suffix == ".docx":
                    text = self.docx_parser.parse(file)
                else:
                    text = self.txt_parser.parse(file)

                parsed_documents.append({
                    "file": str(file),
                    "content": text
                })

            except Exception as e:
                self.logger.error(f"Failed to parse file {file}: {str(e)}")


        return {
            "message": "Knowledge build completed",
            "files_count": len(files),
            "parsed_count": len(parsed_documents),
            # "documents": parsed_documents
        }
        