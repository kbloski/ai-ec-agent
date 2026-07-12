import json
from typing import Dict, Any

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage

from domain.enums.ollama_message_role import OllamaMessageRole
from domain.enums.content_status import ContentStatus

from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt

BASE_SYSTEM_PROMPT = """"""



def generate_knowledge_analysis_handler(
    knowledge_id: int
) -> Dict[str, Any]:
    container = Container()

    target_audience_repo = container.target_audiences_repository()
    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()

    knowledge_db =  knowledge_repo.get_by_id( id=knowledge_id )
    knowledge_dto = OfferKnowledgeMapper.to_dto( item=knowledge_db )
    assembled_dto =  knowledge_assembler.assemble_dto( item=knowledge_dto )
    knowledge_json = assembled_dto.to_dict()

    return knowledge_json



    response = ollama_service.chat_llm(
        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=BASE_SYSTEM_PROMPT
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=build_uniqueness_constraint_prompt(
                    existing_data= json.dumps( [t.to_dict() for t in target_audiences_db_dtos])
                )
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=user_prompt
            )
        ]
    )


    response_json = json.loads(response.content )

    return new_target_audiences