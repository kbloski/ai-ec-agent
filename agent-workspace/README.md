# agent-workspace

Trwałe środowisko pracy dla agenta AI rozwijającego jeden lub wiele projektów skonfigurowanych w:

```text
./projects/PROJECTS.md
```

To repozytorium nie zawiera właściwego kodu aplikacji.

Służy jako warstwa pomocnicza wokół projektów i przechowuje kontekst potrzebny agentowi między sesjami.

Właściwe projekty mogą znajdować się w dowolnym miejscu lokalnego systemu plików.

## Struktura

```text
.
├── ROOT_PROMPT.md
├── projects/
│   └── PROJECTS.md
├── prompts/
├── rules/
├── memory/
├── plans/
├── decisions/
├── references/
├── templates/
├── output/
└── scratch/
```

* `projects/` — konfiguracja lokalizacji aktywnych projektów;
* `prompts/` — trwałe instrukcje określające sposób pracy agenta;
* `rules/` — trwałe reguły i ograniczenia, których agent musi przestrzegać;
* `memory/` — wiedza o projektach, architekturze, integracjach i konwencjach;
* `plans/` — plany większych zadań;
* `decisions/` — ważne decyzje techniczne i ich uzasadnienie;
* `references/` — dokumentacja, materiały wejściowe i zewnętrzne źródła;
* `templates/` — szablony dokumentów;
* `output/` — trwałe wyniki pracy agenta, np. raporty, analizy, diagramy i eksporty;
* `scratch/` — tymczasowe pliki robocze.

Właściwy kod projektów nie znajduje się bezpośrednio w tym repozytorium.

Ich lokalizacje są wskazywane przez:

```text
projects/PROJECTS.md
```

## Projekty

`PROJECTS.md` może wskazywać jeden lub wiele projektów.

Przykład:

```text
/home/user/projects/backend
/home/user/projects/frontend
/home/user/projects/worker
```

Na Windows:

```text
D:/Projects/backend
D:/Projects/frontend
```

Każda ścieżka wskazuje kanoniczny katalog główny danego projektu.

Projekty mogą być całkowicie niezależnymi repozytoriami.

Agent przed rozpoczęciem pracy z kodem odczytuje `PROJECTS.md` i ustala, którego projektu lub których projektów dotyczy aktualne zadanie.

## Jak to działa

Przy pierwszym kontakcie z projektem agent analizuje jego strukturę, technologie, architekturę, workflow, testy, istotne ograniczenia i inne informacje potrzebne do dalszej pracy.

Następnie zapisuje trwały kontekst m.in. w:

```text
prompts/
rules/
memory/
```

Przy kolejnych sesjach korzysta z zapisanej wiedzy i analizuje tylko fragmenty projektu potrzebne do wykonania aktualnego zadania.

Nie powinien ponownie analizować całego projektu bez wyraźnego powodu.

Każdy projekt może posiadać własny kontekst.

Przykładowo:

```text
memory/
├── backend/
├── frontend/
└── worker/

rules/
├── backend/
├── frontend/
└── shared/
```

Agent nie powinien automatycznie przenosić wiedzy, reguł ani konwencji z jednego projektu do drugiego.

## Podział odpowiedzialności

W uproszczeniu:

```text
projects/    → lokalizacja aktywnych projektów

prompts/     → jak agent powinien pracować

rules/       → czego agent musi przestrzegać

memory/      → co agent wie o projektach

plans/       → jak agent zamierza wykonać większe zadania

decisions/   → co zostało zdecydowane i dlaczego

references/  → materiały wejściowe i pomocnicze

output/      → trwałe wyniki pracy

scratch/     → pliki tymczasowe
```

W szczególności:

```text
prompts/ ≠ rules/
rules/ ≠ memory/
memory/ ≠ decisions/
```

`prompts/` określa sposób działania agenta.

`rules/` zawiera obowiązujące ograniczenia i wymagania.

`memory/` przechowuje trwałą wiedzę o projektach.

`decisions/` przechowuje istotne decyzje wraz z ich uzasadnieniem.

## Utrzymanie workspace

Agent samodzielnie utrzymuje workspace.

Może tworzyć, aktualizować, reorganizować i usuwać nieaktualne materiały w odpowiednich katalogach, jeżeli jest to potrzebne do zachowania poprawnego i użytecznego kontekstu.

W szczególności powinien:

* aktualizować nieaktualną wiedzę;
* usuwać lub scalać duplikaty;
* zapisywać trwałe odkrycia;
* aktualizować reguły, gdy zmieniają się obowiązujące ograniczenia;
* utrzymywać aktywne plany;
* dokumentować ważne decyzje;
* porządkować materiały pomocnicze;
* usuwać zbędne pliki tymczasowe.

Istotna wiedza nie powinna pozostawać wyłącznie w `scratch/`.

## Kontekst wielu projektów

Jeżeli zadanie dotyczy kilku projektów, agent może pracować z nimi równocześnie.

Powinien jednak traktować każdy projekt jako osobny codebase i niezależnie weryfikować:

* architekturę;
* technologie;
* zależności;
* wersje runtime;
* komendy developerskie;
* testy;
* konwencje;
* reguły;
* proces buildowania;
* deployment.

Informacje charakterystyczne dla jednego projektu nie powinny być automatycznie uznawane za prawdziwe dla innych.

Wiedza dotycząca integracji między projektami może być przechowywana jako kontekst cross-project.

## Pełne zasady

Pełne zasady pracy agenta znajdują się w:

```text
ROOT_PROMPT.md
```

README opisuje jedynie ogólną ideę i strukturę workspace.

`ROOT_PROMPT.md` pozostaje głównym źródłem instrukcji operacyjnych.

## Git

`agent-workspace` oraz projekty wskazane w `projects/PROJECTS.md` mogą być osobnymi repozytoriami Git i mogą być wersjonowane całkowicie niezależnie.

Przykładowo:

```text
agent-workspace/
    .git/

D:/Projects/backend/
    .git/

D:/Projects/frontend/
    .git/
```

Zmiany w workspace nie oznaczają automatycznie zmian w repozytoriach projektów i odwrotnie.

## Idea

```text
LOCATE PROJECT
      ↓
ANALYZE ONCE
      ↓
REMEMBER
      ↓
LOAD RULES
      ↓
WORK
      ↓
VALIDATE
      ↓
GENERATE OUTPUT
      ↓
LEARN
      ↓
UPDATE CONTEXT
```

Celem jest, aby agent z każdą kolejną sesją znał projekty coraz lepiej, nie analizował ich za każdym razem od zera i pozostawiał po swojej pracy zarówno aktualny trwały kontekst, jak i potrzebne artefakty w `output/`.

Workspace pełni rolę trwałej pamięci operacyjnej i warstwy organizacyjnej dla agenta, natomiast właściwe repozytoria projektów pozostają od niego niezależne.
