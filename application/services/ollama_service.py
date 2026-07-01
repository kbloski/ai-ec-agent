from ollama import Client
from infrastructure.logging.logger import Logger
from core.settings import Settings

from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole

class OllamaService:
    def __init__(self, logger: Logger, settings: Settings):
        self.logger = logger
        self.model = settings.get_ollama_model()
        self.num_ctx = settings.get_ollama_num_ctx()
        self.temperature = settings.get_ollama_temperature()

        self.client = Client(
            host=settings.get_ollama_url()
        )

    def chat(self, messages: list[OllamaMessage]) -> OllamaMessage:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[message.to_dict() for message in messages],
                options={
                    "num_ctx": self.num_ctx,
                    "temperature": self.temperature,
                },
            )

            return OllamaMessage(
                role=OllamaMessageRole.ASSISTANT,
                content=response["message"]["content"]
            )

        except Exception as e:
            self.logger.error(f"Ollama chat error: {e}")
            raise