# Kontekst projektu

Pracujesz na istniejącym projekcie składającym się z:

* **frontendu w React**, zorganizowanego zgodnie z obowiązującą architekturą projektu,
* **backendu w Pythonie**, rozwijanego zgodnie z aktualnymi konwencjami i strukturą aplikacji.

Twoim zadaniem jest rozwijanie istniejącego kodu przy zachowaniu spójności z obecną architekturą. Nie twórz nowej architektury ani nowych wzorców, jeżeli istnieją już rozwiązania, które można wykorzystać lub rozszerzyć.

---

# Analiza projektu przed rozpoczęciem pracy

Przed wykonaniem jakichkolwiek zmian przeanalizuj istniejący kod oraz architekturę projektu w zakresie niezbędnym do realizacji zadania.

Podstawowym źródłem wiedzy o projekcie jest katalog:

* `/ai-ec-agent`

Jeżeli charakter zadania tego wymaga (np. dotyczy komunikacji pomiędzy frontendem i backendem, API, modeli danych lub interfejsu użytkownika), rozszerz analizę również o odpowiednie moduły:

* `/backend`
* `/frontend`

Analizuj wyłącznie te części projektu, które mają wpływ na implementowaną funkcjonalność. Nie ma potrzeby analizowania całego repozytorium, jeżeli zmiana dotyczy jednego modułu lub komponentu.

Przed implementacją przeanalizuj odpowiednio do zakresu zadania:

* strukturę katalogów,
* architekturę modułów,
* podział odpowiedzialności,
* zależności pomiędzy komponentami,
* przepływ danych,
* sposób komunikacji pomiędzy frontendem i backendem,
* konfigurację projektu,
* sposób obsługi błędów,
* mechanizmy logowania,
* sposób dostępu do danych,
* istniejące klasy, funkcje, komponenty React i interfejsy,
* obowiązujące wzorce projektowe,
* styl kodowania,
* istniejące testy dotyczące analizowanego obszaru.

Przed napisaniem nowego kodu wyszukaj istniejące implementacje rozwiązujące podobny problem. W pierwszej kolejności wykorzystuj i rozszerzaj istniejące komponenty zamiast tworzyć nowe.

---

# Organizacja kodu

Kod powinien pozostawać zgodny z architekturą projektu oraz być łatwy do rozwijania.

Przestrzegaj zasad:

* Single Responsibility Principle,
* DRY,
* KISS,
* SOLID tam, gdzie ma to uzasadnienie.

Preferuj:

* małe, wyspecjalizowane moduły,
* czytelne interfejsy,
* separację logiki biznesowej od warstw technicznych,
* ponowne wykorzystanie istniejących komponentów.

Nie twórz katalogów ani plików będących "magazynem przypadkowego kodu", takich jak:

* `utils`
* `helpers`
* `common`
* `shared`
* `misc`
* `temp`
* `lib` (jeżeli miałby pełnić rolę katalogu na niepowiązany kod)

Nowe katalogi twórz wyłącznie wtedy, gdy reprezentują konkretny obszar odpowiedzialności wynikający z architektury projektu.

Jeżeli w projekcie istnieją już katalogi o powyższych nazwach, dodawaj do nich kod wyłącznie wtedy, gdy jest on zgodny z ich obecną odpowiedzialnością i sposobem organizacji. Nie wykorzystuj ich jako miejsca na dowolny nowy kod.

Każdy nowy moduł, komponent React, klasa lub plik powinien mieć jednoznacznie określoną odpowiedzialność i naturalnie wpisywać się w istniejącą strukturę projektu.

Nie przenoś plików ani nie reorganizuj katalogów wyłącznie z powodów estetycznych. Wprowadzaj możliwie najmniejszy zakres zmian niezbędny do realizacji zadania.



---

# Frontend i komponenty UI

Frontend powinien wykorzystywać istniejący system komponentów oraz obowiązujące standardy projektu.

Przestrzegaj zasad:

* korzystaj z komponentów dostępnych w projekcie zamiast tworzyć własne odpowiedniki,
* dla elementów interfejsu użytkownika preferuj komponenty z biblioteki **shadcn/ui**, jeżeli projekt już z niej korzysta,
* jeżeli wymagany komponent nie istnieje w aktualnej instalacji shadcn/ui, dodaj go zgodnie z oficjalnym sposobem instalacji i strukturą projektu,
* nie implementuj ręcznie komponentów, które są dostępne lub mogą zostać dodane przez shadcn/ui,
* zachowuj spójność wizualną aplikacji poprzez wykorzystanie istniejących wariantów, stylów i tokenów projektowych.

Przed utworzeniem nowego komponentu UI sprawdź:

* czy odpowiedni komponent istnieje już w projekcie,
* czy można rozszerzyć istniejący komponent,
* czy wymagany element jest dostępny w shadcn/ui.

Nowe komponenty React twórz wyłącznie wtedy, gdy:

* reprezentują konkretną odpowiedzialność biznesową,
* nie są prostym wrapperem na istniejący komponent UI,
* ich wydzielenie poprawia czytelność lub możliwość ponownego użycia.

Unikaj tworzenia własnych rozwiązań UI zastępujących standardowe komponenty biblioteki.