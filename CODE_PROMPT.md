# Kontekst projektu

Pracujesz na istniejącym projekcie składającym się z:

- frontendu w React, rozwijanego zgodnie z istniejącą architekturą, konwencjami i systemem komponentów projektu,
- backendu w Pythonie, rozwijanego zgodnie z aktualną strukturą, wzorcami i zasadami aplikacji.

Twoim zadaniem jest rozwijanie istniejącego kodu przy zachowaniu spójności z obecną architekturą projektu.

Zanim napiszesz nowy kod, zrozum istniejący sposób rozwiązania danego problemu w projekcie.

Preferuj zgodność z istniejącym kodem, architekturą i konwencjami projektu nad wprowadzaniem nowych wzorców lub ogólnie uznawanych praktyk, jeżeli projekt posiada już własne rozwiązanie danego problemu.

Nie twórz nowej architektury, nowych warstw abstrakcji ani nowych wzorców projektowych, jeżeli istniejące rozwiązania można rozszerzyć lub ponownie wykorzystać.

Wprowadzaj możliwie najmniejszy zakres zmian potrzebny do poprawnej realizacji zadania.


---

# Źródła prawdy i priorytety

Aktualny kod, konfiguracja projektu i testy są głównym źródłem prawdy o rzeczywistym stanie aplikacji.

`_ai/agent_memory` jest źródłem dodatkowego kontekstu, wcześniejszych ustaleń i wiedzy trudnej do odtworzenia, ale nie zastępuje analizy aktualnego kodu.

Jeżeli informacje zapisane w `_ai/agent_memory` są sprzeczne z aktualnym kodem, konfiguracją, testami lub aktualnymi instrukcjami użytkownika:

1. zweryfikuj rzeczywisty stan projektu,
2. traktuj aktualny kod i bieżące instrukcje użytkownika jako źródło prawdy,
3. popraw, zaktualizuj lub usuń nieaktualną notatkę z `_ai/agent_memory`.

Aktualne instrukcje użytkownika mają pierwszeństwo przed wcześniejszymi ustaleniami zapisanymi w pamięci agenta.


---

# Pamięć agenta

Katalog:

`_ai/agent_memory`

służy jako trwała pamięć agenta pomiędzy sesjami.

Pamięć ma przechowywać przede wszystkim wiedzę, której ponowne ustalenie w przyszłości:

- wymagałoby dużo czasu,
- wymagałoby ponownej głębszej analizy kodu,
- wymagałoby prześledzenia wielu modułów lub zależności,
- jest często potrzebna podczas pracy nad projektem,
- nie wynika bezpośrednio i jednoznacznie z kodu,
- mogłaby zostać utracona pomiędzy sesjami.

## Przed rozpoczęciem pracy

Przed rozpoczęciem implementacji sprawdź zawartość `_ai/agent_memory`.

Jeżeli istnieją tam notatki dotyczące:

- analizowanego modułu,
- wcześniejszych decyzji architektonicznych,
- znanych pułapek,
- nieoczywistych zależności,
- ustaleń z użytkownikiem,
- ograniczeń technicznych,
- trwających większych inicjatyw,

uwzględnij je podczas analizy zadania.

Nie zakładaj jednak automatycznie, że każda notatka jest nadal aktualna. W razie potrzeby skonfrontuj ją z bieżącym kodem.

## Co zapisywać w pamięci

Zapisuj informacje, które będą przydatne podczas przyszłych zadań i których ponowne odkrycie byłoby kosztowne czasowo lub trudne.

Przykładowo:

- decyzje architektoniczne oraz ich uzasadnienie,
- ważne kompromisy techniczne,
- ustalenia i preferencje przekazane przez użytkownika,
- poprawki wcześniejszego podejścia potwierdzone przez użytkownika,
- nieoczywiste zależności pomiędzy modułami,
- pułapki w kodzie lub konfiguracji,
- znane ograniczenia systemu,
- istotne zachowania zewnętrznych usług lub bibliotek,
- ważne założenia, które nie są widoczne bezpośrednio w kodzie,
- przyczyny zastosowania nietypowego rozwiązania,
- status większej niedokończonej inicjatywy,
- informacje, których ustalenie wymagało znaczącej analizy i prawdopodobnie będą ponownie potrzebne,
- wiedzę często potrzebną przy pracy nad danym obszarem projektu.

Jeżeli podczas pracy odkryjesz informację tego rodzaju, możesz zaktualizować `_ai/agent_memory` od razu, bez konieczności czekania do zakończenia zadania.

Aktualizuj pamięć na bieżąco zawsze wtedy, gdy uznasz, że nowa wiedza będzie istotna w przyszłych sesjach.

## Czego nie zapisywać w pamięci

Nie zapisuj:

- informacji łatwych do odtworzenia z kodu,
- oczywistej struktury katalogów,
- listy istniejących klas lub funkcji,
- historii zmian,
- opisu każdego wykonanego zadania,
- changelogu,
- informacji dostępnych bezpośrednio z historii gita,
- tymczasowych szczegółów implementacyjnych,
- wyników jednorazowego debugowania, które nie mają znaczenia w przyszłości,
- danych, które szybko tracą aktualność i nie mają trwałej wartości,
- sekretów, tokenów, haseł, kluczy API ani innych danych uwierzytelniających.

Nie twórz wpisu w `_ai/agent_memory` tylko dlatego, że zadanie zostało zakończone.

Pamięć nie jest dziennikiem pracy.

## Organizacja pamięci

Zapisuj notatki w plikach `.md`.

Grupuj je tematycznie, np. według:

- modułu,
- domeny biznesowej,
- integracji,
- obszaru technicznego,
- większej inicjatywy.

Nie organizuj pamięci chronologicznie, jeżeli wiedza dotyczy konkretnego obszaru projektu.

Preferuj aktualizację istniejącego pliku zamiast tworzenia kolejnego pliku zawierającego podobne informacje.

Pamięć powinna opisywać aktualny stan wiedzy o projekcie, a nie historię jego zmian.

Jeżeli jakaś informacja stanie się nieaktualna:

- popraw ją,
- zastąp aktualną wersją,
- albo usuń.

Nie pozostawiaj świadomie nieaktualnych informacji w pamięci.


---

# Analiza projektu przed rozpoczęciem pracy

Przed wykonaniem zmian przeanalizuj istniejący kod oraz architekturę projektu w zakresie niezbędnym do realizacji bieżącego zadania.

Analizuj źródła wiedzy w następującej kolejności:

1. `_ai/agent_memory` — wcześniejsze ustalenia, decyzje, pułapki i wiedza trwała,
2. `ai-ec-agent` — podstawowe źródło wiedzy o architekturze i konwencjach projektu,
3. `backend` i `frontend` — odpowiednie moduły wymagane przez charakter zadania,
4. testy, konfigurację i pozostałe elementy bezpośrednio związane ze zmienianą funkcjonalnością.

Nie analizuj całego repozytorium bez potrzeby.

Zakres analizy powinien odpowiadać zakresowi zadania.

Przed implementacją, odpowiednio do charakteru zadania, sprawdź:

- strukturę katalogów,
- architekturę analizowanego modułu,
- podział odpowiedzialności,
- zależności pomiędzy komponentami,
- przepływ danych,
- sposób komunikacji frontend ↔ backend,
- konfigurację,
- sposób obsługi błędów,
- sposób logowania,
- sposób dostępu do danych,
- istniejące modele danych,
- istniejące klasy i funkcje,
- komponenty React,
- interfejsy i typy,
- istniejące kontrakty API,
- obowiązujące wzorce projektowe,
- styl kodowania,
- testy dotyczące analizowanego obszaru.

Przed stworzeniem nowego rozwiązania wyszukaj istniejące implementacje rozwiązujące podobny problem.

W pierwszej kolejności:

1. wykorzystaj istniejące rozwiązanie,
2. rozszerz istniejące rozwiązanie,
3. dopiero jeśli powyższe nie są właściwe, utwórz nowe rozwiązanie.


---

# Zakres zmian

Implementuj wyłącznie zmiany niezbędne do realizacji bieżącego zadania.

Nie wykonuj przy okazji:

- niezwiązanych refaktoryzacji,
- reorganizacji katalogów,
- masowego formatowania niepowiązanych plików,
- zmian nazw niezwiązanych z zadaniem,
- aktualizacji zależności bez potrzeby,
- modernizacji kodu tylko dlatego, że można go napisać inaczej,
- zmian architektury niepotrzebnych do realizacji funkcjonalności.

Jeżeli podczas pracy zauważysz niezależny problem, nie naprawiaj go automatycznie, chyba że:

- bezpośrednio blokuje realizację zadania,
- powoduje błąd w zmienianym obszarze,
- albo użytkownik wyraźnie poprosił o jego naprawę.

Jeżeli problem jest istotny, ale nie powinien być naprawiany w ramach bieżącego zadania, możesz poinformować o nim użytkownika po zakończeniu pracy.


---

# Organizacja kodu

Kod powinien pozostawać zgodny z istniejącą architekturą projektu i być łatwy do dalszego rozwijania.

Przestrzegaj:

- Single Responsibility Principle,
- DRY,
- KISS,
- SOLID tam, gdzie jego zastosowanie rzeczywiście upraszcza rozwój projektu.

Preferuj:

- małe, wyspecjalizowane moduły,
- jasno określoną odpowiedzialność,
- czytelne interfejsy,
- separację logiki biznesowej od warstw technicznych,
- ponowne wykorzystanie istniejącego kodu,
- rozszerzanie istniejących mechanizmów zamiast ich duplikowania.

Nie twórz katalogów ani plików pełniących rolę magazynu przypadkowego kodu, takich jak:

- `utils`,
- `helpers`,
- `common`,
- `shared`,
- `misc`,
- `temp`,
- `lib` — jeżeli miałby pełnić rolę ogólnego katalogu na niepowiązany kod.

Jeżeli katalog o takiej nazwie już istnieje, dodawaj do niego kod wyłącznie wtedy, gdy nowy kod odpowiada jego obecnej, jasno określonej odpowiedzialności.

Każdy nowy:

- moduł,
- komponent React,
- hook,
- klasa,
- serwis,
- plik,
- endpoint,

powinien posiadać jednoznacznie określoną odpowiedzialność i naturalnie wpisywać się w istniejącą strukturę projektu.

Nie przenoś istniejących plików ani nie reorganizuj katalogów wyłącznie z powodów estetycznych.


---

# Frontend i komponenty UI

Frontend powinien wykorzystywać istniejący system komponentów oraz obowiązujące standardy projektu.

Przed utworzeniem nowego komponentu sprawdź:

1. czy odpowiedni komponent już istnieje,
2. czy istniejący komponent można rozszerzyć,
3. czy wymagany element jest dostępny w używanej przez projekt bibliotece UI,
4. czy projekt posiada już analogiczne rozwiązanie w innym miejscu.

Jeżeli projekt korzysta z `shadcn/ui`:

- preferuj istniejące komponenty `shadcn/ui`,
- wykorzystuj istniejące warianty i style,
- korzystaj z istniejących tokenów projektu,
- nie implementuj ręcznie elementów dostępnych w `shadcn/ui`.

Jeżeli wymagany komponent `shadcn/ui` nie jest jeszcze zainstalowany, ale projekt korzysta z tej biblioteki, dodaj go zgodnie z oficjalnym sposobem instalacji i istniejącą strukturą projektu.

Nie twórz własnych zamienników standardowych komponentów biblioteki bez uzasadnionej potrzeby.

Nowe komponenty React twórz wtedy, gdy:

- posiadają konkretną odpowiedzialność biznesową lub funkcjonalną,
- ich wydzielenie poprawia czytelność,
- ich wydzielenie rzeczywiście umożliwia ponowne użycie,
- komponent nie jest jedynie zbędnym wrapperem na istniejący element UI.

Zachowuj spójność wizualną z pozostałą częścią aplikacji.


---

# Backend

Backend rozwijaj zgodnie z aktualną strukturą aplikacji Python.

Przed utworzeniem:

- nowego endpointu,
- serwisu,
- modelu,
- repozytorium,
- warstwy abstrakcji,
- mechanizmu walidacji,
- sposobu obsługi błędów,

sprawdź, jak analogiczny problem rozwiązano już w projekcie.

Nie twórz dodatkowych warstw tylko po to, aby kod odpowiadał abstrakcyjnemu wzorcowi architektonicznemu.

Logika biznesowa powinna znajdować się w warstwie zgodnej z aktualną architekturą projektu, a nie przypadkowo w endpointach, komponentach technicznych lub modelach danych.


---

# Kontrakty frontend ↔ backend

Zmiany w komunikacji pomiędzy frontendem i backendem traktuj jako zmiany kontraktu.

Jeżeli zmieniasz:

- request,
- response,
- strukturę danych,
- nazwę pola,
- typ pola,
- kod błędu,
- semantykę endpointu,
- sposób autoryzacji,
- sposób paginacji,
- sposób filtrowania,

sprawdź wszystkie miejsca korzystające z danego kontraktu.

Nie duplikuj ręcznie modeli lub typów, jeżeli projekt posiada istniejący mechanizm ich współdzielenia lub generowania.

Zachowuj kompatybilność wsteczną, jeżeli nie istnieje uzasadniona potrzeba jej zerwania.

Nie zmieniaj kontraktów API bez potrzeby wynikającej z bieżącego zadania.


---

# Dane i migracje

Przed zmianą sposobu przechowywania danych sprawdź, jak projekt obecnie zarządza schematem danych.

Jeżeli projekt posiada istniejący mechanizm migracji:

- korzystaj z niego,
- zachowuj jego istniejące konwencje,
- generuj lub twórz migracje zgodnie ze sposobem używanym w projekcie.

Nie zakładaj jednak, że mechanizm migracji istnieje.

Jeżeli projekt obecnie nie posiada systemu migracji, nie dodawaj nowego frameworka ani mechanizmu migracyjnego wyłącznie dlatego, że byłby standardowym rozwiązaniem.

Dodanie systemu migracji powinno wynikać z rzeczywistej potrzeby projektu lub wyraźnej decyzji użytkownika.

Jeżeli zmiana danych wymaga rozwiązania, którego aktualnie projekt nie posiada, najpierw przeanalizuj istniejące podejście i wybierz rozwiązanie możliwie najmniej ingerujące w architekturę.

Nie wykonuj destrukcyjnych zmian danych bez jednoznacznej potrzeby.

Jeżeli projekt posiada migracje, które mogły zostać już zastosowane w istniejących środowiskach, nie modyfikuj ich bez wyraźnego uzasadnienia. Preferuj nową migrację zgodnie z konwencją projektu.


---

# Zależności

Nie dodawaj nowej biblioteki, jeżeli problem można rozsądnie rozwiązać za pomocą zależności już obecnych w projekcie.

Przed dodaniem zależności:

1. sprawdź istniejące zależności,
2. sprawdź, czy projekt nie posiada już rozwiązania danego problemu,
3. oceń, czy nowa zależność daje realną wartość względem kosztu jej utrzymywania.

Nie implementuj ręcznie skomplikowanej funkcjonalności, jeżeli projekt świadomie wykorzystuje już bibliotekę rozwiązującą ten problem.

Nie aktualizuj wersji istniejących zależności bez potrzeby związanej z bieżącym zadaniem.

Nie wykonuj dużych aktualizacji zależności „przy okazji”.


---

# Obsługa błędów

Stosuj istniejący sposób obsługi błędów.

Nie wprowadzaj nowego globalnego mechanizmu obsługi błędów, jeżeli projekt posiada już własny.

Nie ukrywaj błędów przez puste `catch`, `except` lub podobne konstrukcje.

Błąd powinien:

- zostać obsłużony tam, gdzie istnieje możliwość podjęcia sensownej decyzji,
- zostać przekazany dalej, jeżeli odpowiedzialność należy do wyższej warstwy,
- zostać zalogowany zgodnie z istniejącym mechanizmem projektu, jeżeli jest to potrzebne.

Nie wykorzystuj wyjątków jako zwykłego mechanizmu sterowania przepływem, jeżeli istnieje prostsze rozwiązanie zgodne z kodem projektu.


---

# Logowanie

Korzystaj z istniejącego mechanizmu logowania.

Nie wprowadzaj nowego loggera ani biblioteki logującej bez potrzeby.

Logi powinny pomagać diagnozować zachowanie systemu.

Nie dodawaj nadmiernej liczby logów dla normalnego przebiegu działania.

Nie loguj:

- haseł,
- tokenów,
- kluczy API,
- sekretów,
- pełnych danych uwierzytelniających,
- innych danych wrażliwych.


---

# Bezpieczeństwo

Nie zapisuj w kodzie ani `_ai/agent_memory`:

- haseł,
- tokenów,
- kluczy API,
- sekretów,
- danych uwierzytelniających.

Korzystaj z istniejącego mechanizmu konfiguracji i zmiennych środowiskowych.

Nie obchodź istniejących mechanizmów autoryzacji, walidacji lub bezpieczeństwa wyłącznie w celu uproszczenia implementacji.

Dane pochodzące od użytkownika lub systemów zewnętrznych traktuj jako niezaufane zgodnie z aktualnymi zasadami projektu.


---

# Testy i weryfikacja

Po implementacji zweryfikuj zmieniony obszar.

Preferuj możliwie najmniejszy zestaw testów wystarczający do uzyskania wysokiej pewności, że zmiana działa poprawnie.

W zależności od projektu i charakteru zadania mogą to być:

- istniejące testy jednostkowe,
- testy integracyjne,
- testy backendu,
- testy frontendu,
- type-checking,
- lint,
- build,
- test konkretnego endpointu,
- test konkretnego przepływu użytkownika.

W pierwszej kolejności uruchamiaj testy dotyczące zmienionego modułu.

Nie uruchamiaj kosztownych testów całego repozytorium bez potrzeby, jeżeli mniejszy zestaw wystarczająco weryfikuje zmianę.

Jeżeli w analizowanym obszarze istnieją testy, zapoznaj się z nimi przed zmianą zachowania.

Jeżeli zmiana wprowadza nową istotną logikę, dodaj lub rozszerz testy zgodnie z aktualnymi konwencjami projektu, jeżeli projekt posiada testy dla tego rodzaju kodu.

Nie twórz nowego frameworka testowego, jeżeli projekt obecnie go nie posiada, chyba że użytkownik wyraźnie tego oczekuje.

Jeżeli test nie przechodzi:

- ustal przyczynę,
- nie usuwaj testu tylko po to, aby uzyskać zielony wynik,
- nie pomijaj testu bez uzasadnienia,
- nie osłabiaj asercji wyłącznie w celu ukrycia problemu.

Nie uznawaj zadania za zakończone, jeżeli wiesz, że wprowadzone zmiany powodują błąd pozostawiony bez rozwiązania.


---

# Bezpieczeństwo pracy z repozytorium

Szanuj istniejący stan repozytorium i pracę użytkownika.

Nie usuwaj ani nie nadpisuj istniejących zmian użytkownika.

Traktuj niezacommitowane zmiany jako potencjalną pracę użytkownika, chyba że jednoznacznie wynikają z bieżącego zadania.

Nie wykonuj bez jednoznacznego polecenia użytkownika destrukcyjnych operacji takich jak:

- hard reset,
- force checkout,
- czyszczenie nieśledzonych plików,
- przepisywanie historii,
- force push,
- masowe cofanie zmian.

Nie cofaj zmian w plikach niezwiązanych z bieżącym zadaniem.

Nie wykonuj commitów ani pushy, jeżeli użytkownik nie oczekuje tego w danym środowisku lub workflow.


---

# Konfiguracja

Przed dodaniem nowych ustawień sprawdź istniejący mechanizm konfiguracji.

Nie twórz nowego sposobu konfiguracji, jeżeli projekt posiada już:

- pliki konfiguracyjne,
- zmienne środowiskowe,
- obiekty settings,
- mechanizm dependency injection,
- konfigurację runtime.

Nowe ustawienia umieszczaj tam, gdzie logicznie należą zgodnie z istniejącą architekturą.

Nie hardcoduj wartości środowiskowych, które powinny być konfigurowalne.


---

# Dokumentacja i komentarze

Nie dodawaj komentarzy opisujących oczywisty kod.

Komentarze powinny wyjaśniać przede wszystkim:

- dlaczego zastosowano dane rozwiązanie,
- nietypowe ograniczenia,
- nieoczywiste zachowanie,
- istotne kompromisy techniczne.

Jeżeli projekt posiada dokumentację dotyczącą zmienianego mechanizmu i zmiana powoduje, że dokumentacja staje się nieaktualna, zaktualizuj ją.

Nie twórz rozbudowanej dokumentacji dla prostych zmian, jeżeli projekt nie stosuje takiej praktyki.


---

# Unikanie nadmiernej abstrakcji

Nie twórz abstrakcji na podstawie hipotetycznej przyszłej potrzeby.

Nie dodawaj:

- interfejsu mającego tylko jedną implementację bez uzasadnionej potrzeby,
- factory tylko dla jednego przypadku,
- dodatkowego service layer, jeżeli projekt go nie stosuje,
- wrappera bez realnej odpowiedzialności,
- konfiguracji dla wartości, która nie wymaga konfiguracji,
- mechanizmu pluginowego dla pojedynczego przypadku,
- generycznego systemu tam, gdzie wystarcza proste rozwiązanie.

Projektuj pod aktualne wymagania, pozostawiając kod możliwy do rozszerzenia bez budowania funkcjonalności, która nie jest obecnie potrzebna.


---

# Zachowanie istniejącego stylu

Dostosuj się do istniejącego stylu kodu.

Dotyczy to między innymi:

- nazewnictwa,
- struktury plików,
- importów,
- organizacji komponentów React,
- sposobu definiowania typów,
- sposobu definiowania modeli Python,
- sposobu tworzenia endpointów,
- walidacji,
- obsługi błędów,
- testów,
- formatowania.

Nie zmieniaj istniejącego stylu tylko dlatego, że preferujesz inny.


---

# Postępowanie w przypadku niepewności

Jeżeli odpowiedź można ustalić na podstawie:

- `_ai/agent_memory`,
- `ai-ec-agent`,
- kodu,
- konfiguracji,
- testów,

najpierw przeanalizuj te źródła zamiast pytać użytkownika.

Pytaj użytkownika wtedy, gdy istnieje rzeczywista decyzja produktowa, biznesowa lub architektoniczna, której nie można wiarygodnie wywnioskować z projektu.

Jeżeli istnieje kilka technicznie poprawnych rozwiązań, preferuj rozwiązanie:

1. zgodne z istniejącą architekturą,
2. powodujące najmniejszą zmianę,
3. najprostsze,
4. łatwe do utrzymania,
5. niewprowadzające niepotrzebnej zależności lub abstrakcji.


---

# Zakończenie zadania

Po zakończeniu pracy przedstaw zwięzłe podsumowanie zawierające:

- co zostało zmienione,
- istotne decyzje implementacyjne, jeżeli takie wystąpiły,
- jakie testy lub inne formy weryfikacji wykonano,
- czy pozostały znane ograniczenia lub kwestie wymagające dalszej pracy.

Nie opisuj każdego zmienionego wiersza kodu.

Jeżeli w trakcie zadania powstała trwała wiedza, której ponowne ustalenie byłoby czasochłonne lub która będzie często potrzebna w przyszłości, zaktualizuj `_ai/agent_memory`.

Przed zakończeniem zadania upewnij się, że ewentualnie zmienione notatki w `_ai/agent_memory` nadal odpowiadają rzeczywistemu stanowi projektu.