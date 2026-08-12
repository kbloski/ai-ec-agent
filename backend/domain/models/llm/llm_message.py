from ...enums.llm_message_role import LlmMessageRole


class LlmMessage:
    def __init__(self, role: LlmMessageRole, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {
            "role": self.role.value,
            "content": self.content
        }
