from .memory_service import MemoryService
import requests


class OllamaService:
    model = "qwen2.5:7"
    ollamaUrl = "http://localhost:11434/api/chat"

    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service

    def chat(self, chat_id: str, messages: list[dict]):
        # 1. pobierz historię z memory
        history = self.memory_service.get(chat_id)

        # 2. zbuduj pełny kontekst
        full_messages = [
            {
                "role": "system",
                "content": "Jesteś asystentem AI dla ecommerce i sprzedaży."
            },
            *history,
            *messages
        ]

        # 3. call do Ollama
        response = self._call_ollama(full_messages)

        # 4. zapis do memory
        last_user_msg = next(
            (m for m in reversed(messages) if m["role"] == "user"),
            None
        )

        if last_user_msg:
            self.memory_service.save(
                chat_id,
                last_user_msg["content"],
                response
            )

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