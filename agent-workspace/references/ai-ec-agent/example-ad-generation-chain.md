# Przykładowy, rzeczywisty łańcuch generowania — od Oferty do reklamy

Pobrane 2026-09-04 z działającej instancji backendu (`python main.py`, port 8002) — realne dane z lokalnej bazy deweloperskiej (`backend/app.db`), nie dane wymyślone. Każdy odczyt to `GET` na już zaimplementowany endpoint (assembled DTO, dokładnie to, co widzi frontend). Konkretny łańcuch: **Offer 2 → Knowledge 2 → BrandMarketing 2 → MarketingStrategy 2 → OfferStrategy 2 → MessageStrategy 3 → AdStrategy 2 → CreativeStrategy 7 → AdExecution 45 → CreativeExecution 131** (gałąź „ads”, produkt „Słoik Milo”).

Ogólny mechanizm (co dokładnie trafia do promptu na każdym kroku) jest opisany w `application-flow.md`. Ten plik pokazuje to samo, ale na **jednym konkretnym, rzeczywistym przykładzie** — dla każdego etapu: co dokładnie było wejściem do LLM i co dokładnie z tego wejścia powstało.

---

## 1. Offer (id=2) — `GET /offers/create`, ręczne, brak AI

**Wejście:** brak — dane wpisane ręcznie przez użytkownika w formularzu.

**Co istnieje:**
```json
{
  "name": "Słoik Milo",
  "buying_price": 25.0,
  "selling_price": 74.0,
  "details": "Słoik wypełniony kolorowymi karteczkami podzielonymi na różne kategorie tematyczne...",
  "offer_items": [
    { "name": "kolorowe karteczki", "quantity": 96, "details": "Kolorowe karteczki z wartościowymi przesłaniami, podzielone na 6 kategorii oznaczonych różnymi kolorami." },
    { "name": "jar", "quantity": 1, "details": "słoik z kolorowymi karteczkami złożonymi na pół" },
    { "name": "instrukcja", "quantity": 1, "details": "Instrukcja na zawieszce przywiązanej do słoika" }
  ]
}
```
Dodatkowo osobnym, opcjonalnym wywołaniem (`POST /offers/2/insights/generate`) wygenerowano `offer_insights` (AI, na bazie samej oferty) — np. `pain_points`: „Difficulty balancing work demands with mental well-being without a tangible self-care aid”, `target_audience`: „single working adults managing career growth and personal well-being”.

---

## 2. Knowledge (id=2) — `GET /offers/2/knowledges/generate`

**Wejście do LLM:** cały Offer(2) powyżej (`offer_service.build_llm_context(2)` → `to_content_dict()`, czyli bez `id`).

**Co zostało wygenerowane:**
```json
{
  "offer_summary": "Słoik Milo is a customizable jar containing 96 color-coded note cards organized into thematic categories designed for self-reflection, emotional expression, and personal growth.",
  "category": "Self-care tools, mindfulness aids, personalized gifts, and educational resources",
  "value_proposition": "A customizable, tactile tool that transforms abstract emotional and mental well-being goals into actionable, daily practices through structured, color-coded prompts."
}
```
Plus **44 `knowledge_insights`** (jeden model per pojedynczy fakt), pogrupowane wg `KnowledgeInsightType`, np.:
- `feature`: „Customizable categories and color schemes”
- `differentiator`: „Unique combination of physical tangibility and thematic categorization”
- `emotional_benefit`: „Reduces stress through organized self-expression”
- `limitation`: „No digital integration for tracking progress or analytics”

Każdy insight ma `fact_status`/`review_status` (tu: wszystkie `verified`/`approved` — czyli ktoś już przeszedł ręczną weryfikację w UI).

---

## 3. TargetAudience (11 rekordów) — `GET /knowledges/2/target-audiences/generate`

**Wejście do LLM:** Knowledge(2) + lista już istniejących `TargetAudience` tej wiedzy (`build_uniqueness_prompt`, żeby model nie powtórzył segmentu).

**Przykład jednego z 11 wygenerowanych segmentów** (`id=22`, `score=0.82` — najwyżej oceniony):
```json
{
  "name": "Mindfulness Enthusiasts",
  "reason": "Aligns with self-care and emotional well-being goals; color-coded systems appeal to organized individuals",
  "score": 0.82,
  "age_min": 25, "age_max": 35, "purchasing_power": "medium",
  "pain_points": ["difficulty maintaining daily reflection habits", "overwhelm from unstructured journaling"],
  "message_angles": ["transform abstract feelings into actionable steps", "color-coded organization for busy lives"],
  "marketing_channels": ["Instagram Reels", "Pinterest boards", "Wellness podcast sponsorships"]
}
```
(pozostałe 10 to warianty dla innych person: „Gift-Giving Nostalgia Seekers”, „Therapy Practice Coaches”, „Digital Nomad Self-Reflection Communities” itd.)

---

## 4. BrandMarketing (id=2) — `GET /knowledges/2/brand-marketing/generate`

**Wejście do LLM:** Knowledge(2) (offer_summary + wszystkie 44 insighty).

**Co zostało wygenerowane (wybrane pola z ~30):**
```json
{
  "brand_name": "Słoik Milo",
  "brand_positioning": "A physical, personalized ritual that helps you pause, name what you're feeling, and turn mental chaos into greater clarity.",
  "tagline": "A moment to hear yourself.",
  "unique_selling_proposition": "A personalized physical self-reflection ritual that removes the pressure of the blank page and helps you reconnect with yourself without another screen.",
  "brand_voice": "Empathetic, encouraging, and structured",
  "customer_transformation": "From 'I have too much in my head' to 'I understand what I'm feeling and what I need right now.'"
}
```
Widać bezpośrednie przejście insightów Knowledge → konkretny język marki (np. insight `emotional_benefit: "Reduces stress..."` → `customer_pains: ["Feeling overwhelmed by too many thoughts and emotions", ...]`).

---

## 5. MarketingStrategy (id=2) — `GET /brand-marketing/2/marketing-strategy/generate`

**Wejście do LLM:** Knowledge(2) + BrandMarketing(2).

**Co zostało wygenerowane (wybrane pola):**
```json
{
  "marketing_objective": "Drive awareness and adoption of Słoik Milo as a tangible, personalized self-reflection ritual...",
  "primary_audience": ["Mindfulness Enthusiasts", "Journaling & Self-Reflection Seekers", "Screen-Fatigued Self-Care Consumers"],
  "campaign_directions": [
    { "name": "From Chaos to Clarity", "objective": "Demonstrate product's ability to organize emotional overwhelm", "audience": "Mindfulness Enthusiasts" },
    { "name": "The Gift of Reflection", "objective": "Position product as meaningful gift solution", "audience": "Gift-Giving Nostalgia Seekers" }
  ]
}
```
`primary_audience: "Mindfulness Enthusiasts"` to bezpośrednie odwołanie do nazwy segmentu wygenerowanego w kroku 3 (`TargetAudience.name`) — model dostał go w kontekście przez `Knowledge → target_audiences`.

---

## 6. OfferStrategy (id=2) — `GET /marketing-strategy/2/offer-strategy/generate`

**Wejście do LLM:** Knowledge + BrandMarketing + MarketingStrategy (cały łańcuch wstecz).

**Co zostało wygenerowane (wybrane pola):**
```json
{
  "offer_name": "Słoik Milo: Your Personalized Reflection Journey",
  "core_value_proposition": "A simple, personalized, screen-free ritual that makes self-reflection easier to start and easier to return to.",
  "customer_objection_handling": [
    { "objection": "Isn't it just a jar with prompts?", "solution": "Show that Milo is a thoughtfully designed reflection system with curated prompts, color-coded categories, personalization..." }
  ],
  "guarantee": "30-day satisfaction guarantee if the product does not meet customer expectations."
}
```

---

## 7. MessageStrategy (id=3) — `GET /offer-strategy/2/message-strategy/generate`

**Wejście do LLM:** Knowledge + BrandMarketing + MarketingStrategy + OfferStrategy.

**Co zostało wygenerowane (wybrane pola):**
```json
{
  "core_message": "Słoik Milo transforms mental chaos into clarity through a simple, personalized physical ritual that makes self-reflection easier to start and return to.",
  "primary_message_angle": "Structured, screen-free prompts that make self-reflection easier to start and return to.",
  "feature_to_benefit_mapping": [
    { "feature": "Color-coded note cards", "functional_benefit": "Visual categorization makes prompts easier to navigate", "emotional_benefit": "Makes reflection feel more approachable and less chaotic." }
  ]
}
```
To ostatni etap wspólny dla wszystkich gałęzi — od tego miejsca (`message_strategy_id=3`) pipeline rozgałęzia się na ads/UGC/page.

---

## 8. AdStrategy (id=2) — `GET /message-strategy/3/ad-strategy/generate` (gałąź ADS)

**Wejście do LLM:** cały łańcuch wstecz aż do Knowledge, przez `message_strategy_id=3`.

**Co zostało wygenerowane:**
```json
{
  "customer_stage": "Consideration (aware of self-reflection needs but seeking structured solutions)",
  "creative_concepts": [
    {
      "name": "From Chaos to Clarity",
      "idea": "Show a relatable moment of mental overwhelm followed by the simple act of choosing a Milo prompt and taking a few minutes to reflect.",
      "recommended_creative_type": "problem-solution / UGC demo",
      "emotional_direction": "Relatable, calming, reassuring"
    }
  ],
  "recommended_formats": [
    { "format": "ugc_testimonial", "reason": "Leverage real user stories to build trust..." },
    { "format": "product_demo", "reason": "Demonstrate customization process and usage..." }
  ]
}
```
Widać, że nazwa kampanii z `MarketingStrategy.campaign_directions[0].name` („From Chaos to Clarity”, krok 5) wraca tu jako `creative_concepts[0].name` — model konsekwentnie trzyma się wcześniej ustalonego konceptu w całym łańcuchu.

---

## 9. CreativeStrategy (id=7) — `GET /ad-strategy/2/creative-strategy/generate`

**Wejście do LLM:** AdStrategy(2) + cały łańcuch wstecz.

**Co zostało wygenerowane:**
```json
{
  "name": "From Chaos to Clarity",
  "creative_type": "problem-solution",
  "recommended_format": "short form video",
  "creative_big_idea": "Show the journey from mental chaos to clarity by highlighting how Milo's color-coded prompts provide a simple, actionable ritual for reflection.",
  "hook_strategy": {
    "type": "relatable scenario",
    "direction": "Start with a visually chaotic scene transitioning to calm through Milo's structured prompts"
  },
  "emotion_flow": ["curiosity", "recognition", "trust", "desire"]
}
```

---

## 10. AdExecution (id=45) — `GET /creative-strategy/7/ad-execution/create`, **bez AI**

**Wejście:** brak LLM — tylko parametry z requestu (wybrane ręcznie przez użytkownika w UI, walidowane wg enuma `CreativeTypes`):
```json
{ "creative_type": "video", "platform": "instagram_feed", "format": "Vertical 4:5" }
```
To „pojemnik” na konkretne wykonanie kreatywne — dopiero kolejny krok generuje treść.

---

## 11. CreativeExecution (id=131) — `GET /ad-execution/45/creative-execution/generate` (liść gałęzi ADS)

**Wejście do LLM:** AdExecution(45) [`creative_type`/`platform`/`format`] + cały łańcuch wstecz aż do Knowledge + dodatkowe parametry wyboru frameworka/kąta/stylu (tu nieużyte — puste `ad_framework_id`/`creative_angle_id`/`execution_style_id`).

**Co zostało wygenerowane — finalny scenariusz 15-sekundowego wideo:**
```json
{
  "duration_seconds": 15,
  "creative_thesis": {
    "big_idea": "Słoik Milo transforms mental chaos into clarity through a simple, personalized ritual...",
    "visual_engine": "A seamless transition from a cluttered, overwhelmed moment to calm clarity through the structured use of color-coded prompts."
  },
  "structure": [
    { "name": "Hook", "start_second": 0, "end_second": 3, "goal": "Capture attention with a relatable moment of mental overwhelm" },
    { "name": "Demonstration", "start_second": 3, "end_second": 8, "goal": "Show the product in action during a real-world reflection moment" },
    { "name": "Benefits", "start_second": 8, "end_second": 11, "goal": "Highlight the immediate emotional and practical benefits" },
    { "name": "CTA", "start_second": 11, "end_second": 15, "goal": "Encourage immediate action with a clear call to purchase" }
  ],
  "scenes": [
    {
      "order": 1, "section": "Hook", "start_second": 0, "end_second": 3,
      "visual": "Close-up of a hand scrolling rapidly through a phone screen filled with notifications... The hand pulls a Milo card from the jar, the color-coded text visible.",
      "on_screen_text": "Feeling overwhelmed by too many thoughts?"
    }
  ]
}
```
(pełny `content_json` ma 4 sceny — Hook/Demonstration/Benefits/CTA — każda z `visual`, `camera_direction`, `voiceover`, `on_screen_text`, `editing_notes`).

---

## Podsumowanie — co widać na tym konkretnym przykładzie

- Każdy krok **rzeczywiście** dokłada nowy poziom konkretności: Offer (fakty o produkcie) → Knowledge (uogólnione insighty) → BrandMarketing (język marki) → strategie (kanały, segmenty, obiekcje) → AdStrategy/CreativeStrategy (koncept kreatywny) → CreativeExecution (gotowy scenariusz sekunda-po-sekundzie).
- Konkretne sformułowania **realnie migrują** między etapami (np. nazwa kampanii „From Chaos to Clarity” z kroku 5 → 8 → 9; segment „Mindfulness Enthusiasts” z kroku 3 → 5 → 8) — potwierdza to opisany w `application-flow.md` mechanizm pełnego odtwarzania łańcucha kontekstu przy każdym wywołaniu.
- Widać też praktyczną skalę promptów: sam Knowledge(2) to już ~22 KB JSON-a (44 insighty + 11 target audiences), a `page_copy`/`creative_execution` musi to wszystko (plus kolejne warstwy) zmieścić w jednym wywołaniu — stąd realna potrzeba dużego `OLLAMA_CONTEXT_LENGTH` opisana w `architecture.md`.

## Powiązane pliki pamięci

- `../../memory/ai-ec-agent/application-flow.md` — ogólny opis mechanizmu i pełnej listy etapów (w tym gałęzie UGC i page, tu nie pokazane).
- `../../memory/ai-ec-agent/architecture.md` — warstwy backendu, konfiguracja Ollama.
