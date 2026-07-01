import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self._ollama_model = os.getenv("OLLAMA_MODEL", "llama3")

    def get_ollama_model(self) -> str:
        return self._ollama_model
