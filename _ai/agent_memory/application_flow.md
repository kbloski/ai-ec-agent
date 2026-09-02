---
name: application-flow
description: Backend generation-chain flow (Offer → ... → Page Copy / Creative Execution) — non-obvious routing/handler behavior not visible from a single file.
metadata:
  type: project
---

Pełny, szczegółowy opis łańcucha (co dokładnie generuje LLM na każdym kroku, pełne
listy pól) jest utrzymywany w `APPLICATION_FLOW.md` w katalogu głównym projektu —
tam szukać przy pracy nad konkretnym krokiem generacji. Tutaj tylko fakty, które
nie wynikają z jednego pliku i łatwo je przeoczyć.

## Kształt łańcucha

```
Offer → Knowledge → Brand Marketing → Marketing Strategy → Offer Strategy → Message Strategy
                                                                                  ├─ Ad Strategy → Creative Strategy → Ad Execution (kontener) → Creative Execution (LLM, finalna reklama)
                                                                                  ├─ UGC Creatives (bezpośrednio z message_strategy_id)
                                                                                  └─ Page Strategy → Page Requirements (kontener) → Page Blueprint → Page Content Plan → Page Copy (LLM, finalny tekst)
```
Boczne, opcjonalne gałęzie od Knowledge: Target Audience, Analysis → Checklist.

## Nieoczywiste zachowania routingu (łatwo się pomylić)

- Endpointy `.../generate` przyjmują w URL **wyłącznie id bezpośredniego rodzica**,
  nie cały łańcuch przodków. Handler sam chodzi w górę po relacjach przez
  repozytoria, żeby odtworzyć kontekst (np. `generate_offer_strategy_handler(marketing_strategy_id)`
  sam dociąga `brand_marketing` i `knowledge`). Jedyny wyjątek: `marketing-strategy/generate`
  bierze dwa id (`knowledge_id` + `brand_markeging_id` — literówka w nazwie parametru
  jest częścią realnego kodu, nie błędem w tym dokumencie).
- Wzorzec "kontener bez LLM → generacja LLM" powtarza się dwa razy i łatwo go
  pominąć, szukając "gdzie generuje się finalna reklama/strona":
  - Ads: `AdExecution` (`.../ad-execution/create`, GET, bez LLM — tylko
    `creative_type`/`platform`/`format`) → `CreativeExecution`
    (`.../ad-execution/{id}/creative-execution/generate`, LLM, tu dopiero
    powstają sceny/hook/CTA).
  - Page: `PageRequirements` (`.../page-requirements/create`, bez LLM, lista
    wymaganych sekcji) → `PageBlueprint` (`.../page-requirements/{id}/page-blueprint/generate`,
    LLM). Blueprint bierze `page_requirements_id`, **nie** `page_strategy_id`.
- `GET /offers/{id}/suggestions` i `GET /knowledges/{knowledge_id}/suggestions`
  (starsze "sugestie uzupełnień") — pierwszy już nie istnieje w routingu
  (zastąpiony przez `POST /offers/{offer_id}/insights/generate` z body
  `{types: [...]}`), drugi nadal istnieje jako handler, ale route jest
  zakomentowany w `general_routes.py`.
- Stary, równoległy generator `Advertisement` (`knowledge_advertisement_generate_handler`,
  szybka ścieżka `knowledge_id` → gotowe reklamy z pominięciem całego łańcucha
  strategii) ma pełny stos DTO/repo/asembler gotowy i wpięty w DI, ale route
  jest zakomentowany. Jeśli ktoś prosi o "szybkie reklamy bez strategii" — to
  już istnieje, tylko trzeba odkomentować route, nie pisać od nowa.

## Fact/Review status (weryfikacja wygenerowanych danych)

`OfferInsight`, `KnowledgeInsight`, `TargetAudience` mają dwa niezależne pola
statusu ustawiane przez `POST /<zasob>/{id}/update`:
- `FactStatus` (VERIFIED/UNVERIFIED/DISPUTED) — domyślnie `UNVERIFIED` przy
  generacji.
- `ReviewStatus` (PENDING/APPROVED/REJECTED) — ręczny review przez człowieka.

Statyczne słowniki tych i innych enumów wystawione są jako lookup endpointy:
`/fact-statuses`, `/review-statuses`, `/ad-frameworks`, `/creative-angels`,
`/execution-styles`, `/platforms`, `/page-sections` — jeśli frontend potrzebuje
listy opcji do selecta, prawdopodobnie już jest gotowy endpoint.

## CRUD wzorzec

Prawie każdy zasób w łańcuchu ma komplet: `generate`/`create`, lista dla
rodzica, szczegóły po id, `POST /<zasob>/{id}/update` (zwykle
`{fields: {...}}` dict, ale Target Audience/Insighty/Page Requirements mają
własny typowany request model), oraz `GET /<zasob>/{id}/delete` (celowo `GET`
nie `DELETE`, oznaczone komentarzem `# DELETE in future` — nieukończona
migracja na właściwe metody HTTP, nie przeoczenie).
