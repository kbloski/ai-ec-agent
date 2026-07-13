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




import json
from typing import Dict, Any, List

from di.container import Container

from application.mappers.offer_knowledge_mapper import OfferKnowledgeMapper

from domain.models.ollama.llm_ollama_message import LlmOllamaMessage
from domain.enums.ollama_message_role import OllamaMessageRole


BASE_SYSTEM_PROMPT = """
You are an expert in e-commerce product analysis.

Your task is to analyze products in terms of their sales potential.
Think like an entrepreneur investing their own money into a product.

Rules:
1. Provide specific and factual answers.
2. Do not invent information that is not present in the data.
3. If information is missing, clearly state that fact.
4. Evaluate the product objectively.
5. Point out both advantages and risks.
6. Result values must be in polish
"""


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
    "Czy produkt posiada efekt WOW? Oceń, czy wyróżnia się na rynku i czy łatwo stworzyć atrakcyjne materiały reklamowe.",
    "Kim jest idealny klient tego produktu? Opisz grupę docelową, potrzeby, motywacje oraz zachowania zakupowe.",
    "Czy produkt dobrze prezentuje się wizualnie? Oceń potencjał sprzedaży poprzez zdjęcia i materiały video.",
    "Jaka powinna być cena sprzedaży produktu? Uwzględnij koszt zakupu + 15 zł dostawy + 20 zł reklamy + 15 zł marży.",
    "Czy produkt ma potencjał osiągnięcia dobrej rentowności?",
    "Czy produkt sprawia wrażenie wysokiej jakości?",
    "Jakie jest ryzyko reklamacji, zwrotów i niezadowolenia klientów?",
    "Czy produkt jest łatwy w logistyce?",
    "Czy produkt można sprzedawać cały rok? Oceń sezonowość.",
    "Czy klient może kupić produkt ponownie? Oceń potencjał dodatków i akcesoriów.",
    "Czy produkt wymaga elektroniki, specjalnej obsługi, certyfikatów lub zezwoleń?",
    "Oceń ogólny potencjał produktu w skali 1-10.",
    "Jakie są największe zalety produktu?",
    "Jakie są największe ryzyka sprzedaży tego produktu?",
    "Co należy poprawić przed rozpoczęciem sprzedaży?",
    "Czy rekomendujesz sprzedaż produktu? TAK/WARUNKOWO/NIE i dlaczego?"
]


def chunk_list(
    items: List[str],
    size: int
) -> List[List[str]]:

    return [
        items[i:i + size]
        for i in range(0, len(items), size)
    ]


def build_product_context_prompt(
    product_data: Dict[str, Any]
) -> str:

    return f"""
PRODUCT DATA:

{json.dumps(
    product_data,
    ensure_ascii=False,
    indent=2
)}

Analyze the product based on the data provided above.
Do not draw conclusions based on information that is not present in the data.
"""


def build_questions_prompt(
    questions: List[str]
) -> str:

    return f"""
ANALYSIS QUESTIONS:

{json.dumps(
    questions,
    ensure_ascii=False,
    indent=2
)}


Answer each question based only on the provided product data.

Return ONLY valid JSON:

[
    {{
        "question": "exact question text",
        "answer": "detailed answer"
    }}
]


Rules:
- Answer every question.
- Do not skip questions.
- Do not add markdown.
- Do not add any text outside JSON.
- If information is missing, state that clearly.
"""


def generate_knowledge_analysis_handler(
    knowledge_id: int
) -> Dict[str, Any]:

    container = Container()
    logger = container.logger()
    knowledge_repo = container.offer_knowledge_repository()
    knowledge_assembler = container.offer_knowledge_assembler()
    ollama_service = container.ollama_service()


    logger.info(f"Generating knowledge analysis for knowledge_id={knowledge_id}")

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


    question_batches = chunk_list(
        items=PRODUCT_ANALYSIS_QUESTIONS,
        size=10
    )

    logger.info(f"Split {len(PRODUCT_ANALYSIS_QUESTIONS)} questions into {len(question_batches)} batches")


    final_analysis = []


    for batch_index, batch in enumerate(question_batches, start=1):

        logger.info(f"Processing batch {batch_index}/{len(question_batches)} ({len(batch)} questions)")

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
                    questions=batch
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
Invalid JSON response from model:

{response.content}
"""
            )


        if not isinstance(batch_result, list):

            raise Exception(
                "Model response is not a list."
            )


        logger.info(f"Batch {batch_index}/{len(question_batches)} returned {len(batch_result)} answers")

        final_analysis.extend(
            batch_result
        )


    logger.info(f"Knowledge analysis completed for knowledge_id={knowledge_id}, total_answers={len(final_analysis)}")

    return {
        "product_id": knowledge_id,
        "analysis": final_analysis
    }