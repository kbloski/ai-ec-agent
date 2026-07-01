from infrastructure.logging.logger import Logger
from infrastructure.repositories.products_repository import ProductRepository
from infrastructure.services.path_service import PathService
from .ollama_service import OllamaService
import json
from domain.models.ollama.ollama_message import OllamaMessage
from domain.enums.ollama.ollama_message_role import OllamaMessageRole


class ProductService:
    def __init__(
        self,
        logger: Logger,
        path_service: PathService,
        product_repository: ProductRepository,
        ollama_service: OllamaService,
    ):
        self.logger = logger
        self.path_service = path_service
        self.product_repo = product_repository
        self.ollama_service = ollama_service

        self.ai_workflows_path = self.path_service.BASE_DIR / "infrastructure/ai/workflows"

    def analyze_product(self, product_id: int):
        self.logger.info("Analyzing product data...")

        product = self.product_repo.get_by_id(product_id)
        if not product:
            self.logger.error(f"Product with ID {product_id} not found.")
            return {"error": f"Product with ID {product_id} not found."}

        # --- load workflow ---
        workflow_file_path = self.ai_workflows_path / "product_analyze.json"

        with open(workflow_file_path, "r", encoding="utf-8") as file:
            workflow_data = json.load(file)

        workflow_config = workflow_data.get("config", {})
        workflow_steps = workflow_data.get("steps", [])

        # --- SAFE lookup step ---
        steps_map = {step.get("id"): step for step in workflow_steps}
        input_step = steps_map.get("input_validation", {})

        input_prompt = input_step.get("prompt", "")

        # --- build chat ---
        chat = [
            OllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=workflow_config.get("system_prompt", "")
            ),
            OllamaMessage(
                role=OllamaMessageRole.USER,
                content="product_data: " + json.dumps(product.to_dict(), default=str)
            ),
            OllamaMessage(
                role=OllamaMessageRole.USER,
                content=input_prompt
            )
        ]

        # --- call model ---
        message = self.ollama_service.chat(messages=chat)

        chat.append(message)

        return {
            "product": product,
            "chat": chat,
        }