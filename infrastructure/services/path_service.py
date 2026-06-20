from pathlib import Path
from infrastructure.logging.logger import Logger

class PathService:
    def __init__(self, 
            logger: Logger
        ):

        self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"

        self.RAW_ECOMMERCE_KNOWLEDGE = self.DATA_DIR / "raw" / "ecommerce_knowledge"
        self.ECOMMERCE_KNOWLEDGE = self.DATA_DIR / "knowledge" / "ecommerce"
