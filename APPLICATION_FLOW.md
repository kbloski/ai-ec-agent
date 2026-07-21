# Application Flow

Dokument opisuje pełny przepływ aplikacji na podstawie faktycznie zarejestrowanych
endpointów w `api/routes/general_routes.py`. Każdy kolejny krok w łańcuchu wymaga
`id` obiektu wygenerowanego w kroku poprzednim — widać to po parametrach ścieżki
(`{knowledge_id}`, `{brand_marketing_id}`, itd.), które kumulują się przy kolejnych
generacjach. Przy każdym kroku opisano: **co konkretnie generuje LLM** (jakie dane/pola),
**gdzie to się zapisuje** oraz **po co ten krok istnieje** w całym łańcuchu.

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

Ogólna logika całego łańcucha: każdy kolejny krok **zawęża i konkretyzuje** to, co
wygenerował poprzedni — od surowych danych o ofercie, przez strategię (dlaczego i
dla kogo), aż po gotowy, publikowalny tekst/scenariusz (co dokładnie napisać/nakręcić).
Wcześniejsze kroki celowo nie generują gotowych treści (copy, hasła, scenariusze) —
to zadanie ostatnich ogniw łańcucha (Page Copy, Ad Execution, UGC Creatives).

---

## 1. Offer

Punkt wejścia — dane produktu/oferty. Bez LLM, czysty CRUD/lista.

| Akcja | Endpoint | Co robi |
|---|---|---|
| Lista ofert | `GET /offers?page=` | Paginowana lista ofert z bazy — brak LLM. |
| Seed przykładowej pełnej oferty | `GET /offers/seed-full` | Wstawia przykładowe dane testowe. |
| Szczegóły oferty | `GET /offers/{id}` | Pojedyncza oferta. |
| Sugestie uzupełnień do oferty | `GET /offers/{id}/suggestions` | Generuje unikalne (nieduplikujące istniejących) propozycje `pain_points` i `target_audience` jako `OfferInsight` ze statusem `suggested` — dwa osobne wywołania LLM, każde z kontekstem uniqueness-constraint względem już istniejących insightów. Po co: pozwala użytkownikowi rozszerzyć surowe dane oferty o świeże kąty, zanim zbuduje się z nich Knowledge. |

## 2. Knowledge (z Offer)

**Co generuje:** ustrukturyzowaną wiedzę o ofercie — `OfferKnowledge`
(`offer_summary`, `category`, `value_proposition`) oraz zestaw `KnowledgeInsight`
(po jednym wierszu na insight, typy: `problem_solved`, `solution`, `transformation`,
`offer_component`, `feature`, `functional_benefit`, `emotional_benefit`,
`differentiator`, `strength`, `limitation`, `assumption`, `additional_insight`).
LLM ma za zadanie zrozumieć ofertę: co to jest, jaki problem rozwiązuje, jaką
transformację daje klientowi, z czego się składa, jakie ma cechy/korzyści
funkcjonalne i emocjonalne, czym różni się od alternatyw, jakie ma mocne i słabe
strony — celowo **bez** tworzenia person, reklam czy kampanii na tym etapie.

**Po co:** to pierwsza warstwa "wiedzy fundamentalnej" o produkcie, z której
korzystają wszystkie kolejne generatory w łańcuchu (audience, brand, marketing,
ads, strony) — nic dalej nie powstaje bez przejścia przez ten krok.

| Akcja | Endpoint |
|---|---|
| Wygeneruj knowledge dla oferty | `GET /offers/{id}/knowledges/generate` |
| Lista knowledge dla oferty | `GET /offers/{offer_id}/knowledges` |
| Szczegóły knowledge | `GET /knowledges/{knowledge_id}` |
| Sugestie uzupełnień knowledge | `GET /knowledges/{knowledge_id}/suggestions` *(obecnie wyłączone w routingu — handler `suggest_offer_knowledge_data_handler` istnieje i działa)*. Trzy pogrupowane wywołania LLM (features/benefits, positioning, additional_insights), każde z uniqueness-constraint względem istniejących insightów danego typu — dopisuje nowe `KnowledgeInsight` ze statusem `suggested`. Po co: pozwala douzupełnić wiedzę o produkcie bez ręcznego wymyślania kolejnych cech/różnicowników. |

## 3. Target audience (opcjonalna gałąź od Knowledge)

**Co generuje:** min. 3 realistyczne segmenty klientów (`TargetAudience`) —
pełny profil demograficzno-psychograficzny (`age_min/max`, `gender`, `location`,
`purchasing_power`, `lifestyles`, `values`), psychologia zakupu
(`awareness_level`, `price_sensitivity`, `research_level`, `decision_time`),
`pain_points`, `motivations`, `buying_triggers`, `objections`, gotowe
`message_angles` i `marketing_channels`, plus `score`/`confidence`. Pola
enumeryczne walidowane względem domenowych enumów. Generacja idzie z
uniqueness-constraint względem już istniejących person, by nie duplikować
segmentów.

**Po co:** rozbija ofertę na konkretne, gotowe pod targetowanie person klienta —
używane potencjalnie przy targetowaniu reklam, ale **nie jest wymagany** do
dalszych kroków głównego łańcucha (marketing/offer/message strategy nie przyjmują
`target_audience_id`) — to gałąź informacyjna/poglądowa.

| Akcja | Endpoint |
|---|---|
| Wygeneruj target audience | `GET /knowledges/{knowledge_id}/target-audiences/generate` |
| Lista target audience dla knowledge | `GET /knowledges/{knowledge_id}/target-audiences` |
| Podgląd pojedynczej grupy | `GET /target-audiences/{target_audience_id}` |

## 4. Analysis → Checklist (opcjonalna gałąź od Knowledge)

Służy do oceny/walidacji knowledge — czy w ogóle warto inwestować dalej w ten
produkt — zanim zbuduje się na nim całą strategię marketingową. Nie jest
wymagana do przejścia dalej w głównym łańcuchu strategii.

| Akcja | Endpoint | Co robi |
|---|---|---|
| Szczegóły analizy | `GET /analysis/{analyse_id}` | Podgląd. |
| Utwórz analizę dla knowledge | `GET /knowledges/{knowledge_id}/analysis/create` | Bez LLM — tworzy pusty rekord `Analysis` + join `KnowledgeAnalysis`, kontener na kolejne kroki. |
| Lista analiz dla knowledge | `GET /knowledges/{knowledge_id}/analysis` | Podgląd. |
| Wygeneruj odpowiedzi na pytania analizy | `GET /knowledges/{knowledge_id}/analysis/{analyse_id}/answers/generate` | LLM odpowiada (w paczkach po 10) na stałą listę pytań biznesowych, tworząc `AnalysisQuestion` (`question`, `answer`, `score`, `confidence`) — w roli przedsiębiorcy inwestującego własne pieniądze, oceniając obiektywnie potencjał sprzedażowy (zalety i ryzyka), bez zmyślania brakujących danych. Po co: strukturalna ocena opłacalności produktu pytanie-po-pytaniu. |
| Szczegóły checklisty | `GET /checklists/{checklist_id}` | Podgląd. |
| Utwórz checklistę dla analizy | `GET /knowledges/{knowledge_id}/analysis/{analysis_id}/checklists/create` | Bez LLM — tworzy pusty rekord `Checklist` + join `AnalysisChecklist`, kontener na zadania. |
| Wygeneruj checklistę | `GET /knowledges/{knowledge_id}/analysis/{analyse_id}/checklists/{checklist_id}/generate` | LLM generuje konkretne, gotowe do skopiowania zadania walidacji rynku pod polski rynek (`ChecklistItem`: `title`, `description`, `note`) — Google Trends, Meta Ads Library, TikTok Creative Center, marketplace'y (Amazon/AliExpress/Temu/eBay), analiza opinii klientów, social media — każde zadanie z realnymi frazami/hashtagami do wyszukania (10-15+), nie ogólnikami. Po co: daje użytkownikowi konkretny plan działania do ręcznej walidacji rynku przed dalszą inwestycją w produkt. |
| Lista checklist dla analizy | `GET /analysis/{analysis_id}/checklists` | Podgląd. |

## 5. Brand marketing (start głównego łańcucha strategii)

**Co generuje:** fundament marki (`BrandMarketing`) — nazwę, pozycjonowanie,
kategorię, konkurencyjne wyróżnienie, cel i obietnicę marki, osobowość i
wartości marki, głos/ton (także osobno dla social media i komunikacji z
klientem), tagline, USP, kluczowe komunikaty, docelowe postrzeganie i emocje,
skojarzenia z marką, pragnienia/lęki/obiekcje klienta, motywatory zakupowe,
historię marki wraz z narracją transformacji klienta, filary treści, kierunki
storytellingu/UGC, styl i kierunek wizualny oraz jasne "rób"/"nie rób" dla marki.
Świadomie **bez** reklam, kampanii, CTA czy konkretnych kreacji.

**Po co:** to pierwszy krok głównego łańcucha strategii, budowany bezpośrednio na
`knowledge_id` — ustala niezmienną tożsamość marki, z której muszą wynikać
wszystkie kolejne decyzje strategiczne (marketing, offer, message, ads, strony, UGC).

| Akcja | Endpoint |
|---|---|
| Wygeneruj brand marketing | `GET /knowledges/{knowledge_id}/brand-marketing/generate` |
| Lista brand marketing dla knowledge | `GET /knowledges/{knowledge_id}/brand-marketing` |
| Szczegóły brand marketing | `GET /brand-marketing/{id}` |

## 6. Marketing strategy

**Co generuje:** `MarketingStrategy` — cel marketingowy i strategię wzrostu,
priorytetyzację odbiorców (główni/drugorzędni + uzasadnienie i potencjał),
pełne mapowanie customer journey (awareness/consideration/conversion/retention),
role i strategie poszczególnych kanałów marketingowych, taktyki pozyskiwania i
budowania zaufania, strategię contentową (filary + cele treści), strategię
społeczności i współpracy z twórcami/influencerami, kierunki kampanii (nazwa/cel/
odbiorca/kąt strategiczny), taktyki konwersji i retencji, testowalne hipotezy
marketingowe oraz KPI. Świadomie **bez** reklam, nagłówków, tekstów sprzedażowych,
landing page'y czy maili.

**Po co:** definiuje warstwę go-to-market/strategii wzrostu, na podstawie której
budowane są dalej offer strategy, message strategy i ad strategy.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (wymaga `knowledge_id` + `brand_marketing_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_markeging_id}/marketing-strategy/generate` |
| Lista dla brand marketing | `GET /brand-marketing/{brand_marketing_id}/marketing-strategy` |
| Szczegóły | `GET /marketing-strategy/{id}` |

## 7. Offer strategy

**Co generuje:** `OfferStrategy` — odpowiedź na pytanie "jak zapakować produkt
w ofertę najbardziej atrakcyjną dla konkretnego klienta": nazwę i pozycjonowanie
oferty, główną propozycję wartości, główny problem klienta i mechanizm
rozwiązania, korzyść główną oraz drugorzędne/funkcjonalne/emocjonalne, strukturę
oferty i stos wartości (value stack), elementy redukcji ryzyka i budowania
zaufania, strategię cenową i pilności, obsługę obiekcji klienta, konkurencyjne
wyróżnienie oraz dźwignie konwersji. Świadomie **bez** reklam, nagłówków, tekstów,
landing page'y czy maili.

**Po co:** określa, jak "zapakować" produkt w konkretną, przekonującą ofertę —
fundament pod dalsze przekazy komunikacyjne (message strategy) i kreacje.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (wymaga `knowledge_id` + `brand_marketing_id` + `marketing_strategy_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/generate` |
| Lista dla marketing strategy | `GET /marketing-strategy/{marketing_strategy_id}/offer-strategy` |
| Szczegóły | `GET /offer-strategy/{id}` |

## 8. Message strategy

**Co generuje:** `MessageStrategy` — bank przekazu komunikacyjnego: core message
i message marki, główny oraz drugorzędne kąty komunikacyjne, komunikaty pod
konkretnych odbiorców, pain pointy i pragnienia klienta, komunikaty korzyści wraz
z mapowaniem cecha→korzyść, komunikaty obsługujące obiekcje i budujące zaufanie,
dowody (proof points), wyzwalacze emocjonalne i argumenty racjonalne, oraz banki
kątów reklamowych/contentowych/UGC. Świadomie **bez** gotowych reklam, nagłówków,
landing page'y czy tekstów maili.

**Po co:** to ostatni wspólny krok przed rozgałęzieniem na ads i stronę —
dostarcza gotowy do wykorzystania bank argumentów/kątów, z którego czerpią
zarówno generatory reklam (ad strategy, creative strategy, UGC), jak i strony
(page copy).

| Akcja | Endpoint |
|---|---|
| Wygeneruj (kumuluje całą ścieżkę: `knowledge_id`, `brand_marketing_id`, `marketing_strategy_id`, `offer_strategy_id`) | `GET /knowledges/{knowledge_id}/brand-marketing/{brand_marketing_id}/marketing-strategy/{marketing_strategy_id}/offer-strategy/{offer_strategy_id}/message-strategy/generate` |
| Lista dla offer strategy | `GET /offer-strategy/{offer_strategy_id}/message-strategy` |
| Szczegóły | `GET /message-strategy/{id}` |

---

## Gałąź A: Ads (reklamy wideo)

### 9a. Ad strategy

**Co generuje:** `AdStrategy` — odpowiedź na "jaką reklamę zrobić, dla kogo, z
jakim argumentem, w jakim formacie i dlaczego powinna zadziałać": cel biznesowy/
reklamowy i zdarzenie konwersji, etap customer journey odbiorcy, priorytetyzację
odbiorców z uzasadnieniem, kąty pod segment (pain point/pragnienie/trigger
zakupowy), kąty message (angle/problem/obietnica/obiekcja/wymagany dowód), kąty
ofertowe (mechanizm wartości/redukcja ryzyka), wysokopoziomowe koncepcje
kreatywne (nazwa/pomysł/na jakim kącie bazuje/dlaczego zadziała/rekomendowany
format/kierunek emocjonalny), rekomendowane formaty reklam (np. ugc_testimonial,
product_demo, comparison, founder_story, before_after, static_benefit_ad) oraz
hipotezy testowe A/B. Świadomie **bez** finalnego copy, nagłówków, scenariuszy
wideo czy promptów wizualnych.

**Po co:** przekłada strategię w konkretny, testowalny plan reklamowy —
konsumowany dalej przez Creative Strategy oraz UGC Creatives.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `message_strategy_id`) | `.../message-strategy/{message_strategy_id}/ad-strategy/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/ad-strategy` |
| Szczegóły | `GET /ad-strategy/{id}` |

### 10a. Creative strategy

**Co generuje:** `CreativeStrategy` — rozwija koncepcję z Ad Strategy w spójny
kierunek kreatywny: cel, typ kreacji (wideo/statyczna/karuzela/ugc),
rekomendowany format, segment docelowy, "wielką ideę" (creative big idea), kąt
komunikacyjny, strategię hooka (typ/cel/kierunek), narracyjny framework
(np. problem→eskalacja→rozwiązanie), kierunek wizualny/stylistyczny, strategię
"mówcy" (kto mówi, jakim tonem/w jakiej roli), sekwencję emocji w reklamie,
wymaganą strategię dowodów/social proof oraz wytyczne produkcyjne. Świadomie
**bez** gotowego scenariusza, dialogów, grafik czy promptów AI.

**Po co:** rozwija wybraną koncepcję z Ad Strategy w pełny kierunek kreatywny,
gotowy do przełożenia na konkretną, "kręcalną" egzekucję (Ad Execution).

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `ad_strategy_id`) | `.../ad-strategy/{ad_strategy_id}/creative-strategy/generate` |
| Lista dla ad strategy | `GET /ad-strategy/{ad_strategy_id}/creative-strategy` |
| Szczegóły | `GET /creative-strategy/{id}` |

### 11a. Ad execution (finalna kreacja reklamowa)

**Co generuje:** `AdExecution` — precyzyjny, gotowy do realizacji blueprint
reklamy wideo: platforma/format/placement/czas trwania/proporcje, strategia
hooka, oś czasu sekcji hook→problem→solution→proof→offer→cta (każda z nazwą,
zakresem sekund, celem i emocją), pełny podział na sceny (kolejność, sekcja,
czas trwania, cel, opis wizualny, wskazówki kamery, voiceover, dialogi, teksty
na ekranie, emocja per scena), wymagane materiały produkcyjne (nagrania, ujęcia
produktu, testimoniale, screenshoty, animacje), notatki produkcyjne oraz
szczegóły CTA. Handler waliduje, że suma czasu trwania scen dokładnie odpowiada
zadanej długości reklamy (inaczej zwraca błąd). Świadomie **nie** jest
dokumentem strategicznym ani nie generuje grafik/wideo/promptów AI.

**Po co:** to finalny, produkcyjny shot-list reklamy, który ekipa
produkcyjna/generator zasobów może wykonać wprost — koniec pionu reklamowego.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `creative_strategy_id`) | `.../creative-strategy/{creative_strategy_id}/ad-execution/generate` |
| Lista dla creative strategy | `GET /creative-strategy/{creative_strategy_id}/ad-execution` |
| Szczegóły | `GET /ad-execution/{id}` |

### Boczna gałąź od Message strategy: UGC creatives

**Co generuje:** `UgcCreative` — pomysły na autentycznie wyglądający content
UGC nagrywany "przez klienta" (nie polerowaną reklamę): personę klienta (typ/
sytuacja/problem/dlaczego ta osoba działa), format treści (recenzja selfie,
unboxing, before/after, problem→rozwiązanie itd.), kąt treści, naturalny
(nienachalny) pomysł na hook, wysokopoziomowy przebieg wideo (etapy typu "pokaż
problem" → "pokaż produkt" → "pierwsze użycie" → "efekt" → "opinia", bez
pełnego scenariusza), styl nagrania (z ręki, naturalne światło, bez polishu),
dopasowanie do platform (TikTok/Reels/Stories), miękkie CTA oraz uzasadnienie
psychologiczne, dlaczego powinno zadziałać. Generacja z uniqueness-constraint
względem istniejących UGC dla danej message strategy.

**Po co:** generowana równolegle do Ad Strategy, bezpośrednio z
`message_strategy_id` (bez przechodzenia przez ad-strategy/creative-strategy) —
dostarcza pulę naturalnych, "organicznych" koncepcji treści pod social/creator
marketing, odrębnych od dopracowanych scenariuszy Ad Execution.

| Akcja | Endpoint |
|---|---|
| Wygeneruj | `.../message-strategy/{message_strategy_id}/ugc-creatives/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/ugc-creatives` |
| Szczegóły | `GET /ugc-creatives/{id}` |

### Starszy/równoległy moduł: Advertisement

**Co generuje:** `count` gotowych, różnych kreacji reklamowych naraz —
framework, kąt psychologiczny, hook (tekst/typ/wizualnie/czas trwania), problem,
rozwiązanie, dowód (typ/treść), scenariusz w scenach, voiceover, kierunki
wizualne i teksty nakładkowe, dane grupy docelowej, obiekcje wraz z odpowiedziami
oraz oceny (hook/emocje/klarowność/intencja zakupu/ogólna) — persystowane jako
`Advertisement` + powiązane `Scene`/`AdvertisementScene` oraz
`AdvertisementObjection`.

**Po co:** to odrębny, prostszy generator kreacji reklamowych spinany
bezpośrednio z `knowledge_id`, z pominięciem całego łańcucha brand-marketing/
strategy — szybka ścieżka "od razu do gotowych reklam" bez przechodzenia przez
warstwy strategiczne. **Obecnie route jest zakomentowany** w `general_routes.py`,
ale handler (`knowledge_advertisement_generate_handler`) oraz stos DTO/repo/
asembler istnieją i są w pełni wpięte w DI.

---

## Gałąź B: Strona sprzedażowa (Page)

### 9b. Page strategy

**Co generuje:** `PageStrategy` — *dlaczego* strona ma istnieć i dla kogo, bez
żadnej struktury ani treści: cel strony, akcję konwersji, grupę docelową, jej
poziom świadomości i etap customer journey, główną propozycję wartości, główny
przekaz i kąt komunikacyjny, problem i pragnienie klienta, wyzwalacze
emocjonalne i racjonalne, motywatory i bariery zakupowe, obiekcje do
rozwiązania, wymagania zaufania, pozycjonowanie konkurencyjne, kierunek głosu
marki oraz strategię konwersji (główne/drugorzędne czynniki decyzyjne) i
strategię per etap customer journey.

**Po co:** ustala strategiczne uzasadnienie strony (kto, dlaczego, jaka
logika konwersji), z którego korzystają dalej Page Blueprint, Content Plan i Copy.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `message_strategy_id`) | `.../message-strategy/{message_strategy_id}/page-strategy/generate` |
| Lista dla message strategy | `GET /message-strategy/{message_strategy_id}/page-strategy` |
| Szczegóły | `GET /page-strategy/{id}` |

### 10b. Page blueprint

**Co generuje:** `PageBlueprint` — strukturę strony (bez treści): listę sekcji
w kolejności, każda z typem sekcji, priorytetem (wymagana/opcjonalna), celem,
etapem customer journey, rolą konwersyjną, celem psychologicznym, wymaganymi
elementami, elementami dowodowymi, obiekcjami, które adresuje, i notatkami.
Typy sekcji wybierane ze stałego słownika (core: hero, problem, solution,
benefits, features, how_it_works, social_proof, offer, risk_reversal, faq,
final_cta; opcjonalne: product_showcase, comparison, testimonials, before_after,
unique_mechanism, bonus_stack, urgency, pricing) — handler waliduje każdy
`section_type` względem dozwolonej listy i odrzuca nieznane wartości.

**Po co:** definiuje architekturę informacyjną/kolejność sekcji strony, którą
Content Plan i Copy dalej wypełniają treścią.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_strategy_id`) | `.../page-strategy/{page_strategy_id}/page-blueprint/generate` |
| Lista dla page strategy | `GET /page-strategy/{page_strategy_id}/page-blueprint` |
| Szczegóły | `GET /page-blueprint/{id}` |

### 11b. Page content plan

**Co generuje:** `PageContentPlan` — dla każdej sekcji z Page Blueprint (1:1,
bez dodawania/usuwania sekcji) określa, jaka treść i argumentacja ma się w niej
znaleźć: cel treści, pytanie klienta, na które sekcja odpowiada, stan
psychologiczny klienta w tym momencie, kierunek przekazu, kluczowe elementy i
argumenty, punkty emocjonalne i racjonalne, wymagane dowody, adresowane
obiekcje, rolę CTA oraz potrzebne wsparcie wizualne — wciąż bez finalnego tekstu.

**Po co:** łączy strukturę (Blueprint) z finalnym tekstem (Copy), precyzując
dokładnie jaki argument ma nieść każda sekcja, zanim padnie ostateczny tekst.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_blueprint_id`) | `.../page-blueprint/{page_blueprint_id}/page-content-plan/generate` |
| Lista dla page blueprint | `GET /page-blueprint/{page_blueprint_id}/page-content-plan` |
| Szczegóły | `GET /page-content-plan/{id}` |

### 12b. Page copy (finalny tekst strony)

**Co generuje:** `PageCopy` — finalną warstwę tekstową strony. Dla każdej
sekcji z Content Plan (ta sama kolejność, bez zmian w liście sekcji) pisze
realny nagłówek, podnagłówek, treść główną, punkty wypunktowane, bloki treści
specyficzne dla typu sekcji (np. `benefit` — tytuł/opis, `faq_item` —
pytanie/odpowiedź, `offer_card` — nazwa/cena/zawartość/CTA, `comparison_row`
itd.), tekst CTA oraz tekst wspierający — w oparciu wyłącznie o wcześniejszy
kontekst strategiczny, unikając pustych sloganów marketingowych ("najlepszy
produkt", "rewolucyjny" itp.).

**Po co:** to ostatnie ogniwo pionu strony — gotowy do publikacji tekst
konsumowany bezpośrednio przez frontend/renderer strony.

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
- Widoczny wzorzec "od strategii do treści": kroki 5-8 (Brand/Marketing/Offer/
  Message strategy) świadomie **nie generują żadnej gotowej treści** (bez
  nagłówków, CTA, scenariuszy) — dopiero ostatnie ogniwa każdej gałęzi
  (Ad Execution, UGC Creatives, Page Copy) produkują tekst gotowy do publikacji.
  To rozdzielenie pozwala tej samej strategii zasilać wiele różnych egzekucji
  (np. wiele wariantów Ad Execution z jednej Creative Strategy).
- Wszystkie generacje idą przez `ollama_service` (lokalny model LLM) i zapisują
  wynik do bazy (SQLite, `Base.metadata.create_all()` — Alembic nie jest w tym
  repo faktycznie zainicjalizowany mimo że jest zależnością).
- Warstwy: `api/routes` (routing) → `application/handlers` ("kontrolery",
  budują własny `Container()`) → `application/services` / `application/assemblers`
  (logika + składanie DTO z dzieci) → `infrastructure/repositories` (SQLAlchemy) →
  `domain/models` (encje).
