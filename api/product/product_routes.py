from fastapi import APIRouter

from di.container import Container
from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole
import json

def register_product_routes(router: APIRouter):

    @router.get("/product/analyze")
    def product_analyze():
        container = Container()
        ollama_service = container.ollama_service()
        path_service = container.path_service()

        data = []

        workflowPath = path_service.BASE_DIR / "infrastructure/ai/workflows/offer_generation.json"
        with open(workflowPath, "r", encoding="utf-8") as f:
            workflow_json = json.load(f)
        
        data.append("Workflow JSON loaded successfully.")

        system_prompt = workflow_json["config"]["system_prompt"]
        messages = [
            OllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=system_prompt
            ),
            OllamaMessage(
                role=OllamaMessageRole.USER,
                content="Powiedz cześć do mnie i to kim jestes."
            ),
        ]

        messages.append(ollama_service.chat(messages))

        # messages.append(assistant_message)
        # messages.append(OllamaMessage(
        #     role=OllamaMessageRole.USER,
        #     content="Czy lubisz mnie?"
        # ))

        # response = ollama_service.chat(messages)

        # messages.append(response)

        return {
            "name" : "product-analyze",
            "status": "ok",
            "data" : data,
            "result": {
                "messages" : messages
            }
        }