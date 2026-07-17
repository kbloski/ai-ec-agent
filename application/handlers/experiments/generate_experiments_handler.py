import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.experiment_strategy.experiment_strategy import ExperimentStrategy
from domain.models.experiments.experiment import Experiment


SYSTEM_PROMPT = """
Jesteś ekspertem od growth marketingu oraz systemów eksperymentacji marketingowej.

Twoim zadaniem jest stworzenie strategii eksperymentów marketingowych
na podstawie pełnego kontekstu:

1. KNOWLEDGE BASE:
- produkt,
- klient,
- rynek,
- customer voice,
- problemy,
- potrzeby,
- obiekcje,
- motywacje zakupowe.


2. BRAND MARKETING:
- positioning,
- wartości marki,
- osobowość marki,
- brand voice,
- brand tone,
- target perception.


3. MARKETING STRATEGY:
- segmenty,
- kanały,
- customer journey,
- cele marketingowe.


4. OFFER STRATEGY:
- oferta,
- value proposition,
- benefity,
- mechanizm wartości,
- redukcja ryzyka.


5. MESSAGE STRATEGY:
- główne komunikaty,
- kąty komunikacji,
- emocje,
- proof points,
- obiekcje.


CEL:

Stwórz eksperymenty, które pozwolą znaleźć
największe dźwignie wzrostu.


Nie twórz przypadkowych testów kreatywnych.

Najpierw testuj:

1. audience fit
2. customer problem
3. message-market fit
4. offer-market fit
5. channel fit
6. creative optimization


Każdy eksperyment powinien odpowiadać na pytanie:

"Jakiej decyzji biznesowej ten eksperyment pomoże dokonać?"


Każdy eksperyment musi zawierać:

- nazwę,
- kategorię,
- strategic_question,
- cel,
- hipotezę,
- podstawę hipotezy,
- uzasadnienie,
- grupę docelową,
- etap lejka,
- kanał,
- wymagany asset,
- testowaną zmienną,
- wariant kontrolny,
- wariant testowy,
- metryki sukcesu,
- regułę decyzji,
- oczekiwaną wiedzę,
- priorytetyzację.


Priorytetyzację licz według:

Impact:
Jak duży wpływ może mieć wynik?

Confidence:
Jak mocne są obecne przesłanki?

Ease:
Jak łatwo i tanio można wykonać test?


Zwróć wyłącznie JSON:

{
    "experiment_strategy": "",

    "learning_objectives": [
        ""
    ],

    "experiments": [

        {
            "name": "",

            "category": "",


            "strategic_question": "",


            "objective": "",


            "hypothesis": "",


            "hypothesis_basis": [
                ""
            ],


            "reason": "",


            "target_audience": "",


            "funnel_stage": "",


            "channel": "",


            "asset_type": "",


            "variable_tested": "",


            "control_variant": "",


            "test_variant": "",


            "success_metrics": [
                ""
            ],


            "decision_rule": "",


            "expected_learning": "",


            "priority": {
                "impact": 0,
                "confidence": 0,
                "ease": 0,
                "score": 0
            },


            "estimated_cost": "",


            "estimated_duration": "",


            "status": "planned"
        }

    ]
}


Bez markdown.
Bez komentarzy.
Tylko JSON.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj strategię eksperymentów marketingowych.

KNOWLEDGE BASE:

{knowledge_json}


BRAND MARKETING:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}

"""


def generate_experiments_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int
):

    container = Container()

    knowledge_service = container.knowledge_service()
    brand_marketing_service = container.brand_marketing_service()
    marketing_strategy_service = container.marketing_strategy_service()
    offer_strategy_service = container.offer_strategy_service()
    message_strategy_service = container.message_strategy_service()
    experiment_strategy_repository = container.experiment_strategy_repository()
    experiments_repository = container.experiments_repository()
    experiment_strategy_service = container.experiment_strategy_service()

    ollama_service = container.ollama_service()


    knowledge = knowledge_service.get_knowledge_details_by_id(
        knowledge_id=knowledge_id
    )

    brand_marketing = brand_marketing_service.get_brand_marketing_by_id(
        id=brand_marketing_id
    )

    marketing_strategy = marketing_strategy_service.get_marketing_strategy_by_id(
        id=marketing_strategy_id
    )

    offer_strategy = offer_strategy_service.get_offer_strategy_by_id(
        id=offer_strategy_id
    )

    message_strategy = message_strategy_service.get_message_strategy_by_id(
        id=message_strategy_id
    )


    def serialize(data):
        return json.dumps(
            data.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )


    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=serialize(knowledge),

        brand_strategy_json=serialize(brand_marketing),

        marketing_strategy_json=serialize(marketing_strategy),

        offer_strategy_json=serialize(offer_strategy),

        message_strategy_json=serialize(message_strategy)

    )


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


    data = json.loads(response.content.strip())

    strategy_entity = ExperimentStrategy(
        knowledge_id=knowledge_id,
        brand_marketing_id=brand_marketing_id,
        marketing_strategy_id=marketing_strategy_id,
        offer_strategy_id=offer_strategy_id,
        message_strategy_id=message_strategy_id,
        experiment_strategy=data.get("experiment_strategy"),
        learning_objectives=data.get("learning_objectives", []),
    )
    created_strategy = experiment_strategy_repository.create(strategy_entity)

    for experiment in data.get("experiments", []):
        experiment_entity = Experiment(
            experiment_strategy_id=created_strategy.id,
            name=experiment.get("name"),
            category=experiment.get("category"),
            strategic_question=experiment.get("strategic_question"),
            objective=experiment.get("objective"),
            hypothesis=experiment.get("hypothesis"),
            hypothesis_basis=experiment.get("hypothesis_basis", []),
            reason=experiment.get("reason"),
            target_audience=experiment.get("target_audience"),
            funnel_stage=experiment.get("funnel_stage"),
            channel=experiment.get("channel"),
            asset_type=experiment.get("asset_type"),
            variable_tested=experiment.get("variable_tested"),
            control_variant=experiment.get("control_variant"),
            test_variant=experiment.get("test_variant"),
            success_metrics=experiment.get("success_metrics", []),
            decision_rule=experiment.get("decision_rule"),
            expected_learning=experiment.get("expected_learning"),
            priority=experiment.get("priority", {}),
            estimated_cost=experiment.get("estimated_cost"),
            estimated_duration=experiment.get("estimated_duration"),
            status=experiment.get("status", "planned"),
        )
        experiments_repository.create(experiment_entity)

    return experiment_strategy_service.get_experiment_strategy_by_id(id=created_strategy.id)