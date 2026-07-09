from ...enums.ollama_message_role import OllamaMessageRole


class LlmOllamaMessage:
    def __init__(self, role: OllamaMessageRole, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role.value,
            "content": self.content
        }