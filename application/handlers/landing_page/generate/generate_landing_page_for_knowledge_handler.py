import json

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


SYSTEM_PROMPT = """
Jesteś ekspertem od tworzenia wysokokonwertujących stron sprzedażowych e-commerce
(CRO specialist, direct response copywriter, UX designer).

Twoim zadaniem jest przygotować kompletny plan landing page produktu,
który maksymalizuje sprzedaż.

Nie tworzysz kodu HTML/CSS.
Nie tworzysz projektu graficznego.

Tworzysz szczegółowy blueprint strony:
- co powinno znajdować się w każdej sekcji,
- jakie teksty powinny być użyte,
- jakie emocje wykorzystać,
- jakie zdjęcia/video powinny być pokazane,
- jakie obiekcje klienta trzeba rozwiać.

Bazuj na danych produktu i grupach docelowych.

Najważniejsze zasady:

1. Sprzedawaj korzyści, nie funkcje.

Nie:
"3000W silnik"

Tak:
"Poradzi sobie z gałęziami i drewnem bez wysiłku."

2. Każda sekcja musi mieć konkretny cel sprzedażowy.

3. Strona musi prowadzić klienta przez proces:

Problem
↓
Uświadomienie potrzeby
↓
Rozwiązanie
↓
Korzyści
↓
Dowód społeczny
↓
Usunięcie ryzyka
↓
Zakup


4. Uwzględnij:

- urgency (pilność)
- trust building
- social proof
- gwarancje
- CTA
- FAQ
- upsell/cross-sell
- elementy zwiększające AOV


5. Pisz teksty gotowe do wykorzystania na stronie.

Dla każdej sekcji przygotuj:

- nazwa sekcji
- cel sekcji
- główny nagłówek
- podtytuł
- tekst sprzedażowy
- CTA (jeżeli potrzebne)
- rekomendowane zdjęcia/video
- elementy zwiększające konwersję


6. Myśl jak klient.

Uwzględnij:
- czego klient się boi,
- jakie ma pytania,
- dlaczego może nie kupić,
- co musi zobaczyć aby zaufać.


7. Dopasuj komunikację do najlepszej grupy docelowej.


Zwróć wynik jako poprawny JSON:

{
 "landing_page_strategy": {
    "target_customer": "",
    "main_angle": "",
    "core_message": "",
    "sections": [
       {
          "order": 1,
          "name": "",
          "goal": "",
          "headline": "",
          "subheadline": "",
          "copy": "",
          "cta": "",
          "visual_direction": "",
          "conversion_elements": []
       }
    ],
    "additional_conversion_elements": {
        "urgency": [],
        "trust": [],
        "social_proof": [],
        "upsells": [],
        "chatbot_strategy": [],
        "faq_topics": []
    }
 }
}
"""


def get_user_prompt(product_json: str):
    return f"""
Przygotuj wysokokonwertującą stronę sprzedażową dla poniższego produktu.

DANE PRODUKTU:

{product_json}


Wykorzystaj wszystkie dostępne informacje:

- opis produktu
- value proposition
- problemy klientów
- rozwiązania
- transformacje
- benefity funkcjonalne
- benefity emocjonalne
- wyróżniki
- mocne strony
- ograniczenia
- grupy docelowe
- obiekcje klientów


Struktura strony, którą masz zoptymalizować:


1. Pasek informacyjny nad menu
- dostawa
- promocje
- gwarancja


2. Menu


3. Hero section:
- nazwa produktu
- główny komunikat
- zdjęcie/video
- cena
- CTA
- trust badges


4. Problem → rozwiązanie


5. Najważniejsze benefity


6. Szczegóły produktu i specyfikacja


7. Produkt w użyciu:
- lifestyle
- before/after
- UGC


8. Jak działa krok po kroku


9. Social proof


10. FAQ


11. Final CTA + gwarancja


Dodatkowo uwzględnij:

- elementy pilności
- budowanie zaufania
- chatbot
- quiz produktowy jeżeli ma sens
- upsell/cross-sell
- zwiększenie wartości koszyka


Nie pisz ogólnych porad.
Przygotuj konkretną stronę dla tego produktu.
"""


def generate_landing_page_for_knowledge_handler(knowledge_id: int):

    container = Container()

    logger = container.logger()
    knowledge_service = container.knowledge_service()

    ollama_service = container.ollama_service()


    assembled_knowledge_dto =  knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id)


    knowledge_json = json.dumps(
        assembled_knowledge_dto.to_dict(),
        ensure_ascii=False,
        indent=2
    )


    logger.info(
        "Generating landing page strategy"
    )


    result = ollama_service.chat_llm(
        messages=[
            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=SYSTEM_PROMPT
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=get_user_prompt(
                    knowledge_json
                )
            )
        ]
    )


    response_content = result.content


    try:
        landing_page_strategy = json.loads(
            response_content
        )

    except Exception:
        landing_page_strategy = {
            "raw_response": response_content
        }


    return landing_page_strategy