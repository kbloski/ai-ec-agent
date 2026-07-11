import json
from di.container import Container
from application.mappers.offer_mapper import OfferMapper
from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole
from infrastructure.ai.prompts.constraints.uniqueness_prompt import build_uniqueness_constraint_prompt  

def get_system_prompt(offer_data: str):
    SYSTEM_PROMPT = f"""
You are an expert in e-commerce strategy, product marketing, and consumer psychology.
You specialize in product analysis, customer behavior, buying motivations, and creating effective sales arguments.

You think like an experienced marketer and market analyst: you look for hidden customer needs, purchase drivers, problems, objections, and opportunities to increase product attractiveness.

You base your conclusions on available data, analyze products from the customer's perspective, and clearly distinguish facts from assumptions. Your goal is to provide practical business insights that can help improve product positioning, marketing communication, and sales performance.

Currently analyzed product:

```json
{offer_data}"""





PAIN_POINTS_PROMPT = """
Przeanalizuj produkt i zidentyfikuj realistyczne problemy klientów, które ten produkt rozwiązuje.

Najpierw zrozum produkt:
- jakie zadanie pomaga wykonać,
- jakie niedogodności usuwa,
- jakie trudności zmniejsza,
- jakie istniejące metody lub narzędzia może usprawnić.

Wygeneruj punkty bólu na podstawie realnych sytuacji, w których klient potrzebowałby tego produktu.

Zasady:
- Trzymaj się rzeczywistego przeznaczenia i możliwości produktu.
- Nie wymyślaj całkowicie nowych rynków ani niezwiązanych zastosowań.
- Nie zakładaj profesjonalnego zastosowania, jeśli produkt wyraźnie go nie wspiera.
- Nie twórz problemów, które nie mają bezpośredniego związku z produktem.
- Nie opisuj cech produktu, jego zalet ani korzyści marketingowych.
- Opisuj sytuację klienta przed zakupem produktu.
- Skup się na frustracji, trudnościach, stracie czasu, wysiłku, niedogodnościach lub ograniczeniach.

Istniejące punkty bólu traktuj jako kontekst. Rozwijaj je i uzupełniaj, ale nie kopiuj ich bezmyślnie.

Zwróć wyłącznie poprawną tablicę JSON zawierającą stringi.

Wygeneruj kilka realistycznych punktów bólu klientów.
"""



TARGET_AUDIENCE_PROMPT = """
Przeanalizuj produkt i rozszerz istniejącą grupę docelową o dodatkowe realistyczne grupy klientów.

Znajdź osoby, które naturalnie mogłyby kupić ten produkt, ponieważ mają podobną potrzebę lub problem.

Oprzyj analizę na:
- obecnej grupie docelowej,
- przeznaczeniu produktu,
- sytuacjach użycia produktu,
- problemach klientów.

Zasady:
- Trzymaj się obecnego pozycjonowania produktu.
- Nie szukaj całkowicie nowych rynków.
- Nie twórz mało prawdopodobnych grup zawodowych, jeśli produkt nie pasuje do ich potrzeb.
- Nie używaj szerokich grup typu "wszyscy", "ludzie", "klienci".
- Każda grupa odbiorców musi mieć konkretny powód, aby kupić ten produkt.
- Skup się na praktycznych grupach klientów przydatnych w komunikacji marketingowej.
- Nie powtarzaj istniejących grup odbiorców.

Zwróć wyłącznie poprawną tablicę JSON zawierającą stringi.

Wygeneruj kilka dodatkowych segmentów klientów.
"""



def suggets_offer_data_handler(offer_id : int):
    container = Container()
    offer_repository = container.offers_repository()
    offer_assembler = container.offer_assembler()
    ollama_service  = container.ollama_service()

    offer_db = offer_repository.get_by_id(id=offer_id)
    offer_dto = OfferMapper.to_dto(item=offer_db)
    offer_assembled = offer_assembler.assemble_dto(item=offer_dto)

    # ---------------------------------------
    # PAIN POINTS
    # ---------------------------------------

    messages = [
        LlmOllamaMessage(
            role = OllamaMessageRole.SYSTEM,
            content = get_system_prompt(offer_assembled.to_dict())
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=build_uniqueness_constraint_prompt( json.dumps(offer_assembled.pain_points))
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=PAIN_POINTS_PROMPT
        )
    ]

    response_pain_points = ollama_service.chat_llm(messages=messages)
    new_pain_points_arr = json.loads(response_pain_points.content)
    updated_pain_points = offer_assembled.pain_points + new_pain_points_arr
    offer_db.pain_points = updated_pain_points
    offer_assembled.pain_points = updated_pain_points

    # ---------------------------------------
    # Target audience
    # ---------------------------------------

    messages = [
        LlmOllamaMessage(
            role = OllamaMessageRole.SYSTEM,
            content = get_system_prompt(offer_assembled.to_dict())
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=build_uniqueness_constraint_prompt( json.dumps(offer_assembled.target_audience))
        ),
        LlmOllamaMessage(
            role=OllamaMessageRole.USER,
            content=TARGET_AUDIENCE_PROMPT
        )
    ]

    response_target_audience = ollama_service.chat_llm(messages=messages)
    new_targets_audience = json.loads(response_target_audience.content)
    updated_target_audience = offer_assembled.target_audience + new_targets_audience
    offer_db.target_audience = updated_target_audience
    offer_assembled.target_audience = updated_target_audience

    offer_repository.update( item = offer_db)

    return offer_assembled