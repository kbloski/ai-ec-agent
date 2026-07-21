import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self._ollama_llm_model = os.getenv("OLLAMA_LLM_MODEL")
        self._ollama_vlm_model = os.getenv("OLLAMA_VLM_MODEL")

    def get_host(self) -> str:
        return os.getenv("HOST", "0.0.0.0")
    
    def get_port(self) -> int:
        return int(os.getenv("PORT", "8000"))

    def get_ollama_llm_model(self) -> str:
        return self._ollama_llm_model
    
    def get_ollama_url(self) -> str:
        return os.getenv("OLLAMA_URL", "http://localhost:11434")
    
    def get_ollama_temperature(self) -> float:
        return float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))

    def get_ollama_num_ctx(self) -> int:
        return int(os.getenv("OLLAMA_CONTEXT_LENGTH", "131072"))