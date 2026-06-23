from infrastructure.logging.logger import Logger

class MemoryService:
    def __init__(self, logger : Logger ):
        # per-instance storage (ważne!)
        self.logger = logger
        self.history = {}

    def get(self, chat_id: str):
        return self.history.get(chat_id, [])

    def save(self, chat_id: str, user_msg: str, assistant_msg: str):
        if chat_id not in self.history:
            self.history[chat_id] = []

        self.history[chat_id].append({
            "role": "user",
            "content": user_msg
        })

        self.history[chat_id].append({
            "role": "assistant",
            "content": assistant_msg
        })