import json
from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


def knowledge_advertisement_generate_handler(knowledge_id : int ):
    container = Container()
    
    knowledge_service = container.knowledge_service()
    ollama_service = container.ollama_service()
    
    knowledge_details = knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id)
    knowledge_details_json = json.loads( knowledge_details.to_dict() )
    
    return "knowledge_details.to_dict()"