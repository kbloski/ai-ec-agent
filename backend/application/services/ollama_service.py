from ollama import Client
import json
from infrastructure.logging.logger import Logger
from infrastructure.services.path_service import PathService
from core.settings import Settings

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole

class OllamaService:
    def __init__(self, logger: Logger, settings: Settings, path_service: PathService):
        self.logger = logger
        self.path_service = path_service
        self.llm_model = settings.get_ollama_llm_model()
        self.num_ctx = settings.get_ollama_num_ctx()
        self.temperature = settings.get_ollama_temperature()
        self.client = Client(  host=settings.get_ollama_url() )
        self.global_system_prompt = self._load_global_system_prompt()

    def _load_global_system_prompt(self) -> str:
        try:
            return self.path_service.GLOBAL_SYSTEM_PROMPT.read_text(encoding="utf-8")
        except Exception as e:
            self.logger.error(f"Nie udało się wczytać globalnego promptu systemowego: {e}")
            return ""

    def chat_llm(self, messages: list[LlmOllamaMessage]) -> LlmOllamaMessage:
        """Obsługuje standardowe modele tekstowe (LLM)"""
        try:
            # ✅ Naprawione: Konwertujemy obiekty domenowe na słowniki akceptowane przez Ollamę
            payload_messages = [msg.to_dict() for msg in messages]

            if self.global_system_prompt:
                payload_messages.insert(0, LlmOllamaMessage(
                    role=OllamaMessageRole.SYSTEM,
                    content=self.global_system_prompt
                ).to_dict())
                
            response = self.client.chat(
                model=self.llm_model,
                messages=payload_messages,
                options={
                    "num_ctx": self.num_ctx,
                    "temperature": self.temperature,
                },
            )

            return LlmOllamaMessage(
                role=OllamaMessageRole.ASSISTANT,
                content=response["message"]["content"]
            )

        except Exception as e:
            self.logger.error(f"Ollama llm chat error: {e}")
            raise

