from fastapi import APIRouter

from di.container import Container
from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole

def register_test_routes(router: APIRouter):

    @router.get("/test")
    def test():
        container = Container()

        ollama_service = container.ollama_service()

        messages = [
            OllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=(
                    "Jesteś pomocnym asystentem AI, "
                    "który pomaga użytkownikom w różnych zadaniach."
                )
            ),
            OllamaMessage(
                role=OllamaMessageRole.USER,
                content="Powiedz cześć do mnie."
            ),
        ]

        assistant_message = ollama_service.chat(messages)

        messages.append(assistant_message)
        messages.append(OllamaMessage(
            role=OllamaMessageRole.USER,
            content="Czy lubisz mnie?"
        ))

        response = ollama_service.chat(messages)

        messages.append(response)

        return {
            "status": "ok",
            "result": {
                "response": response,
                "messages" : messages
            }
        }