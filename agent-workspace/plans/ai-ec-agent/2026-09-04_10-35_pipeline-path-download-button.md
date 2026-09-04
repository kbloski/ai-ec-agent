# Goal

Na każdej stronie zasobu (encji pipeline'u) dodać w bocznym panelu (`AppContextSidebar`) przycisk pobierający plik `.txt` z pełną ścieżką danych dla bieżącej encji — wykorzystując już gotowy backendowy endpoint `POST /pipeline/path`.

# Context

W tej samej sesji zbudowano `POST /pipeline/path` (`backend/application/handlers/pipeline/get_pipeline_path_handler.py`) — zwraca dla dowolnej encji pipeline'u (dowolny z 16 głównych etapów, obejmujący trzon + wszystkie 3 gałęzie: ads/ugc/page) pełną ścieżkę wstecz do Offer, z `data` (surowe pole encji) i `llm_context` (gotowy, otagowany string dokładnie taki, jaki widzi LLM przy generowaniu — dla etapów, z których coś dalej się generuje) dla każdego ogniwa. Obecnie jedyny sposób z tego skorzystać to ręczne wywołanie API — użytkownik chce szybki eksport z poziomu UI.

Diagnoza z tej samej sesji: przy odpalaniu backendu przez `python main.py` (`reload=True`) osierocone subprocessy robocze mogą nawarstwiać się na porcie 8002 ze starą wersją kodu — do zweryfikowania samodzielnie przez użytkownika przy testowaniu (najpewniej: sprawdzić `/openapi.json` zawiera `/pipeline/path` zanim testuje się resztę). To nie jest już zadanie do wykonania w tym planie.

# Current State

- Backend: endpoint gotowy, zweryfikowany logicznie (`TestClient`, izolowane wywołanie routera) — działanie przez faktyczny proces HTTP do potwierdzenia przez użytkownika.
- Frontend: brak jakiegokolwiek UI korzystającego z tego endpointu.

# Proposed Approach

## Zakres — które strony dostają przycisk

Tylko strony odpowiadające 16 typom encji z backendowego `PipelineEntityType` (trzon + ads/ugc/page). Bez przycisku: Analysis, Checklist, TargetAudience, OfferInsight, OfferItem, KnowledgeInsight — brak dla nich odpowiednika w `STAGE_CONFIG` backendu.

Mapowanie pattern→entityType (z `AppContextSidebar.tsx`, wartości `entityType` identyczne z `PipelineEntityType` w backendzie):

```
/offers/:id/*            → offer
/knowledges/:id/*        → knowledge
/brand-marketing/:id/*   → brand_marketing
/marketing-strategy/:id/*→ marketing_strategy
/offer-strategy/:id/*    → offer_strategy
/message-strategy/:id/*  → message_strategy
/ad-strategy/:id/*       → ad_strategy
/creative-strategy/:id/* → creative_strategy
/ad-execution/:id/*      → ad_execution
/page-strategy/:id/*     → page_strategy
/page-requirements/:id/* → page_requirements
/page-blueprint/:id/*    → page_blueprint
/page-content-plan/:id/* → page_content_plan
/creative-execution/:id/*→ creative_execution
/ugc-creatives/:id/*     → ugc_creative
/page-copy/:id/*         → page_copy
```

Id encji z `match.params.id` (wszystkie powyższe patterny mają jeden segment `:id` odpowiadający własnemu id strony).

## 1. RTK Query — `frontend/src/features/pipeline/pipelineApi.ts` (nowy)

```ts
export interface PipelinePathStage {
  stage: string
  id: number
  data: Record<string, unknown>
  llm_context: string | null
}
export interface PipelinePathResponse {
  requested: { entity_type: string; entity_id: number }
  path: PipelinePathStage[]
}

export const pipelineApi = api.injectEndpoints({
  endpoints: (builder) => ({
    getPipelinePath: builder.mutation<PipelinePathResponse, { entity_type: string; entity_id: number }>({
      query: (body) => ({ url: '/pipeline/path', method: 'POST', body }),
    }),
  }),
})
export const { useGetPipelinePathMutation } = pipelineApi
```
Mutacja (nie query) — pobieranie inicjowane kliknięciem, nie automatycznym renderem.

## 2. Nowy komponent — `frontend/src/components/DownloadPipelinePathButton.tsx`

- Props: `{ entityType: string; entityId: number }`.
- Na klik: `getPipelinePath({ entity_type: entityType, entity_id: entityId }).unwrap()`.
- Formatowanie odpowiedzi do czytelnego tekstu: dla każdego etapu nagłówek `===== STAGE (id=N) =====` + `llm_context` (gotowy string), a dla liści bez `llm_context` (creative_execution/ugc_creative/page_copy) — `JSON.stringify(data, null, 2)`.
- Pobranie pliku: `Blob` + tymczasowy `<a download>` (`URL.createObjectURL`/`revokeObjectURL`), nazwa: `pipeline-path_<entityType>-<entityId>.txt`.
- Stan: disabled + "Pobieranie…" podczas mutacji; błędy pokaże istniejący globalny middleware (`apiErrorMiddleware.ts`).
- UI: istniejący `Button` (`components/ui/button.tsx`, np. `variant="outline" size="sm"`), ikona `Download` z `lucide-react`.

## 3. `AppContextSidebar.tsx` — rozszerzenie

- Dodać pole `entityType` (opcjonalne) do 16 wpisów w `sections` wg mapowania wyżej.
- W bloku "Aktualny etap" (obok istniejącego `Link`), jeśli `section.config.entityType` istnieje: wyrenderować `<DownloadPipelinePathButton entityType={section.config.entityType} entityId={Number(section.match.params.id)} />`.

# Files / Components Involved

- `frontend/src/features/pipeline/pipelineApi.ts` (nowy)
- `frontend/src/components/DownloadPipelinePathButton.tsx` (nowy)
- `frontend/src/components/AppContextSidebar.tsx` (edycja)

Backend bez zmian.

# Risks

Minimalne — czysto frontendowa, addytywna zmiana UI; żadnych zmian kontraktu API ani istniejących komponentów poza dodaniem opcjonalnego pola konfiguracyjnego.

# Validation

Po uruchomieniu backendu przez użytkownika: otworzyć strony z różnych gałęzi (np. `/offers/2`, `/ad-execution/45`, stronę page_copy, stronę ugc_creative), kliknąć przycisk, sprawdzić poprawność pobranego `.txt` (czytelne nagłówki + kontekst), potwierdzić brak przycisku na stronach bez odpowiednika (Analysis, TargetAudience itd.). Dodatkowo `npm run lint` i `npx tsc --noEmit` po zmianach.

# Open Questions

Brak.
