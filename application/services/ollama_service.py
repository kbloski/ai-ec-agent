from .memory_service import MemoryService
from infrastructure.logging.logger import Logger
import requests


class OllamaService:
    # model = "qwen2.5:7"
    model = "qwen3:14b"
    ollamaUrl = "http://localhost:11434/api/chat"

    def __init__(self, logger : Logger, memory_service: MemoryService):
        self.memory_service = memory_service
        self.logger = Logger

    def chat(self, chat_id: str, messages: list[dict]):
        response = self._call_ollama(
            self.memory_service.get(chat_id) + messages
        ) 

        if user_msg := next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            None
        ):
            self.memory_service.save(chat_id, user_msg, response)

        return response

    def _call_ollama(self, messages):
        res = requests.post(
            self.ollamaUrl,
            json={
                "model": self.model,
                "messages": messages,
                "stream": False
            }
        )

        return res.json()["message"]["content"]