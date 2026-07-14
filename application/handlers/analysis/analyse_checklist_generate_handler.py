import json

from di.container import Container
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper
from domain.models.checklist.checklist_item import ChecklistItem
from application.mappers.checklist_item_mapper import ChecklistItemMapper


SYSTEM_PROMPT = """
You are an expert in e-commerce product research and dropshipping validation.

Your task is to create detailed TODO checklists that help verify the market potential of a product before starting sales.

You do not directly judge or rate the product. Instead, you create research instructions that a user can execute step by step.

Every generated task must:
- be a specific action to perform,
- contain detailed instructions on how to complete the analysis,
- specify where the research should be performed,
- include example search phrases/queries,
- describe what data should be collected,
- explain how to interpret the results.

You work using these research methods:
- Google Trends research,
- Meta Ads Library research,
- TikTok Creative Center research,
- marketplace research (Amazon, AliExpress, Temu, eBay),
- customer review analysis,
- social media research.

Do not create generic advice.

Do not write:
"check competitors"

Instead, provide exact instructions:
- where to go,
- what to search for,
- what to analyze,
- what data to collect,
- what indicates a positive or negative signal.

The response MUST be ONLY a valid JSON array.

Each element must have exactly this structure:

[
  {
    "title": "task name",
    "description": "detailed task execution instructions",
    "note": "additional information or empty string"
  }
]

Do not add any text outside the JSON.
Values must be in polish.
"""


def prepare_user_prompt(json_offer_data: str) -> str:
    return f"""
Based on the product data, prepare a product research checklist.

Product data:

{json_offer_data}


Generate a list of tasks that the user should perform to validate the potential of this product.


Include:


1. Google Trends:

Create tasks related to:
- analyzing the main product keywords,
- analyzing the customer's problem,
- analyzing alternative product names,
- analyzing seasonality,
- analyzing related searches.

For each task:
- generate specific phrases to search,
- explain where to go,
- explain what to check,
- explain how to interpret the results.


2. Meta Ads Library:

Create tasks related to:
- searching for product advertisements,
- searching for competitor advertisements,
- searching based on customer problems,
- analyzing successful running ads.

Each task must include:
- specific search phrases,
- filtering instructions,
- advertising elements to analyze,
- signals that indicate product potential.


3. TikTok Creative Center:

Create tasks related to:
- analyzing product popularity,
- analyzing hashtags,
- analyzing viral videos,
- analyzing user comments.

Include:
- specific search phrases,
- hashtags,
- research instructions,
- evaluation criteria.


4. Marketplace research:

Create separate tasks for:

- Amazon,
- AliExpress,
- Temu,
- eBay.

For each platform define:
- what keywords to search,
- what products to compare,
- what data to collect:
  - number of reviews,
  - product rating,
  - popularity indicators,
  - recurring customer problems,
  - customer needs.


5. Customer review analysis:

Create tasks related to:
- finding negative reviews,
- finding purchase motivations,
- finding the most common problems,
- finding product improvement opportunities.

Include:
- where to search,
- what information to extract,
- how to use the findings in the product offer.


6. Social media research:

Create tasks for:

- TikTok,
- Instagram,
- YouTube,
- Pinterest.

For each:
- provide search phrases,
- provide hashtags,
- describe what to analyze,
- describe what signals indicate customer interest.


7. Final product audit:

Add a final summary task.

It should include:
- how to collect all research results,
- what criteria to evaluate,
- how to decide whether the product should move to the next stage.


Every task must be a practical execution instruction.

Do not create generic tasks.

Bad example:

"Check competitors"


Good example:

"Analyze competitor ads in Meta Ads Library:
1. Open Meta Ads Library.
2. Search for phrases: [phrase1], [phrase2], [phrase3].
3. Save active advertisements.
4. Analyze the hook, offer, comments, and how long the advertisement has been running."


Every task must be possible to complete by someone without additional expertise.


Return ONLY a JSON array following the format defined in the SYSTEM PROMPT.
"""


def analyse_checklist_generate_handler(
    knowledge_id: int,
    analyse_id: int,
    checklist_id: int
):
    container = Container()

    logger = container.logger()
    ollama_service = container.ollama_service()
    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.analysis_assembler()
    checklist_items_repository=container.checklist_items_repository()

    # ---------
    # Get product data
    # ---------

    knowledge_db = knowledge_repo.get_by_id(id=knowledge_id)

    knowledge_dto = OfferKnowledgeMapper.to_dto(
        item=knowledge_db
    )

    assembled_knowledge = knowledge_assembler.assemble_dto(
        item=knowledge_dto
    )

    json_offer_data = json.dumps(
        assembled_knowledge.to_dict(),
        ensure_ascii=False,
        indent=2
    )

    # ---------
    # Prepare prompt
    # ---------

    user_prompt = prepare_user_prompt(
        json_offer_data=json_offer_data
    )

    # ---------
    # Call LLM
    # ---------

    response = ollama_service.chat_llm(
        messages=[
            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=SYSTEM_PROMPT
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=user_prompt
            )
        ]
    )

    
    # ---------
    # Checklist Items Create
    # ---------
    checklist_items = []
    response_object = json.loads(response.content)

    for item in response_object:
        checklist_items.append(ChecklistItem(
            title=item["title"],
            description=item["description"],
            note=item["note"]
        ))

    checklist_items_db = checklist_items_repository.create_many(items=checklist_items)

    items_dtos = [ChecklistItemMapper.to_dto(ch) for ch in checklist_items_db]

    return items_dtos