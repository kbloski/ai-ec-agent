# Application Flow

Dokument opisuje pełny przepływ aplikacji na podstawie faktycznie zarejestrowanych
endpointów w `api/routes/general_routes.py`. Każdy kolejny krok w łańcuchu wymaga
`id` obiektu wygenerowanego w kroku poprzednim — widać to po parametrach ścieżki
(`{knowledge_id}`, `{brand_marketing_id}`, itd.), które kumulują się przy kolejnych
generacjach.

## Skrócony przepływ

```
Offer
  └─ Knowledge (z Offer)
       ├─ Target audience (opcjonalnie, informacyjnie)
       ├─ Analysis → Checklist (opcjonalnie, walidacja/ocena knowledge)
       └─ Brand marketing
            └─ Marketing strategy
                 └─ Offer strategy
                      └─ Message strategy
                           ├─ Ad strategy
                           │    └─ Creative strategy
                           │         └─ Ad execution   (gotowa reklama)
                           ├─ UGC creatives             (gotowe kreacje UGC)
                           └─ Page strategy
                                └─ Page blueprint
                                     └─ Page content plan
                                          └─ Page copy   (gotowy tekst strony)
```

Od `Message strategy` w dół droga się rozgałęzia na dwa równoległe piony:
**reklamy wideo/ads** (Ad strategy → Creative strategy → Ad execution, oraz
osobno UGC creatives) i **strona sprzedażowa** (Page strategy → Page blueprint →
Page content plan → Page copy). Oba piony bazują na tym samym `message_strategy_id`
i mogą być generowane niezależnie od siebie.

---

## 1. Offer

Punkt wejścia — dane produktu/oferty.

| Akcja | Endpoint |
|---|---|
| Lista ofert | `GET /offers?page=` |
| Seed przykładowej pełnej oferty | `GET /offers/seed-full` |
| Szczegóły oferty | `GET /offers/{id}` |
| Sugestie uzupełnień do oferty (pain points, target audience) | `GET /offers/{id}/suggestions` |

`suggestions` generuje unikalne (nieduplikujące istniejących) propozycje `pain_points`
i `target_audience` jako `OfferInsight` ze statusem `suggested`.

## 2. Knowledge (z Offer)

Ustrukturyzowana wiedza o ofercie — podsumowanie, kategoria, propozycja wartości,
insighty (features, benefits, differentiators, strengths, limitations, itd.).

| Akcja | Endpoint |
|---|---|
| Wygeneruj knowledge dla oferty | `GET /offers/{id}/knowledges/generate` |
| Lista knowledge dla oferty | `GET /offers/{offer_id}/knowledges` |
| Szczegóły knowledge | `GET /knowledges/{knowledge_id}` |
| Sugestie uzupełnień knowledge (feature/benefit/differentiator/strength/limitation/additional_insight) | `GET /knowledges/{knowledge_id}/suggestions` *(obecnie wyłączone w routingu — handler istnieje: `suggest_offer_knowledge_data_handler`)* |

## 3. Target audience (opcjonalna gałąź od Knowledge)

Rozszerzenie grup odbiorców na bazie knowledge — nie jest wymagane do dalszych
kroków (marketing strategy itd. nie przyjmują `target_audience_id`).

| Akcja | Endpoint |
|---|---|
| Wygeneruj target audience | `GET /knowledges/{knowledge_id}/target-audiences/generate` |
| Lista target audience dla knowledge | `GET /knowledges/{knowledge_id}/target-audiences` |
| Podgląd pojedynczej grupy | `GET /target-audiences/{target_audience_id}` |

## 4. Analysis → Checklist (opcjonalna gałąź od Knowledge)

Służy do oceny/walidacji knowledge pytaniami analitycznymi i checklistą — również
nie jest wymagana do przejścia dalej w głównym łańcuchu strategii.

| Akcja | Endpoint |
|---|---|
| Szczegóły analizy | `GET /analysis/{analyse_id}` |
| Utwórz analizę dla knowledge | `GET /knowledges/{knowledge_id}/analysis/create` |
| Lista analiz dla knowledge | `GET /knowledges/{knowledge_id}/analysis` |
| Wygeneruj odpowiedzi na pytania analizy | `GET /knowledges/{knowledge_id}/analysis/{analyse_id}/answers/generate` |
| Szczegóły checklisty | `GET /checklists/{checklist_id}` |
| Utwórz checklistę dla analizy | `GET /knowledges/{knowledge_id}/analysis/{analysis_id}/checklists/create` |
| Wygeneruj checklistę | `GET /knowledges/{knowledge_id}/analysis/{analyse_id}/checklists/{checklist_id}/generate` |
| Lista checklist dla analizy | `GET /analysis/{analysis_id}/checklists` |

## 5. Brand marketing (start głównego łańcucha strategii)

Pierwszy krok głównej ścieżki, budowany bezpośrednio na `knowledge_id`.

| Akcja | Endpoint |
|---|---|
| Wygeneruj brand marketing | `GET /knowledges/{knowledge_id}/brand-marketing/generate` |
| Lista brand marketing dla knowledge | `GET /knowledges/{knowledge_id}/brand-marketing` |
| Szczegóły brand marketing | `GET /brand-marketing/{id}` |

## 6. Marketing strategy

| Akcja | Endpoint |
|---|---|
| Wygeneruj (wymaga `knowledge_id` + `brand_marketing_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_markeging_id}/marketing-strategy/generate` |
| Lista dla brand marketing | `GET /brand-marketing/{brand_marketing_id}/marketing-strategy` |
| Szczegóły | `GET /marketing-strategy/{id}` |

## 7. Offer strategy

| Akcja | Endpoint |
|---|---|
| Wygeneruj (wymaga `knowledge_id` + `brand_marketing_id` + `marketing_strategy_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/generate` |
| Lista dla marketing strategy | `GET /marketing-strategy/{marketing_strategy_id}/offer-strategy` |
| Szczegóły | `GET /offer-strategy/{id}` |

## 8. Message strategy

Ostatni wspólny krok przed rozgałęzieniem na ads i stronę.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (kumuluje całą ścieżkę: `knowledge_id`, `brand_marketing_id`, `marketing_strategy_id`, `offer_strategy_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/generate` |
| Lista dla offer strategy | `GET /offer-strategy/{offer_strategy_id}/message-strategy` |
| Szczegóły | `GET /message-strategy/{id}` |

---

## Gałąź A: Ads (reklamy wideo)

### 9a. Ad strategy

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `message_strategy_id`) | `.../message-strategy/{message_strategy_id}/ad-strategy/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/ad-strategy` |
| Szczegóły | `GET /ad-strategy/{id}` |

### 10a. Creative strategy

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `ad_strategy_id`) | `.../ad-strategy/{ad_strategy_id}/creative-strategy/generate` |
| Lista dla ad strategy | `GET /ad-strategy/{ad_strategy_id}/creative-strategy` |
| Szczegóły | `GET /creative-strategy/{id}` |

### 11a. Ad execution (finalna kreacja reklamowa)

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `creative_strategy_id`) | `.../creative-strategy/{creative_strategy_id}/ad-execution/generate` |
| Lista dla creative strategy | `GET /creative-strategy/{creative_strategy_id}/ad-execution` |
| Szczegóły | `GET /ad-execution/{id}` |

### Boczna gałąź od Message strategy: UGC creatives

Generowane równolegle do Ad strategy, bezpośrednio z `message_strategy_id` (nie
przechodzi przez ad-strategy/creative-strategy).

| Akcja | Endpoint |
|---|---|
| Wygeneruj | `.../message-strategy/{message_strategy_id}/ugc-creatives/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/ugc-creatives` |
| Szczegóły | `GET /ugc-creatives/{id}` |

### Starszy/równoległy moduł: Advertisement

Odrębny, prostszy generator kreacji reklamowych spinany bezpośrednio z `knowledge_id`
(z pominięciem brand-marketing/strategy chain) — persystuje `Advertisement`,
powiązane `Scene`/`AdvertisementScene` oraz `AdvertisementObjection`.
**Obecnie route jest zakomentowany** w `general_routes.py`, ale handler
(`knowledge_advertisement_generate_handler`) oraz stos DTO/repo/asembler istnieją
i są w pełni wpięte w DI.

---

## Gałąź B: Strona sprzedażowa (Page)

### 9b. Page strategy

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `message_strategy_id`) | `.../message-strategy/{message_strategy_id}/page-strategy/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/page-strategy` |
| Szczegóły | `GET /page-strategy/{id}` |

### 10b. Page blueprint

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_strategy_id`) | `.../page-strategy/{page_strategy_id}/page-blueprint/generate` |
| Lista dla page strategy | `GET /page-strategy/{page_strategy_id}/page-blueprint` |
| Szczegóły | `GET /page-blueprint/{id}` |

### 11b. Page content plan

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_blueprint_id`) | `.../page-blueprint/{page_blueprint_id}/page-content-plan/generate` |
| Lista dla page blueprint | `GET /page-blueprint/{page_blueprint_id}/page-content-plan` |
| Szczegóły | `GET /page-content-plan/{id}` |

### 12b. Page copy (finalny tekst strony)

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_content_plan_id`) | `.../page-content-plan/{page_content_plan_id}/page-copy/generate` |
| Lista dla page content plan | `GET /page-content-plan/{page_content_plan_id}/page-copy` |
| Szczegóły | `GET /page-copy/{id}` |

---

## Uwagi architektoniczne

- Każdy poziom łańcucha ma ten sam trójkowy zestaw endpointów: **`generate`**
  (LLM + zapis do bazy), **lista dla rodzica** (`GET /<parent>/{parent_id}/<zasob>`),
  **szczegóły po id** (`GET /<zasob>/{id}`) — konwencja spójna w całym projekcie.
- Ścieżki `generate` w dolnych piętrach łańcucha (od `marketing-strategy` w dół)
  kumulują w URL identyfikatory wszystkich przodków — endpoint zna pełną ścieżkę
  przodków, mimo że realnie potrzebuje tylko bezpośredniego rodzica do zapytania
  o dane; to celowa konwencja projektu, nie duplikacja przez pomyłkę.
- Wszystkie generacje idą przez `ollama_service` (lokalny model LLM) i zapisują
  wynik do bazy (SQLite, `Base.metadata.create_all()` — Alembic nie jest w tym
  repo faktycznie zainicjalizowany mimo że jest zależnością).
- Warstwy: `api/routes` (routing) → `application/handlers` ("kontrolery",
  budują własny `Container()`) → `application/services` / `application/assemblers`
  (logika + składanie DTO z dzieci) → `infrastructure/repositories` (SQLAlchemy) →
  `domain/models` (encje).
