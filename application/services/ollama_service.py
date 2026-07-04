from ollama import Client
from infrastructure.logging.logger import Logger
from core.settings import Settings

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole

class OllamaService:
    def __init__(self, logger: Logger, settings: Settings):
        self.logger = logger
        self.llm_model = settings.get_ollama_llm_model()
        self.num_ctx = settings.get_ollama_num_ctx()
        self.temperature = settings.get_ollama_temperature()
        self.client = Client(
            host=settings.get_ollama_url()
        )

    def chat_llm(self, messages: list[LlmOllamaMessage]) -> LlmOllamaMessage:
        """Obsługuje standardowe modele tekstowe (LLM)"""
        try:
            # ✅ Naprawione: Konwertujemy obiekty domenowe na słowniki akceptowane przez Ollamę
            payload_messages = [msg.to_dict() for msg in messages]

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

