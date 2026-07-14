

import json
from typing import Dict, Any, List

from di.container import Container

from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.analysis.knowledge_analysis_questions import KNOWLEDGE_ANALYSIS_QUESTIONS


BASE_SYSTEM_PROMPT = """
You are an expert in e-commerce product analysis.

Your task is to analyze products in terms of their sales potential.
Think like an entrepreneur investing their own money into a product.

Rules:
1. Provide specific and factual answers.
2. Do not invent information that is not present in the data.
3. If information is missing, clearly state that fact.
4. Evaluate the product objectively.
5. Point out both advantages and risks.
"""



def chunk_list(
    items: List[str],
    size: int
) -> List[List[str]]:

    return [
        items[i:i + size]
        for i in range(0, len(items), size)
    ]


def build_product_context_prompt(
    product_data: Dict[str, Any]
) -> str:

    return f"""
PRODUCT DATA:

{json.dumps(
    product_data,
    ensure_ascii=False,
    indent=2
)}

Analyze the product based on the data provided above.
Do not draw conclusions based on information that is not present in the data.
"""


def build_questions_prompt(
    questions: List[str]
) -> str:

    return f"""
ANALYSIS QUESTIONS:

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2
)}


Answer each question based only on the provided product data.

Return ONLY valid JSON:

[
    {{
        "question": "exact question text",
        "answer": "detailed answer"
    }}
]


Rules:
- Answer every question.
- Do not skip questions.
- Do not add markdown.
- Do not add any text outside JSON.
- If information is missing, state that clearly.
"""


def knowledge_analysis_answers_generate_handler(
    knowledge_id: int,
    analyse_id: int
) -> Dict[str, Any]:

    container = Container()
    logger = container.logger()
    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()
    knowledge_analysis_repository = container.knowledge_analysis_repository()
    analysis_repository = container.analysis_repository()

    # Get analysis 
    knowledge_analysis_db = knowledge_analysis_repository.find_relation(knowledge_id=knowledge_id,analysis_id=analyse_id)
    analyse_db = analysis_repository.get_by_id(id=knowledge_analysis_db.analysis_id)

    logger.info(f"Generating knowledge analysis for knowledge_id={knowledge_id}")
    knowledge_db = knowledge_repo.get_by_id(
        id=knowledge_id
    )
    knowledge_dto = OfferKnowledgeMapper.to_dto(
        item=knowledge_db
    )
    assembled_dto = knowledge_assembler.assemble_dto(
        item=knowledge_dto
    )
    knowledge_json = assembled_dto.to_dict()


    question_batches = chunk_list(
        items=KNOWLEDGE_ANALYSIS_QUESTIONS,
        size=10
    )

    logger.info(f"Split {len(KNOWLEDGE_ANALYSIS_QUESTIONS)} questions into {len(question_batches)} batches")


    final_analysis = []


    for batch_index, batch in enumerate(question_batches, start=1):

        logger.info(f"Processing batch {batch_index}/{len(question_batches)} ({len(batch)} questions)")

        messages = [

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=BASE_SYSTEM_PROMPT
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=build_product_context_prompt(
                    knowledge_json
                )
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=build_questions_prompt(
                    questions=batch
                )
            )

        ]


        response = ollama_service.chat_llm(
            messages=messages
        )


        try:

            batch_result = json.loads(
                response.content
            )

        except json.JSONDecodeError:

            raise Exception(
                f"""
Invalid JSON response from model:

{response.content}
"""
            )


        if not isinstance(batch_result, list):

            raise Exception(
                "Model response is not a list."
            )


        logger.info(f"Batch {batch_index}/{len(question_batches)} returned {len(batch_result)} answers")

        final_analysis.extend(
            batch_result
        )


    logger.info(f"Knowledge analysis completed for knowledge_id={knowledge_id}, total_answers={len(final_analysis)}")

    # Analysis_questions


    return {
        "product_id": knowledge_id,
        "analysis": final_analysis
    }