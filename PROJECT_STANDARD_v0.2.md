# EKOSYSTEM — PROJECT STANDARD v0.2

**Status:** DRAFT / PILOT  
**Pierwszy projekt pilotażowy:** Progman Kadry

## 1. Zasada nadrzędna

Każdy istotny projekt powinien być możliwy do zrozumienia, wznowienia i bezpiecznego rozwijania bez odtwarzania wiedzy z historii rozmów.

Repozytorium jest trwałym źródłem prawdy o projekcie.

## 2. Minimalna dokumentacja

Poważniejszy projekt powinien posiadać co najmniej:

- `README.md` — mapa projektu,
- `AGENTS.md` — zasady bezpiecznej pracy AI,
- `docs/PROJECT_CONTRACT.md` — cel, granice, wejścia, wyjścia i ryzyka integracyjne,
- `docs/CURRENT_STATE.md` — bieżący snapshot,
- `docs/ARCHITECTURE.md` — komponenty i przepływy,
- `docs/DATA.md` — źródła i cykl życia danych,
- `docs/DECISIONS.md` — istotne decyzje i ich uzasadnienia.

Dokumentów nie tworzymy wyłącznie po to, aby były puste.

## 3. Dane

Projekty pracujące na istotnych danych rozróżniają co najmniej:

- SOURCE / RAW,
- DERIVED,
- WORKING,
- OUTPUT.

Istotnych danych źródłowych nie modyfikujemy w miejscu.

Preferowany model:

ORIGINAL → SNAPSHOT → DERIVED DATA → ANALYSIS

Dane osobowe, produkcyjne bazy i sekrety nie trafiają do Git tylko dlatego, że należą do projektu.

## 4. Provenance

Dla istotnych wyników powinno być możliwe ustalenie:

RESULT → PROCESS / VERSION → SOURCE

## 5. Git i weryfikacja

- domyślna gałąź: `main`,
- małe logiczne commity,
- ważny checkpoint kończymy możliwie czystym working tree,
- przed commitem wykonujemy właściwą dla projektu weryfikację,
- sekrety i duże wygenerowane dane są ignorowane.

Każdy projekt musi dokumentować, jak sprawdzić, że nadal działa.

## 6. Handoff do AI

Preferowany katalog:

`99_HANDOFF/CURRENT/`

Handoff ma być minimalnym zestawem potrzebnym do przekazania aktualnego etapu pracy.

Markdown służy do narracji technicznej i kontekstu, JSON do kompletnych danych strukturalnych, a CSV wtedy, gdy potrzebna jest ręczna praca tabelaryczna.

## 7. Wiedza nie może istnieć tylko w czacie

Po istotnym etapie należy zadać pytanie:

> Czy gdyby rozmowa zniknęła, repozytorium wystarczyłoby do wznowienia projektu?

Jeżeli nie, należy zaktualizować repozytorium.

## 8. Kandydaci do Ekosystemu

Pierwsze wystąpienie rozwiązania nie jest jeszcze wspólnym komponentem.

Preferowany cykl:

lokalne rozwiązanie → sprawdzony wzorzec → ponowne użycie → kandydat → wspólny komponent

## 9. Przenośność / nowe stanowisko

Każdy poważniejszy projekt musi umieć odpowiedzieć:

> Co mam zrobić, gdy otwieram ten projekt na innym komputerze?

README powinien zawierać sekcję `Uruchomienie na nowym stanowisku`.

Instrukcja ma prowadzić od pobrania repozytorium do działającej i zweryfikowanej instancji projektu i obejmować odpowiednio:

1. pobranie repozytorium,
2. wymagania środowiskowe,
3. odtworzenie zależności,
4. wskazanie danych lokalnych,
5. utworzenie lokalnej konfiguracji,
6. uruchomienie,
7. test weryfikacyjny.

Jeżeli projekt używa zmiennych środowiskowych, repo powinno zawierać `.env.example`. Właściwy `.env` nie trafia do Git.

README powinien wyjaśniać, które dane nie są przechowywane w repozytorium, gdzie projekt oczekuje ich lokalnie i skąd można je pozyskać.

Bezwzględna ścieżka konkretnego stanowiska nie może być ukrytą częścią logiki aplikacji.

Przeniesienie projektu na drugi komputer ma być uruchomieniem kolejnego stanowiska, nie ręczną migracją.

## 10. Projekty analizujące istniejącą bazę danych

Dodatkowo:

- oryginalna baza jest nietykalna,
- analiza odbywa się na kontrolowanym snapshotcie,
- snapshot ma zapisane źródło, datę, rozmiar i hash,
- discovery jest oddzielone od interpretacji,
- ważne ustalenia zachowują evidence umożliwiające powrót do tabeli, pola, rekordu, relacji lub zapytania.

## 11. Kryterium dobrego repozytorium

Nowy człowiek lub agent AI powinien bez poprzedniego czatu umieć odpowiedzieć:

1. Co to jest?
2. Dlaczego istnieje?
3. Jaki jest zakres?
4. Na czym obecnie stoimy?
5. Gdzie są źródła prawdy?
6. Jakie dane wykorzystuje?
7. Jak działa na poziomie architektury?
8. Jak sprawdzić, że działa?
9. Jakich rzeczy nie wolno naruszyć?
10. Jaki jest następny krok?
11. Jak uruchomić projekt na innym komputerze?

Standard pozostaje pilotażowy i ma być korygowany na podstawie realnej pracy.
