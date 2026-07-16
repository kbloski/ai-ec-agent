import json

from di.container import Container
from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


# ==========================================================
# PROMPT 1
# LANDING PAGE STRATEGIST
# ==========================================================

LANDING_PAGE_SYSTEM_PROMPT = """

Jesteś ekspertem od tworzenia wysokokonwertujących stron
sprzedażowych e-commerce.

Twoja specjalizacja:
- Direct Response Marketing
- CRO
- UX sprzedażowy
- Copywriting produktowy


Twoim zadaniem jest stworzenie STRATEGII STRONY PRODUKTOWEJ.

Nie generujesz kodu.

Tworzysz dokładny blueprint dla:
- copywritera
- designera
- developera


Analizuj produkt i przygotuj:

1. Target klienta:
- kto kupuje
- jaki ma problem
- czego chce osiągnąć


2. Główny angle sprzedażowy:
- dlaczego klient powinien kupić
- jaka jest największa obietnica produktu


3. Strukturę landing page:


Każda sekcja musi zawierać:

- nazwę sekcji
- cel sprzedażowy
- nagłówek
- podnagłówek
- tekst
- CTA
- opis zdjęcia/video


Struktura bazowa:


1. Pasek informacyjny:
- dostawa
- promocja
- gwarancja


2. Hero section:

Musi zawierać:
- główną obietnicę
- produkt
- benefit
- CTA


3. Problem → rozwiązanie

Pokazać:
- frustrację klienta
- konsekwencje problemu
- produkt jako rozwiązanie


4. Najważniejsze benefity:

3-5 najważniejszych korzyści.


5. Szczegóły produktu:

Funkcje zamień na korzyści.


6. Produkt w użyciu:

Zdjęcia:
- lifestyle
- zastosowanie
- przed/po


7. Jak działa:

Prosty proces krok po kroku.


8. Social proof.


9. FAQ.


10. Final CTA.


Zasady:

Nie opisuj funkcji technicznych bez wyjaśnienia wartości.

Nie:
"3000W silnik"

Tak:
"Więcej mocy do szybkiego cięcia gałęzi."


Myśl jak klient:
"Dlaczego miałbym kupić właśnie to?"

Zwróć JSON.


FORMAT:

{
 "strategy": {
    "customer":"",
    "main_problem":"",
    "main_solution":"",
    "main_angle":"",
    "sections":[]
 }
}

"""


def get_landing_page_prompt(product_json):

    return f"""

Przygotuj strategię landing page dla produktu:

{product_json}


Wykorzystaj:

- problemy klientów
- rozwiązania
- transformacje
- benefity
- wyróżniki
- grupy docelowe
- obiekcje


Stwórz kompletną stronę sprzedażową.

"""



# ==========================================================
# PROMPT 2
# CRO OPTIMIZER
# ==========================================================


CRO_SYSTEM_PROMPT = """

Jesteś ekspertem CRO odpowiedzialnym za zwiększanie konwersji
w sklepach e-commerce.


Dostałeś gotową strategię strony produktu.

Twoim zadaniem jest znaleźć wszystkie elementy,
które mogą zwiększyć sprzedaż.


Nie przebudowujesz strony.

Dodajesz warstwę optymalizacji.


Przeanalizuj:


1. URGENCY

Dodaj:

- ograniczoną dostępność
- promocje czasowe
- countdown
- popularność produktu


Podaj:
- gdzie umieścić
- jaki tekst


------------------------------------------------


2. TRUST BUILDING

Dodaj:

- trust badges
- płatności
- dostawę
- gwarancję
- certyfikaty
- bezpieczeństwo


------------------------------------------------


3. SOCIAL PROOF

Dodaj:

- UGC
- opinie
- zdjęcia klientów
- liczby sprzedaży


------------------------------------------------


4. OBJECTION HANDLING

Znajdź:

- dlaczego klient może nie kupić
- jak rozwiać obiekcje


Dodaj:

- FAQ
- komunikaty


------------------------------------------------


5. AOV

Dodaj:

- bundle
- upsell
- cross sell
- dodatki


------------------------------------------------


6. CHATBOT

Zaproponuj:

- kiedy się pojawia
- jakie pytania obsługuje
- jakie komunikaty


------------------------------------------------


7. PSYCHOLOGIA SPRZEDAŻY

Dodaj:

- miejsca CTA
- sticky cart
- elementy zwiększające uwagę


Zwróć JSON.


FORMAT:

{
 "conversion_strategy": {

   "urgency":[],
   "trust":[],
   "social_proof":[],
   "objection_handling":[],
   "aov":[],
   "chatbot":[],
   "psychology":[]
 }

}

"""



def get_cro_prompt(
    landing_page_strategy,
    product_json
):

    return f"""

Produkt:

{product_json}


Aktualna strategia strony:

{landing_page_strategy}


Zoptymalizuj ją pod maksymalną konwersję.

"""



# ==========================================================
# MAIN HANDLER
# ==========================================================


def generate_landing_page_for_knowledge_v2_handler(
        knowledge_id: int
):

    container = Container()

    logger = container.logger()
    knowledge_service = container.knowledge_service()
    ollama_service = container.ollama_service()

    # ------------------------------------------
    # Pobranie danych produktu
    # ------------------------------------------
    assembled_knowledge_dto =  knowledge_service.get_knowledge_details_by_id(knowledge_id=knowledge_id)



    product_json = json.dumps(
        assembled_knowledge_dto.to_dict(),
        ensure_ascii=False,
        indent=2
    )


    logger.info(
        "Generating landing page strategy"
    )


    # ======================================================
    # STEP 1
    # LANDING PAGE STRATEGY
    # ======================================================


    landing_result = ollama_service.chat_llm(
        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=LANDING_PAGE_SYSTEM_PROMPT
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=get_landing_page_prompt(
                    product_json
                )
            )
        ]
    )


    landing_strategy_raw = (
        landing_result.content
    )


    try:

        landing_strategy = json.loads(
            landing_strategy_raw
        )

    except Exception:

        landing_strategy = {
            "raw_response":
                landing_strategy_raw
        }



    logger.info(
        "Landing strategy generated"
    )



    # ======================================================
    # STEP 2
    # CRO OPTIMIZATION
    # ======================================================


    cro_result = ollama_service.chat_llm(
        messages=[

            LlmOllamaMessage(
                role=OllamaMessageRole.SYSTEM,
                content=CRO_SYSTEM_PROMPT
            ),

            LlmOllamaMessage(
                role=OllamaMessageRole.USER,
                content=get_cro_prompt(
                    landing_strategy,
                    product_json
                )
            )

        ]
    )


    cro_raw = cro_result.content


    try:

        cro_strategy = json.loads(
            cro_raw
        )

    except Exception:

        cro_strategy = {
            "raw_response":
                cro_raw
        }



    logger.info(
        "CRO optimization generated"
    )



    # ======================================================
    # FINAL OUTPUT
    # ======================================================


    return {

        # "product": assembled_knowledge_dto.to_dict(),

        "landing_page_strategy":
            landing_strategy,

        "conversion_strategy":
            cro_strategy

    }