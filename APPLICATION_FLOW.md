# Application Flow

> Zaktualizowano na podstawie faktycznego stanu `api/routes/general_routes.py` oraz
> handlerów w `application/handlers/*` (weryfikacja: 2026-09-02). Poprzednia wersja
> tego dokumentu była nieaktualna w kilku miejscach — patrz `_ai/agent_memory/application_flow.md`
> dla skróconej wersji na potrzeby pamięci agenta.

Dokument opisuje pełny przepływ aplikacji na podstawie faktycznie zarejestrowanych
endpointów w `api/routes/general_routes.py`. Każdy kolejny krok w łańcuchu wymaga
`id` obiektu wygenerowanego w kroku poprzednim. Przy każdym kroku opisano: **co
konkretnie generuje LLM** (jakie dane/pola), **gdzie to się zapisuje** oraz **po co
ten krok istnieje** w całym łańcuchu.

**Ważne:** generatory (`.../generate` handlery) przyjmują w URL wyłącznie **id
bezpośredniego rodzica** — dawniej (i w części dokumentacji) sugerowano, że URL
kumuluje id wszystkich przodków. To nieprawda dla generatorów niżej w łańcuchu:
`offer-strategy/generate` bierze tylko `marketing_strategy_id`, `message-strategy/generate`
tylko `offer_strategy_id`. Handler sam odtwarza pełny kontekst przodków, chodząc w
górę po relacjach (`marketing_strategy → brand_marketing → knowledge` itd.) przez
repozytoria. Jedynym wyjątkiem jest `marketing-strategy/generate`, który w URL
nadal przyjmuje dwa id: `knowledge_id` i `brand_markeging_id` (celowo, bo
`brand_marketing` samo w sobie nie przechowuje `knowledge_id` w ścieżce URL-a).

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
                           │         └─ Ad execution (kontener, bez LLM)
                           │              └─ Creative execution   (gotowa reklama)
                           ├─ UGC creatives             (gotowe kreacje UGC)
                           └─ Page strategy
                                └─ Page requirements (kontener, bez LLM)
                                     └─ Page blueprint
                                          └─ Page content plan
                                               └─ Page copy   (gotowy tekst strony)
```

Od `Message strategy` w dół droga się rozgałęzia na dwa równoległe piony:
**reklamy wideo/ads** (Ad strategy → Creative strategy → Ad execution → Creative
execution, oraz osobno UGC creatives) i **strona sprzedażowa** (Page strategy →
Page requirements → Page blueprint → Page content plan → Page copy). Oba piony
bazują na tym samym `message_strategy_id` i mogą być generowane niezależnie od siebie.

Wzdłuż obu pionów pojawia się ten sam wzorzec: krok "strategia" (LLM) → krok
"kontener/wymagania" (**bez LLM**, czysty CRUD, ustawia parametry wejściowe: format
reklamy/platformę dla Ad Execution, wymagane sekcje dla Page Requirements) → krok
finalnej generacji (LLM, korzysta z kontenera jako doprecyzowania).

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
| Utwórz ofertę | `GET /offers/create` | Bez LLM. |
| Seed przykładowej pełnej oferty | `GET /offers/seed-full` | Wstawia przykładowe dane testowe. |
| Szczegóły oferty | `GET /offers/{id}` | Pojedyncza oferta. |
| Edytuj pola oferty | `POST /offers/{id}/update` | Bez LLM. |
| Wygeneruj insighty do oferty | `POST /offers/{offer_id}/insights/generate` (body: `{types: [OfferInsightType, ...]}`) | Generuje `OfferInsight` dla wskazanych typów (`fact_status=UNVERIFIED` domyślnie) — zastąpiło starsze `GET /offers/{id}/suggestions` z wcześniejszej wersji tego dokumentu (ten endpoint już nie istnieje). Po co: pozwala użytkownikowi rozszerzyć surowe dane oferty o insighty, zanim zbuduje się z nich Knowledge. |
| Szczegóły / edycja insightu oferty | `GET /offer-insights/{id}`, `POST /offer-insights/{id}/update` (`fact_status`, `review_status`) | Ręczna weryfikacja wygenerowanego insightu. |
| Pozycje oferty (Offer Items) | `POST /offers/{offer_id}/items` (create), `GET /offer-items/{id}`, `POST /offer-items/{id}/update` | Bez LLM — CRUD produktów/pozycji wchodzących w skład oferty. |

## 2. Knowledge (z Offer)

**Co generuje:** ustrukturyzowaną wiedzę o ofercie — `Knowledge`
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
| Edytuj pola knowledge | `POST /knowledges/{id}/update` |
| Szczegóły / edycja insightu knowledge (ręczna weryfikacja, patrz "Workflow weryfikacji" niżej) | `GET /knowledge-insights/{id}`, `POST /knowledge-insights/{id}/update` (`fact_status`, `review_status`) |
| Sugestie uzupełnień knowledge | `GET /knowledges/{knowledge_id}/suggestions` *(nadal zakomentowane w routingu — handler `suggest_knowledge_data_handler` istnieje, ale route wyłączony)*. Trzy pogrupowane wywołania LLM (features/benefits, positioning, additional_insights), każde z uniqueness-constraint względem istniejących insightów danego typu — dopisuje nowe `KnowledgeInsight` ze statusem `suggested`. Po co: pozwala douzupełnić wiedzę o produkcie bez ręcznego wymyślania kolejnych cech/różnicowników. |

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
| Wygeneruj (tylko `marketing_strategy_id` — kontekst przodków handler odtwarza sam) | `GET /marketing-strategy/{marketing_strategy_id}/offer-strategy/generate` |
| Lista dla marketing strategy | `GET /marketing-strategy/{marketing_strategy_id}/offer-strategy` |
| Szczegóły | `GET /offer-strategy/{id}` |
| Edytuj pola | `POST /offer-strategy/{id}/update` |

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
| Wygeneruj (tylko `offer_strategy_id`) | `GET /offer-strategy/{offer_strategy_id}/message-strategy/generate` |
| Lista dla offer strategy | `GET /offer-strategy/{offer_strategy_id}/message-strategy` |
| Szczegóły | `GET /message-strategy/{id}` |
| Edytuj pola | `POST /message-strategy/{id}/update` |

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

### 11a. Ad execution (kontener, bez LLM)

**Co robi:** tworzy pusty rekord `AdExecution` — kontener/parametryzację pod
konkretną egzekucję: `creative_strategy_id`, `name`, `creative_type` (np.
video/image/carousel), `platform`, `format`, `is_favorite`. **Nie wywołuje LLM** —
to czysty CRUD, analogiczny do "Analysis"/"Checklist create" i do "Page requirements"
w pionie strony.

**Po co:** pozwala z jednej Creative Strategy stworzyć wiele niezależnych
egzekucji (różne platformy/formaty/typy kreacji), z których każda dostaje
osobną generację w kroku Creative Execution.

| Akcja | Endpoint | Co robi |
|---|---|---|
| Utwórz (+ `creative_strategy_id`, `creative_type`, `platform`, `format`, opcjonalnie `name`) | `GET /creative-strategy/{creative_strategy_id}/ad-execution/create` | Bez LLM. |
| Lista dla creative strategy | `GET /creative-strategy/{creative_strategy_id}/ad-execution` | Podgląd. |
| Szczegóły | `GET /ad-execution/{id}` | Podgląd. |
| Edytuj pola | `POST /ad-execution/{id}/update` | Bez LLM. |

### 12a. Creative execution (finalna kreacja reklamowa)

**Co generuje:** `CreativeExecution` — precyzyjny, gotowy do realizacji blueprint
reklamy, zapisany jako `content_json` powiązany z `ad_execution_id`. Handler
odtwarza pełny kontekst przodków (`ad_execution → creative_strategy → ad_strategy →
message_strategy → offer_strategy → marketing_strategy → brand_marketing → knowledge`),
opcjonalnie doprecyzowuje generację o `ad_framework_id`/`creative_angle_id`/
`execution_style_id` (statyczne słowniki, patrz "Ad frameworks / Creative angels /
Execution styles" niżej) oraz `duration_seconds`/`number_of_slides`, i wybiera
prompt zależnie od `creative_type` z Ad Execution. Dla wideo: `creative_thesis`,
strategia hooka, `structure`, pełny podział na sceny (kolejność, sekcja, zakres
sekund, opis wizualny, voiceover, dialogi, teksty na ekranie), notatki
produkcyjne. Świadomie **nie** generuje grafik/wideo/promptów AI, tylko blueprint
tekstowy.

**Po co:** to finalny, produkcyjny shot-list reklamy — koniec pionu reklamowego.
Rozdzielenie na Ad Execution (kontener) + Creative Execution (LLM) pozwala
wygenerować/regenerować wiele wariantów egzekucji dla tych samych parametrów
kontenera.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `ad_execution_id`, opcjonalnie `duration_seconds`, `number_of_slides`, `ad_framework_id`, `creative_angle_id`, `execution_style_id`) | `GET /ad-execution/{ad_execution_id}/creative-execution/generate` |
| Lista dla ad execution | `GET /ad-execution/{ad_execution_id}/creative-execution` |
| Szczegóły | `GET /creative-execution/{id}` |
| Edytuj pola | `POST /creative-execution/{id}/update` |

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

### 10b. Page requirements (kontener, bez LLM)

**Co robi:** tworzy pusty rekord `PageRequirements` (`page_strategy_id`,
`is_favorite`) — kontener na listę wymaganych sekcji strony. Sama lista sekcji
to osobne rekordy `PageSectionRequirement` (`page_requirements_id`,
`page_section_type_id`, `requirement_type`, `position`), nadpisywane w całości
przez `update` (`replace_for_page_requirements`). Typy sekcji pochodzą ze
stałego słownika (`GET /page-sections`, patrz niżej). **Bez LLM.**

**Po co:** pozwala użytkownikowi ręcznie ustalić/dostosować wymaganą strukturę
strony (które sekcje muszą/mogą się pojawić, w jakiej kolejności) **przed**
wygenerowaniem Page Blueprint — Blueprint generuje się już z tym ograniczeniem
jako inputem, a nie generuje struktury w pełni od zera.

| Akcja | Endpoint | Co robi |
|---|---|---|
| Utwórz (+ `page_strategy_id`) | `GET /page-strategy/{page_strategy_id}/page-requirements/create` | Bez LLM. |
| Lista dla page strategy | `GET /page-strategy/{page_strategy_id}/page-requirements` | Podgląd. |
| Szczegóły | `GET /page-requirements/{id}` | Podgląd. |
| Ustaw listę sekcji | `POST /page-requirements/{id}/update` (body: `section_requirements: [{page_section_type_id, requirement_type, position}]`) | Bez LLM, nadpisuje całą listę. |

### 11b. Page blueprint

**Co generuje:** `PageBlueprint` — strukturę strony (bez treści): listę sekcji
w kolejności, każda z typem sekcji, priorytetem (wymagana/opcjonalna), celem,
etapem customer journey, rolą konwersyjną, celem psychologicznym, wymaganymi
elementami, elementami dowodowymi, obiekcjami, które adresuje, i notatkami.
Typy sekcji wybierane ze stałego słownika (core: hero, problem, solution,
benefits, features, how_it_works, social_proof, offer, risk_reversal, faq,
final_cta; opcjonalne: product_showcase, comparison, testimonials, before_after,
unique_mechanism, bonus_stack, urgency, pricing) — handler waliduje każdy
`section_type` względem dozwolonej listy i odrzuca nieznane wartości. Wejściem
jest `page_requirements_id` (nie `page_strategy_id` bezpośrednio) — handler
odtwarza kontekst przodków samodzielnie: `page_requirements → page_strategy →
message_strategy → offer_strategy → marketing_strategy → brand_marketing → knowledge`.
Zapisany rekord przechowuje zarówno `page_strategy_id`, jak i `page_requirements_id`.

**Po co:** definiuje architekturę informacyjną/kolejność sekcji strony, którą
Content Plan i Copy dalej wypełniają treścią, respektując ograniczenia z Page
Requirements.

| Akcja | Endpoint |
|---|---|
| Wygeneruj (+ `page_requirements_id`) | `GET /page-requirements/{page_requirements_id}/page-blueprint/generate` |
| Lista dla page requirements | `GET /page-requirements/{page_requirements_id}/page-blueprint` |
| Szczegóły | `GET /page-blueprint/{id}` |
| Edytuj pola | `POST /page-blueprint/{id}/update` |

### 12b. Page content plan

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
| Wygeneruj (+ `page_blueprint_id`) | `GET /page-blueprint/{page_blueprint_id}/page-content-plan/generate` |
| Lista dla page blueprint | `GET /page-blueprint/{page_blueprint_id}/page-content-plan` |
| Szczegóły | `GET /page-content-plan/{id}` |
| Edytuj pola | `POST /page-content-plan/{id}/update` |

### 13b. Page copy (finalny tekst strony)

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
| Wygeneruj (+ `page_content_plan_id`) | `GET /page-content-plan/{page_content_plan_id}/page-copy/generate` |
| Lista dla page content plan | `GET /page-content-plan/{page_content_plan_id}/page-copy` |
| Szczegóły | `GET /page-copy/{id}` |
| Edytuj pola | `POST /page-copy/{id}/update` |

---

## Statyczne słowniki / lookupy

Kilka endpointów nie dotyczy żadnego konkretnego rekordu w łańcuchu — zwracają
stałe listy (JSON w `infrastructure/ads/*.json` lub domenowe enumy), używane jako
opcje w UI i/lub jako opcjonalny kontekst doprecyzowujący generację (np. w
Creative Execution):

| Endpoint | Co zwraca |
|---|---|
| `GET /ad-frameworks` | Lista dostępnych frameworków reklamowych (statyczny JSON). |
| `GET /creative-angels` | Lista kątów kreatywnych (statyczny JSON). |
| `GET /execution-styles` | Lista stylów egzekucji (statyczny JSON). |
| `GET /platforms` | Lista obsługiwanych platform reklamowych. |
| `GET /page-sections` | Lista typów sekcji strony (używana m.in. przy Page Requirements). |
| `GET /fact-statuses` | Wartości enuma `FactStatus`. |
| `GET /review-statuses` | Wartości enuma `ReviewStatus`. |

## Workflow weryfikacji wygenerowanych faktów (fact/review status)

Insighty generowane przez LLM (`OfferInsight`, `KnowledgeInsight`, a analogicznie
pola `TargetAudience`) mają dwa niezależne statusy do ręcznej weryfikacji przez
użytkownika, ustawiane przez `POST /<zasob>/{id}/update`:

- `FactStatus` (`domain/enums/fact_status.py`) — `VERIFIED` / `UNVERIFIED` /
  `DISPUTED`: czy fakt jest potwierdzony. Nowo wygenerowane insighty domyślnie
  dostają `UNVERIFIED`.
- `ReviewStatus` (`domain/enums/review_status.py`) — `PENDING` / `APPROVED` /
  `REJECTED`: stan ręcznego review przez człowieka.

Generacja `OfferInsight` idzie przez `POST /offers/{offer_id}/insights/generate`
z body `{types: [...]}` (lista `OfferInsightType`) — zastąpiło to starsze
`GET /offers/{id}/suggestions` z poprzedniej wersji tego dokumentu (ten endpoint
już nie istnieje w routingu).

## Wzorzec CRUD (update/delete) dla każdego zasobu w łańcuchu

Każdy generowany zasób (Offer, Knowledge, Brand Marketing, Marketing/Offer/
Message/Ad Strategy, Creative Strategy, Ad/Creative Execution, UGC Creative,
Page Strategy/Requirements/Blueprint/Content Plan/Copy) ma, obok `generate`/
`create`, listy i szczegółów, także:

- `POST /<zasob>/{id}/update` — częściowa edycja pól (body zwykle
  `{fields: {...}}` jako dowolny dict nadpisywany na rekordzie; niektóre zasoby,
  np. Target Audience, Offer/Knowledge Insight, Page Requirements, mają własny,
  typowany request model zamiast ogólnego `fields` dicta).
- `GET /<zasob>/{id}/delete` — oznaczone w kodzie komentarzem `# DELETE in future`
  (są to `GET`, nie `DELETE`, celowo tymczasowo, do czasu przejścia na właściwe
  metody HTTP).

## Uwagi architektoniczne

- Każdy poziom łańcucha ma zestaw endpointów: **`generate`** (LLM + zapis do
  bazy) lub **`create`** (bez LLM, dla kroków-kontenerów), **lista dla rodzica**
  (`GET /<parent>/{parent_id}/<zasob>`), **szczegóły po id** (`GET /<zasob>/{id}`),
  **`update`** i **`delete`** — konwencja spójna w całym projekcie.
- Endpointy `generate` przyjmują w URL **wyłącznie id bezpośredniego rodzica**
  (wyjątek: `marketing-strategy/generate`, patrz wyżej) — pełny kontekst
  przodków (aż do `knowledge`) handler odtwarza sam, chodząc w górę po relacjach
  przez repozytoria. To ważna zmiana względem starszej wersji tego dokumentu,
  która błędnie sugerowała kumulację wszystkich id przodków w URL.
- Kroki-kontenery bez LLM (Ad Execution, Page Requirements, Analysis, Checklist —
  ich `create`) służą do ustalenia parametrów wejściowych/ograniczeń **przed**
  właściwą generacją LLM w kolejnym kroku (Creative Execution, Page Blueprint,
  odpowiednio Analysis Answers, Checklist generate).
- Widoczny wzorzec "od strategii do treści": kroki 5-8 (Brand/Marketing/Offer/
  Message strategy) świadomie **nie generują żadnej gotowej treści** (bez
  nagłówków, CTA, scenariuszy) — dopiero ostatnie ogniwa każdej gałęzi
  (Creative Execution, UGC Creatives, Page Copy) produkują tekst gotowy do
  publikacji. To rozdzielenie pozwala tej samej strategii zasilać wiele różnych
  egzekucji (np. wiele wariantów Ad Execution/Creative Execution z jednej
  Creative Strategy).
- Wszystkie generacje idą przez `ollama_service` (lokalny model LLM) i zapisują
  wynik do bazy (SQLite, `Base.metadata.create_all()` — Alembic nie jest w tym
  repo faktycznie zainicjalizowany mimo że jest zależnością).
- Warstwy: `api/routes` (routing) → `application/handlers` ("kontrolery",
  budują własny `Container()`) → `application/services` / `application/assemblers`
  (logika + składanie DTO z dzieci) → `infrastructure/repositories` (SQLAlchemy) →
  `domain/models` (encje).
- Endpoint `GET /knowledges/{knowledge_id}/advertisements/generate` (starszy,
  równoległy generator "Advertisement" opisany w sekcji "Starszy/równoległy
  moduł: Advertisement" wyżej) oraz `GET /knowledges/{knowledge_id}/suggestions`
  (sugestie uzupełnień knowledge) są nadal zakomentowane w `general_routes.py` —
  handlery i stos DTO/repo/asembler istnieją, ale route jest wyłączony.
- Sekcja "Settings" (`GET`/`POST /settings/output-prompt`) pozwala odczytać i
  zapisać globalny, konfigurowalny fragment promptu wyjściowego — bez LLM, poza
  głównym łańcuchem.
