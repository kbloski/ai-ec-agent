from pathlib import Path
from infrastructure.logging.logger import Logger

class TxtParser:
    def __init__(self, logger : Logger ):
        self.logger = logger

    def parse(self, file_path: Path) -> str:
        try:
            text = self._read_file(file_path)
            cleaned = self._clean_text(text)

            if self.logger:
                self.logger.info(f"Parsed TXT file: {file_path}")

            return cleaned

        except Exception as e:
            if self.logger:
                self.logger.error(f"TXT parse error {file_path}: {str(e)}")
            raise

    def _read_file(self, file_path: Path) -> str:
        # 🔹 safe reading (AI-grade robustness)
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="latin-1")

    def _clean_text(self, text: str) -> str:
        # 🔹 basic cleanup for AI ingestion
        lines = text.splitlines()

        cleaned_lines = [
            line.strip()
            for line in lines
            if line.strip()  # remove empty lines
        ]

        return "\n".join(cleaned_lines)