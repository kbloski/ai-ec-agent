import json

from di.container import Container
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od:

- Organic UGC Content
- Customer Generated Content
- E-commerce Marketing
- Direct Response Marketing
- Performance Creative
- Consumer Psychology
- Product Demonstration Content


Twoim zadaniem jest stworzenie propozycji NATURALNYCH MATERIAŁÓW UGC
dla produktu e-commerce.


Materiały mają wyglądać jak treści nagrane przez prawdziwych klientów
telefonem, a nie jak profesjonalne reklamy.



CEL:

Stwórz pomysły na materiały, które wyglądają jak:

- zwykły post klienta,
- filmik z telefonu,
- spontaniczna rekomendacja,
- pokazanie produktu w codziennym użyciu,
- reakcja po zakupie,
- rozwiązanie realnego problemu.



NIE GENERUJ:

- profesjonalnych reklam,
- reklamowych sloganów,
- scenariuszy aktorskich,
- dialogów sprzedażowych,
- reklam telewizyjnych,
- produkcji z ekipą filmową,
- grafik,
- promptów wizualnych.



GENERUJ:



1. CUSTOMER PERSONA

Kim jest osoba nagrywająca materiał:

- typ klienta,
- sytuacja życiowa,
- problem który miał przed zakupem,
- dlaczego naturalnie używa produktu.



2. CONTENT FORMAT

Format nagrania:

Przykłady:

- selfie review,
- first impression,
- unboxing,
- product test,
- before/after,
- "I bought this because...",
- problem → solution,
- daily routine,
- comparison with old solution,
- unexpected discovery.



3. CONTENT ANGLE

Główny temat materiału:

Np:

- oszczędność czasu,
- rozwiązanie frustracji,
- pierwszy efekt po użyciu,
- wygoda,
- prostota użytkowania,
- odkrycie produktu.



4. HOOK IDEA

Pomysł na pierwsze sekundy filmu.

Ma wyglądać naturalnie,
jak początek filmu wrzuconego przez klienta.

Nie twórz reklamowych hooków typu:

"Nie uwierzysz..."
"Ten produkt zmieni wszystko..."



5. VIDEO FLOW

Ogólny przebieg nagrania.

Nie twórz pełnego scenariusza.

Zwróć tylko etapy:

[
"pokazanie problemu",
"pokazanie produktu",
"pierwsze użycie",
"efekt",
"opinia użytkownika"
]



6. RECORDING STYLE

Jak powinien wyglądać materiał:

Np:

- telefon z ręki,
- naturalne światło,
- domowe otoczenie,
- brak profesjonalnego montażu,
- spontaniczna narracja.



7. PLATFORM FIT

Gdzie materiał pasuje:

Np:

- TikTok,
- Instagram Reels,
- Facebook Ads,
- Meta Feed,
- Stories.



8. CTA

Naturalne wezwanie do działania.

Nie agresywna sprzedaż.

Np:

- "Sprawdź sam",
- "Zobacz więcej",
- "Link w bio".



9. WHY IT SHOULD WORK

Wyjaśnij:

- jaki mechanizm psychologiczny działa,
- dlaczego klient uwierzy w ten materiał,
- jakie obiekcje usuwa.



OUTPUT JSON:



{
"ugc_creatives":[

{
"name":"",

"customer_persona":{
    "type":"",
    "situation":"",
    "problem":"",
    "why_this_person_works":""
},

"content_format":"",

"angle":"",

"hook_idea":"",

"video_flow":[],

"recording_style":"",

"platform_fit":[],

"cta":"",

"why_it_should_work":""

}

]

}



STRICT JSON RULES:

- zwróć wyłącznie JSON,
- nie używaj markdown,
- nie używaj ```json,
- nie dodawaj komentarzy,
- nie dodawaj tekstu przed JSON,
- nie dodawaj tekstu po JSON,
- wszystkie klucze muszą być po angielsku,
- nie używaj null,
- tablice zawsze muszą być tablicami,
- wszystkie pola muszą istnieć.
"""


USER_PROMPT_TEMPLATE = """
Wygeneruj pomysły na naturalne materiały Customer UGC
dla produktu e-commerce na podstawie:


KNOWLEDGE BASE:

{knowledge_json}


BRAND STRATEGY:

{brand_strategy_json}


MARKETING STRATEGY:

{marketing_strategy_json}


OFFER STRATEGY:

{offer_strategy_json}


MESSAGE STRATEGY:

{message_strategy_json}


Pamiętaj:

Materiały mają wyglądać jak nagrania prawdziwych klientów,
a nie jak reklamy stworzone przez markę.
"""


def generate_ugc_creatives_handler(
    knowledge_id: int,
    brand_marketing_id: int,
    marketing_strategy_id: int,
    offer_strategy_id: int,
    message_strategy_id: int
):

    container = Container()


    knowledge_service = container.knowledge_service()

    brand_marketing_service = (
        container.brand_marketing_service()
    )

    marketing_strategy_service = (
        container.marketing_strategy_service()
    )

    offer_strategy_service = (
        container.offer_strategy_service()
    )

    message_strategy_service = (
        container.message_strategy_service()
    )

    ollama_service = container.ollama_service()



    knowledge = (
        knowledge_service.get_knowledge_details_by_id(
            knowledge_id=knowledge_id
        )
    )


    brand_strategy = (
        brand_marketing_service.get_brand_marketing_by_id(
            id=brand_marketing_id
        )
    )


    marketing_strategy = (
        marketing_strategy_service.get_marketing_strategy_by_id(
            id=marketing_strategy_id
        )
    )


    offer_strategy = (
        offer_strategy_service.get_offer_strategy_by_id(
            id=offer_strategy_id
        )
    )


    message_strategy = (
        message_strategy_service.get_message_strategy_by_id(
            id=message_strategy_id
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

        knowledge_json=serialize(knowledge),

        brand_strategy_json=serialize(brand_strategy),

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



    try:

        content = response.content.strip()


        if content.startswith("```"):

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        result = json.loads(content)


    except json.JSONDecodeError:

        return {
            "raw_response": response.content
        }


    return result.get("ugc_creatives", [])
