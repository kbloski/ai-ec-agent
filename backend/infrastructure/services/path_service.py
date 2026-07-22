from pathlib import Path
from infrastructure.logging.logger import Logger

class PathService:
    def __init__(self, 
            logger: Logger
        ):

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent

        self.UPLOADS_DEV = self.BASE_DIR / "uploads" / "dev"
        self.UPLOADS_PROD = self.BASE_DIR / "uploads" / "prod"

        self.PROMPTS_DIR = self.BASE_DIR / "infrastructure" / "ai" / "prompts"
        self.GLOBAL_SYSTEM_PROMPT = self.PROMPTS_DIR / "global.system.md"
        
        # self.DATA_DIR = self.BASE_DIR / "data"
        # self.RAW_ECOMMERCE_KNOWLEDGE = self.DATA_DIR / "raw" / "ecommerce_knowledge"
        # self.ECOMMERCE_KNOWLEDGE = self.DATA_DIR / "knowledge" / "ecommerce"

