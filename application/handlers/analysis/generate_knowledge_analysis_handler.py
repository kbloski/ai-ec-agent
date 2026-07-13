import json
from typing import Dict, Any, List

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



# PRODUCT_ANALYSIS_QUESTIONS = [

#     "Jaki konkretny problem rozwiązuje produkt?",

#     "Czy jest to realny i istotny problem dla klientów?",

#     "Jak duża jest potrzeba rozwiązania tego problemu?",

#     "Jak bardzo uciążliwy jest problem dla klienta? Oceń w skali 1-10.",

#     "Czy jest to drobna niedogodność czy realna frustracja?",

#     "Jakie emocje wywołuje ten problem u klienta?",

#     "Czy klient aktywnie szuka rozwiązania?",

#     "Czy produkt jest must have czy nice to have?",

#     "Czy produkt może generować zakup impulsywny?",


#     "Czy istnieją produkty konkurencyjne?",

#     "Jakie produkty konkurencyjne istnieją?",

#     "Czym produkt różni się od konkurencji?",

#     "Czy produkt posiada przewagę konkurencyjną?",


#     "Jak często klient spotyka się z tym problemem?",

#     "Czy częstotliwość problemu sprzyja wysokiej sprzedaży?",


#     "Czy produkt posiada efekt WOW?",

#     "Czy produkt wyróżnia się na rynku?",

#     "Czy łatwo stworzyć atrakcyjne reklamy produktu?",


#     "Kto jest idealnym klientem tego produktu?",

#     "Jak duża jest grupa docelowa?",

#     "Jakie są potrzeby i motywacje klientów?",


#     "Czy produkt dobrze wygląda na zdjęciach i filmach?",

#     "Czy nadaje się do reklam TikTok/Facebook/Instagram?",


#     "Jaka cena sprzedaży będzie atrakcyjna dla klienta?",

#     "Oblicz minimalną cenę sprzedaży według wzoru: cena zakupu + 15 zł dostawy + 20 zł reklamy + 15 zł marży.",

#     "Czy klient będzie skłonny zapłacić minimalną cenę sprzedaży?",
#     "Zaproponuj realistyczną cenę sprzedaży.",

#     "Czy produkt ma potencjał osiągnięcia dobrej rentowności?",


#     "Czy produkt sprawia wrażenie wysokiej jakości?",

#     "Czy istnieje ryzyko reklamacji i zwrotów?",


#     "Czy produkt jest łatwy w wysyłce?",

#     "Czy istnieje ryzyko uszkodzeń podczas transportu?",


#     "Czy produkt można sprzedawać cały rok?",

#     "Czy występuje sezonowość?",


#     "Czy klient kupi produkt ponownie?",

#     "Czy można sprzedawać dodatki lub akcesoria?",


#     "Czy produkt wymaga elektroniki lub specjalnej obsługi?",

#     "Czy produkt wymaga certyfikatów lub zezwoleń?",


#     "Oceń potencjał produktu w skali 1-10.",

#     "Jakie są największe zalety produktu?",

#     "Jakie są największe ryzyka sprzedaży?",

#     "Co należy poprawić przed rozpoczęciem sprzedaży?",

#     "Czy rekomendujesz sprzedaż produktu? TAK/WARUNKOWO/NIE. Dlaczego?"
# ]

PRODUCT_ANALYSIS_QUESTIONS = [

    "Jaki konkretny problem rozwiązuje produkt? Opisz problem klienta, jego skalę, częstotliwość występowania oraz poziom uciążliwości w skali 1-10.",

    "Jak istotny jest problem dla klienta? Oceń, czy jest to drobna niedogodność, realna frustracja czy pilna potrzeba wymagająca rozwiązania.",

    "Jakie emocje wywołuje ten problem u klienta i jakie są główne motywacje zakupu produktu?",

    "Czy klient aktywnie szuka rozwiązania tego problemu? Oceń poziom intencji zakupowej i prawdopodobieństwo zakupu.",

    "Czy produkt jest typu must have czy nice to have? Uzasadnij ocenę.",

    "Czy produkt ma potencjał do zakupu impulsywnego? Oceń, jakie czynniki mogą powodować szybki zakup.",


    "Jak wygląda konkurencja dla tego produktu? Wymień istniejące produkty konkurencyjne, alternatywne rozwiązania oraz głównych konkurentów.",

    "Czym produkt różni się od konkurencji? Oceń, czy posiada wyraźną przewagę konkurencyjną i jaka ona jest.",


    "Jak często klient może spotykać się z problemem rozwiązywanym przez produkt? Oceń, czy częstotliwość problemu sprzyja wysokiej sprzedaży.",


    "Czy produkt posiada efekt WOW? Oceń, czy wyróżnia się na rynku i czy łatwo stworzyć atrakcyjne materiały reklamowe pokazujące jego wartość.",


    "Kim jest idealny klient tego produktu? Opisz grupę docelową, jej wielkość, potrzeby, motywacje oraz zachowania zakupowe.",


    "Czy produkt dobrze prezentuje się wizualnie? Oceń potencjał sprzedaży poprzez zdjęcia i krótkie materiały video na TikTok, Facebook i Instagram.",


    "Jaka powinna być cena sprzedaży produktu? Uwzględnij atrakcyjność dla klienta, konkurencję oraz wylicz minimalną cenę według wzoru: cena zakupu + 15 zł dostawy + 20 zł reklamy + 15 zł marży.",

    "Czy produkt ma potencjał osiągnięcia dobrej rentowności? Oceń relację między ceną zakupu, ceną sprzedaży, kosztami reklamy i możliwą marżą.",


    "Czy produkt sprawia wrażenie wysokiej jakości? Oceń postrzeganą wartość produktu oraz ryzyko negatywnych opinii.",

    "Jakie jest ryzyko reklamacji, zwrotów i niezadowolenia klientów? Wskaż główne powody potencjalnych problemów.",


    "Czy produkt jest łatwy w logistyce? Oceń łatwość magazynowania, pakowania, wysyłki oraz ryzyko uszkodzeń podczas transportu.",


    "Czy produkt można sprzedawać przez cały rok? Oceń sezonowość, okresy zwiększonego i zmniejszonego popytu.",


    "Czy klient może kupić produkt ponownie? Oceń potencjał powtarzalnych zakupów oraz możliwość sprzedaży dodatków, akcesoriów lub kolejnych produktów.",


    "Czy produkt wymaga elektroniki, specjalnej obsługi, certyfikatów lub zezwoleń? Wskaż potencjalne bariery sprzedaży.",


    "Oceń ogólny potencjał produktu w skali 1-10. Uwzględnij problem klienta, konkurencję, marketing, marżę, logistykę i ryzyko.",

    "Jakie są największe zalety produktu z punktu widzenia sprzedaży?",

    "Jakie są największe ryzyka sprzedaży tego produktu?",

    "Co należy poprawić lub sprawdzić przed rozpoczęciem sprzedaży produktu?",

    "Czy rekomendujesz sprzedaż produktu? Odpowiedz: TAK / WARUNKOWO / NIE i uzasadnij decyzję."
]



def chunk_list(
    items: List[str],
    size: int
) -> List[List[str]]:
    """
    Dzieli listę pytań na mniejsze paczki.
    """

    return [
        items[i:i + size]
        for i in range(0, len(items), size)
    ]



def build_product_context_prompt(
    product_data: Dict[str, Any]
) -> str:

    return f"""
Dane produktu:

{json.dumps(
    product_data,
    ensure_ascii=False,
    indent=2
)}

Przeanalizuj produkt na podstawie tych informacji.
Nie zakładaj informacji, których nie ma w danych.
"""



def build_questions_prompt(
    questions: List[str],
    batch_number: int,
    total_batches: int
) -> str:

    return f"""
To jest część analizy {batch_number}/{total_batches}.

Odpowiedz na poniższe pytania dotyczące produktu:

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2
)}


Zwróć wynik dokładnie w takim formacie:

[
    {{
        "pytanie": "dokładny tekst pytania",
        "odpowiedz": "szczegółowa odpowiedź"
    }}
]


Ważne zasady:

- Każde pytanie musi posiadać odpowiedź.
- Nie pomijaj pytań.
- Nie zmieniaj nazwy pola "pytanie".
- Nie zmieniaj nazwy pola "odpowiedz".
- Nie zwracaj żadnego tekstu poza JSON.
- Nie używaj markdown.
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
    # Podział pytań
    #

    question_batches = chunk_list(
        PRODUCT_ANALYSIS_QUESTIONS,
        5
    )



    final_analysis = []



    #
    # Analiza batchami po 5 pytań
    #

    for index, batch in enumerate(question_batches):

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
                    questions=batch,
                    batch_number=index + 1,
                    total_batches=len(question_batches)
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
Niepoprawny JSON od modelu.

Batch:
{index + 1}

Response:
{response.content}
"""
            )



        if not isinstance(batch_result, list):

            raise Exception(
                f"""
Model nie zwrócił listy.

Batch:
{index + 1}
"""
            )



        final_analysis.extend(
            batch_result
        )



    return {

        "product_id": knowledge_id,

        "analysis": final_analysis

    }