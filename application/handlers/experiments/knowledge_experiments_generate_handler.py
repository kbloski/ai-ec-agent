import json

from di.container import Container
from domain.models.models import LlmOllamaMessage
from domain.enums.enums import OllamaMessageRole
from domain.enums.experiment_status import ExperimentStatus
from application.mappers.experiment_mapper import ExperimentMapper


SYSTEM_PROMPT = """

Jesteś ekspertem performance marketingu.

Twoim zadaniem jest tworzenie eksperymentów marketingowych.

Nie tworzysz reklam.

Tworzysz hipotezy testowe.


Każdy eksperyment musi zawierać:

name
experiment_type
framework
angle
psychology_trigger
awareness_stage
hypothesis
expected_result
primary_problem
primary_desire
primary_fear
dream_outcome
big_idea
big_promise
unique_mechanism
core_message
offer_strategy
urgency_strategy
cta_strategy
proof_strategy
priority
confidence


Zwróć wyłącznie JSON:

{
"experiments":[]
}


Wygeneruj różne eksperymenty.

Nie powtarzaj angle.

Nie powtarzaj frameworków.

Każdy eksperyment musi być osobną hipotezą marketingową.

Nie dodawaj:

- markdown,
- ```json,
- komentarzy,
- opisów przed JSON.

"""


USER_PROMPT_TEMPLATE = """

Na podstawie danych produktu wygeneruj dokładnie:

{count}

różnych eksperymentów marketingowych.


DANE PRODUKTU:

{product_json}

Zwróć dokładnie strukturę:

{{
"experiments":[
    {{
        "name":"",
        "experiment_type":"",
        "framework":"",
        "angle":"",
        "psychology_trigger":"",
        "awareness_stage":"",
        "hypothesis":"",
        "expected_result":"",
        "primary_problem":"",
        "primary_desire":"",
        "primary_fear":"",
        "dream_outcome":"",
        "big_idea":"",
        "big_promise":"",
        "unique_mechanism":"",
        "core_message":"",
        "offer_strategy":"",
        "urgency_strategy":"",
        "cta_strategy":"",
        "proof_strategy":"",
        "priority":0,
        "confidence":0
    }}
]
}}


DODATKOWE ZASADY:

1. Wygeneruj dokładnie {count} elementów.

2. Każdy eksperyment musi mieć:
- inny angle,
- inny framework,
- inną hipotezę testową.

3. PRIORITY i CONFIDENCE muszą być integer w skali 1-10.
"""


def knowledge_experiments_generate_handler(
    knowledge_id: int,
    count: int
):

    if count <= 0:
        raise ValueError(
            "count musi być większe od 0"
        )

    container = Container()

    knowledge_service = container.knowledge_service()
    ollama_service = container.ollama_service()
    experiments_repository = container.experiments_repository()
    experiment_service = container.experiment_service()

    knowledge_details = knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id)

    product_json = json.dumps(
        knowledge_details.to_dict(),
        ensure_ascii=False,
        indent=2,
        default=str
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(count=count, product_json=product_json)

    response = (
        ollama_service.chat_llm(
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
    )

    generated = json.loads(response.content.strip())
    experiments = generated.get("experiments", [])
    results = []

    for experiment_data in experiments:
        experiment_data.setdefault("status", ExperimentStatus.DRAFT.value)

        experiment = experiments_repository.create(
            ExperimentMapper.to_entity(
                knowledge_id=knowledge_id,
                data=experiment_data
            )
        )

        results.append(
            experiment_service.get_experiment_by_id(id=experiment.id)
        )

    return results
