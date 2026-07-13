from infrastructure.services.path_service import PathService
from infrastructure.logging.logger import Logger
from infrastructure.parsers.docx_parser import DocxParser
from infrastructure.parsers.txt_parser import TxtParser
from application.services.ollama_service import OllamaService

class KnowledgeService:

    def __init__(
        self,
        logger: Logger,
        docx_parser: DocxParser,
        txt_parser: TxtParser,
        ollama_service: OllamaService,
        path_service: PathService,
    ):
        self.logger = logger
        self.docx_parser = docx_parser
        self.path_service = path_service
        self.txt_parser = txt_parser
        self.ollama_service = ollama_service

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