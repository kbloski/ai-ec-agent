import json
from typing import Dict, Any

from di.container import Container

from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage

from domain.enums.ollama_message_role import OllamaMessageRole



BASE_SYSTEM_PROMPT = """
Jesteś ekspertem ds. analizy produktów e-commerce.

Twoim zadaniem jest analizowanie produktów pod kątem ich potencjału sprzedażowego.

Myśl jak przedsiębiorca inwestujący własne pieniądze w produkt.

Zasady:

1. Odpowiadaj konkretnie i rzeczowo.
2. Nie wymyślaj informacji, których nie ma w danych.
3. Jeżeli brakuje informacji, zaznacz ten fakt.
4. Oceniaj produkt obiektywnie.
5. Wskazuj zarówno zalety jak i ryzyka.
6. Odpowiedzi muszą być przygotowane w formacie JSON.
7. Nie dodawaj żadnego tekstu poza JSON.
"""



PRODUCT_ANALYSIS_QUESTIONS = [

    "Jaki konkretny problem rozwiązuje produkt?",
"""
"""

    "Czy jest to realny i istotny problem dla klientów?",

    "Jak duża jest potrzeba rozwiązania tego problemu?",

    "Jak bardzo uciążliwy jest problem dla klienta? Oceń w skali 1-10.",

    "Czy jest to drobna niedogodność czy realna frustracja?",

    "Jakie emocje wywołuje ten problem u klienta?",

    "Czy klient aktywnie szuka rozwiązania?",

    "Czy produkt jest must have czy nice to have?",

    "Czy produkt może generować zakup impulsywny?",


    "Czy istnieją produkty konkurencyjne?",

    "Jakie produkty konkurencyjne istnieją?",

    "Czym produkt różni się od konkurencji?",

    "Czy produkt posiada przewagę konkurencyjną?",


    "Jak często klient spotyka się z tym problemem?",

    "Czy częstotliwość problemu sprzyja wysokiej sprzedaży?",


    "Czy produkt posiada efekt WOW?",

    "Czy produkt wyróżnia się na rynku?",

    "Czy łatwo stworzyć atrakcyjne reklamy produktu?",


    "Kto jest idealnym klientem tego produktu?",

    "Jak duża jest grupa docelowa?",

    "Jakie są potrzeby i motywacje klientów?",


    "Czy produkt dobrze wygląda na zdjęciach i filmach?",

    "Czy nadaje się do reklam TikTok/Facebook/Instagram?",


    "Jaka cena sprzedaży będzie atrakcyjna dla klienta?",

    "Oblicz minimalną cenę sprzedaży według wzoru: cena zakupu + 15 zł dostawy + 20 zł reklamy + 15 zł marży.",

    "Czy klient będzie skłonny zapłacić minimalną cenę sprzedaży?",

    "Zaproponuj realistyczną cenę sprzedaży.",

    "Czy produkt ma potencjał osiągnięcia dobrej rentowności?",


    "Czy produkt sprawia wrażenie wysokiej jakości?",

    "Czy istnieje ryzyko reklamacji i zwrotów?",


    "Czy produkt jest łatwy w wysyłce?",

    "Czy istnieje ryzyko uszkodzeń podczas transportu?",


    "Czy produkt można sprzedawać cały rok?",

    "Czy występuje sezonowość?",


    "Czy klient kupi produkt ponownie?",

    "Czy można sprzedawać dodatki lub akcesoria?",


    "Czy produkt wymaga elektroniki lub specjalnej obsługi?",

    "Czy produkt wymaga certyfikatów lub zezwoleń?",


    "Oceń potencjał produktu w skali 1-10.",

    "Jakie są największe zalety produktu?",

    "Jakie są największe ryzyka sprzedaży?",

    "Co należy poprawić przed rozpoczęciem sprzedaży?",

    "Czy rekomendujesz sprzedaż produktu? TAK/WARUNKOWO/NIE. Dlaczego?"
]



def build_product_data_prompt(
    product_data: Dict[str, Any]
) -> str:

    return f"""
Dane produktu do analizy:

{json.dumps(
    product_data,
    ensure_ascii=False,
    indent=2
)}

Zapamiętaj te informacje. W kolejnym poleceniu otrzymasz pytania dotyczące analizy produktu.
"""



def build_product_questions_prompt() -> str:

    return f"""
Przeanalizuj wcześniej przekazany produkt.

Odpowiedz na każde pytanie:

{json.dumps(
    PRODUCT_ANALYSIS_QUESTIONS,
    ensure_ascii=False,
    indent=2
)}


Wymagany format odpowiedzi:

[
    {{
        "pytanie": "Treść pytania",
        "odpowiedz": "Twoja szczegółowa odpowiedź"
    }}
]


Zasady:
- Każde pytanie musi mieć swoją odpowiedź.
- Nie pomijaj żadnego pytania.
- Zachowaj dokładnie nazwę pola:
  pytanie
  odpowiedz

Zwróć wyłącznie poprawny JSON.
"""



def generate_knowledge_analysis_handler(
    knowledge_id: int
) -> Dict[str, Any]:

    container = Container()

    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()


    #
    # Pobranie produktu
    #

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



    #
    # USER PROMPT 1 - dane produktu
    #

    # product_data_prompt = build_product_data_prompt(
    #     product_data=knowledge_json
    # )



    #
    # USER PROMPT 2 - pytania + format
    #

    # questions_prompt = build_product_questions_prompt()



    response = ollama_service.chat_llm(
        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=BASE_SYSTEM_PROMPT
            ),
            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content="Co to za produkt?: " + json.dumps(knowledge_json)
            ),

            # LlmOllamaMessage(
            #     role=OllamaMessageRole.USER,
            #     content=product_data_prompt
            # ),


            # LlmOllamaMessage(
            #     role=OllamaMessageRole.USER,
            #     content=questions_prompt
            # )

        ]
    )


    #
    # Parsowanie JSON
    #
    analysis = json.loads( response.content )

    return analysis