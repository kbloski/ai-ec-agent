import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from domain.models.page_blueprint.page_blueprint import PageBlueprint



SYSTEM_PROMPT = """
Jesteś ekspertem od:

- E-commerce Landing Page Architecture
- Conversion Rate Optimization
- Direct Response Marketing
- Product Page Psychology
- Customer Journey Design


Twoim zadaniem jest stworzenie PAGE BLUEPRINT
dla sprzedażowego landing page produktu fizycznego.


Na podstawie:

- Knowledge Base
- Page Strategy
- Message Strategy
- Brand Strategy
- Marketing Strategy
- Offer Strategy


Page Blueprint NIE jest finalnym copy.


Określa:

- strukturę strony,
- kolejność sekcji,
- funkcję każdej sekcji,
- elementy potrzebne później do wygenerowania copy.



NIE GENERUJ:

- headline,
- subheadline,
- body copy,
- CTA,
- tekstów sprzedażowych,
- HTML,
- CSS,
- designu,
- obrazów.



CEL LANDING PAGE:


ATTENTION

↓

PROBLEM AWARENESS

↓

PRODUCT DESIRE

↓

VALUE UNDERSTANDING

↓

TRUST

↓

PURCHASE DECISION



KONTEKST:


Tworzysz głównie:

- e-commerce,
- produkty fizyczne,
- low ticket,
- direct response,
- pojedynczy produkt.



AVAILABLE SECTION TYPES:



hero

Cel:
Pierwszy kontakt.
Przekazuje główną wartość produktu.


problem

Cel:
Pokazuje problem, frustrację lub potrzebę klienta.


solution

Cel:
Pokazuje produkt jako rozwiązanie problemu.


benefits

Cel:
Pokazuje rezultaty i korzyści.


features

Cel:
Pokazuje konkretne cechy produktu.


how_it_works

Cel:
Wyjaśnia działanie produktu.


social_proof

Cel:
Buduje zaufanie poprzez dowody.


offer

Cel:
Pokazuje co klient otrzymuje.


risk_reversal

Cel:
Zmniejsza ryzyko zakupu.


faq

Cel:
Usuwa ostatnie pytania i obiekcje.


final_cta

Cel:
Prowadzi do zakupu.



OPTIONAL SECTION TYPES:



product_showcase

Użyj gdy produkt wymaga wizualnego przedstawienia.


comparison

Użyj gdy klient porównuje rozwiązania.


testimonials

Użyj gdy opinie zwiększają konwersję.


before_after

Użyj gdy produkt powoduje transformację.


unique_mechanism

Użyj gdy trzeba wyjaśnić dlaczego produkt działa.


bonus_stack

Użyj gdy oferta posiada dodatkowe elementy.


urgency

Użyj tylko gdy istnieje prawdziwy powód szybkiej decyzji.


pricing

Użyj gdy cena lub warianty mają wpływ na decyzję.



ZASADY WYBORU:



Nie używaj wszystkich sekcji.


Dla większości e-commerce low ticket:

hero
problem
solution
benefits
features
social_proof
offer
risk_reversal
faq
final_cta


są najczęściej wymagane.



Nie dodawaj:

- case studies,
- zaawansowanych sekcji B2B,
- strategii,
- copy.



SECTION PRIORITY:


"required"

Sekcja konieczna dla skuteczności strony.


"optional"

Sekcja zwiększająca konwersję,
ale możliwa do pominięcia.



OUTPUT FORMAT:


Zwróć dokładnie:


{
    "page_blueprint": {

        "page_type": "",

        "primary_conversion_goal": "",

        "sections": [

            {

                "order": 1,

                "section_type": "",

                "section_priority": "",

                "purpose": "",

                "customer_journey_stage": "",

                "conversion_role": "",

                "psychological_goal": "",

                "required_elements": [],

                "proof_elements": [],

                "objection_targets": [],

                "notes": ""

            }

        ]

    }
}



STRICT JSON RULES:


- root JSON musi posiadać "page_blueprint"
- page_blueprint musi posiadać "sections"
- sections musi być tablicą
- każda sekcja musi być obiektem
- section_type zawsze po angielsku
- wszystkie klucze JSON zawsze po angielsku
- nie generuj copy
- nie generuj tekstów reklamowych
- nie używaj markdown
- nie używaj ```json
- nie dodawaj komentarzy
- nie dodawaj tekstu poza JSON
- wszystkie pola muszą istnieć
- nie używaj null

"""



USER_PROMPT_TEMPLATE = """
Wygeneruj Page Blueprint na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


PAGE STRATEGY:

{page_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}

"""



def extract_json(content: str):

    content = content.strip()


    if "```" in content:

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    start = content.find("{")

    end = content.rfind("}")


    if start == -1 or end == -1:

        raise ValueError(
            "JSON object not found"
        )


    return content[start:end + 1]



def generate_page_blueprint_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int,
    page_strategy_id: int
):

    container = Container()


    page_strategy_service = (
        container.page_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    knowledge_service = (
        container.knowledge_service()
    )

    brand_marketing_service = (
        container.brand_marketing_service()
    )

    marketing_strategy_service = (
        container.marketing_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
    )


    page_blueprint_repository = (
        container.page_blueprint_repository()
    )

    page_blueprint_service = (
        container.page_blueprint_service()
    )

    ollama_service = (
        container.ollama_service()
    )



    page_strategy = (
        page_strategy_service
        .get_page_strategy_by_id(
            id=page_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service
        .get_message_strategy_by_id(
            id=message_strategy_id
        )
    )


    knowledge = (
        knowledge_service
        .get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    brand_strategy = (
        brand_marketing_service
        .get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service
        .get_marketing_strategy_by_id(
            id=marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service
        .get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )



    def serialize(obj):

        return json.dumps(
            obj.to_dict(),
            ensure_ascii=False,
            indent=2,
            default=str
        )



    user_prompt = USER_PROMPT_TEMPLATE.format(

        knowledge_json=serialize(
            knowledge
        ),

        page_strategy_json=serialize(
            page_strategy
        ),

        message_strategy_json=serialize(
            message_strategy
        ),

        brand_strategy_json=serialize(
            brand_strategy
        ),

        marketing_strategy_json=serialize(
            marketing_strategy
        ),

        offer_strategy_json=serialize(
            offer_strategy
        )

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



    try:

        content = extract_json(
            response.content
        )


        result = json.loads(
            content
        )


    except Exception as e:

        return {

            "error": "Invalid JSON response",

            "exception": str(e),

            "raw_response": response.content

        }



    page_blueprint_data = (
        result.get(
            "page_blueprint",
            {}
        )
    )



    if not page_blueprint_data:

        return {

            "error": "Missing page_blueprint",

            "raw_response": response.content

        }



    sections = (
        page_blueprint_data.get(
            "sections",
            []
        )
    )



    if not isinstance(
        sections,
        list
    ):

        return {

            "error": "Sections must be list",

            "raw_response": response.content

        }



    allowed_sections = {

        "hero",
        "problem",
        "solution",
        "benefits",
        "features",
        "how_it_works",
        "social_proof",
        "offer",
        "risk_reversal",
        "faq",
        "final_cta",
        "product_showcase",
        "comparison",
        "testimonials",
        "before_after",
        "unique_mechanism",
        "bonus_stack",
        "urgency",
        "pricing"

    }



    for section in sections:


        if (
            section.get("section_type")
            not in allowed_sections
        ):

            return {

                "error": "Invalid section_type",

                "section": section

            }



    entity = PageBlueprint(

        page_strategy_id=page_strategy_id,

        page_type=(
            page_blueprint_data.get(
                "page_type",
                "ecommerce_product"
            )
        ),

        primary_conversion_goal=(
            page_blueprint_data.get(
                "primary_conversion_goal",
                "purchase"
            )
        ),

        sections=sections

    )



    created = (
        page_blueprint_repository.create(
            entity
        )
    )



    return (
        page_blueprint_service
        .get_page_blueprint_by_id(
            id=created.id
        )
    )