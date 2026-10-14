# D4 — ocena MVP, 14.10.2026

**D4: COMPLETE wykonawczo, do odbioru. Formalne zamknięcie MVP oczekuje na decyzję użytkownika w głównej rozmowie ChatGPT.** D0, D1, D2 (po poprawce launchera Windows PowerShell), D2.1 i D3: APPROVED według zlecenia D4 z 14.10.2026. Kontrakt v1.0 pozostaje bez zmian.

## Kryteria rozdziału 8 kontraktu

Ocena dotyczy dostępnych dowodów; PARTIAL oznacza niepełne potwierdzenie, nie automatycznie usterkę. Podstawa: [kontrakt](PROJECT_CONTRACT.md), [D2](D2_TEST_REPORT.md), [D2.1](D2_1_TEST_REPORT.md), [D3](D3_PILOT_REPORT.md), odczyt launcherów/GUI/kontrolera i istniejących dowodów D3. Bez nowych testów silnika.

| # | Kryterium | Ocena | Dowód i ograniczenie |
|---|---|---|---|
| 1 | Pełna transkrypcja z GUI bez ręcznych komend | PARTIAL | D2 potwierdza Start.cmd → PowerShell 5.1 → rzeczywiste GUI, D2.1 widgety i przekazanie parametrów; GUI wywołuje ten sam Controller.start, który ukończył D3. Użytkownik zatwierdził D2 po poprawce. Brak udokumentowanego pełnego przebiegu sterowanego przez widoczne GUI; nie utożsamiamy testów części z takim odbiorem. |
| 2 | WEBINAR_RUI_PL działa i zapisuje rzeczywiste parametry | PASS | D2.1 i D3: large-v3/pl/cuda/float16/batch 8/alignment, bez diarizacji; run.json zawiera parametry i accepted_by_engine dla promptu. Nie dowodzi to poprawy jakości przez prompt. |
| 3 | Nienaruszony oryginał | PASS | D3: identyczny SHA-256 przed/po; integrity.json potwierdza też niezmienność konfiguracji. Kontrola 46565 plików źródła porównywała ścieżki/rozmiary/mtime_ns, nie pełne hashe instalacji. |
| 4 | Komplet wyników i przewidywalna struktura | PASS | D3: TXT/SRT/JSON/run.json/process.log, 748 segmentów, 11903 słowa; zgodność eksportów. D2: osobne katalogi i ponowienie bez nadpisania. Ostatni koniec +23,688 ms poza WAV mieści się w tolerancji aplikacji 100 ms; ścisła kontrola granicy WAV nie przeszła. |
| 5 | Responsywność podczas pracy silnika | PARTIAL | Osobny worker, kolejka i ograniczony poll GUI; D2: zdarzenia Tkinter co <0,5 s podczas przygotowania. Test nie mierzył responsywności podczas ASR/alignmentu; pełny D3 odbył się bez widocznego GUI. |
| 6 | Błędy prezentowane i rejestrowane | PASS | D2/D2.1: błędy wejścia, konfiguracji i workera, trwałe stany błędu/anulowania; GUI pokazuje błędy zadania, run.json/process.log je utrwalają. Błędy przed utworzeniem zadania są komunikatami GUI lub konsoli launchera, bez dziennika zadania. OOM, pełny dysk i awaria zasilania nieprzetestowane. |
| 7 | Możliwość ustalenia wersji narzędzi | PASS | Manifest D3 zawiera wersje narzędzi, rewizje modeli i hashe kodu; snapshot pakietów w repozytorium. Snapshot nie jest lockfile. |
| 8 | Zweryfikowany pilotaż i udokumentowane ograniczenia | PASS | Techniczne kontrole D3 oraz późniejszy odsłuch trzech fragmentów przez użytkownika i jego APPROVED. Kontrakt przewiduje ocenę wybranych fragmentów; nie wykonano pełnej kontroli 11903 słów ani porównania prompt/bez promptu. |
| 9 | Odtworzenie konfiguracji i uruchomienie na innym stanowisku | PARTIAL | README, local.example.toml, profil, snapshot pakietów, opis zasobów offline i launcher dostępne. Brak testu drugiego stanowiska i sprawdzonej instalacji od zera; instrukcja wymaga istniejącego zgodnego stosu. |

**Wynik: 6 PASS, 3 PARTIAL, 0 FAIL.** Nie wykryto potwierdzonej blokującej usterki aplikacji. Nie jest to stwierdzenie pełnego wykonawczego potwierdzenia wszystkich kryteriów kontraktu.

## Odbiór D3 i jakość

Pierwotny raport Work miał status PARTIAL z powodu braku odsłuchu. Następnie użytkownik sprawdził treść, kompletność i synchronizację w 06:20–07:20, 58:00–59:00 i 1:42:00–1:43:00. Uznał wynik za akceptowalny i zatwierdził D3. To selektywna kontrola, nie weryfikacja wszystkich 11903 słów, wszystkich przerw lub całej osi czasu.

Według użytkownika 01:30–03:40 zawiera głównie ciszę i szumy; wygenerowane tam formuły pożegnalne uznano z wysokim prawdopodobieństwem za halucynacje. Słychać echo. Aktywny mikrofon laptopa jest podejrzeniem użytkownika, nie ustaloną przyczyną. Ograniczenia te nie przeszkodziły mu w odbiorze D3. Wyników transkrypcji nie poprawiano.

## Klasyfikacja ograniczeń

1. **Aplikacja i zakres weryfikacji:** rzeczywisty błąd kodowania launchera został naprawiony w D2 i zaakceptowany. Brak nowej potwierdzonej usterki blokującej. Pozostają trzy PARTIAL z tabeli. Eksporty nie są jedną transakcją; po awarii rozstrzyga manifest, a przerwanie całego systemu może pozostawić running. Nie testowano pełnego dysku/OOM/utraty zasilania. Tolerancja końca napisów 100 ms jest jawna, bez korekty wyników.
2. **WhisperX i stos:** halucynacje na ciszy/szumach, możliwe błędy nazw i terminologii; brak pełnej listy błędów potwierdzonych odsłuchem. Prompt nie gwarantuje poprawności. Całe audio trafia do RAM. D3 potwierdził jeden materiał 1:58:43 w 196,781 s, nie dowodzi wydajności dowolnie długich nagrań. RAM nie zmierzono; 9309/16303 MiB to największa punktowa próbka całej karty, nie szczyt procesu. TorchCodec ostrzega o DLL, pyannote o TF32, Lightning adaptuje checkpoint w pamięci; nie zablokowało to FFmpeg → audio w pamięci. Brak podstaw do automatycznej zmiany środowiska.
3. **Nagranie:** cisza, szumy i echo ograniczają jakość rozpoznawania. Techniczna przyczyna echa i jego ilościowy wpływ pozostają niepotwierdzone; nie przypisujemy ich usterce GUI.
4. **Poza MVP:** wiele profili, kolejka, diarizacja, streszczenia/analiza treści, wznowienia i dodatkowe eksporty nie są brakami kryteriów MVP. Wiele ścieżek audio i duże offsety są jawnie odrzucane. CPU/inne compute, inne GPU, pełny przebieg bez alignmentu i wszystkie kodeki nie mają pełnej weryfikacji.

## Ewentualny dalszy rozwój — bez implementacji i autoryzacji

| Propozycja | Uzasadnienie i praktyczne znaczenie |
|---|---|
| Wiele profili i wygodniejsza konfiguracja | Dziś jeden profil i ręczne ścieżki TOML; przy kolejnych zastosowaniach ograniczyłoby to powtarzanie ustawień i pomyłki. |
| Oznaczanie podejrzanych fragmentów | Pożegnania na ciszy ujawnione w D3 uzasadniają pomoc w wyborze miejsc do odsłuchu, bez automatycznego usuwania tekstu. |
| Wsparcie przygotowania nagrań | Kontrola toru nagrywania i próbka odsłuchowa przed webinarami mogą ograniczyć echo/szum; ewentualne przekształcenia tylko w kopii, z zachowaniem osi czasu. |
| Dodatkowy eksport VTT/TSV | D0 wskazało istniejące writery; warto wykorzystać je dopiero przy konkretnej potrzebie odtwarzacza lub dalszej pracy z danymi. |

Uzupełnienie dowodów GUI podczas ASR i uruchomienia na drugim stanowisku byłoby weryfikacją obecnych wymagań, nie nową funkcją. W D4 nie wykonujemy tych prac.

## Repozytorium i rekomendacja

Punkt wyjścia: main, 9fdcd0c, czysty working tree, brak remote. Sprawdzono listę śledzonych plików oraz reguły ignore dla konfiguracji lokalnej, nagrań, wyników, modeli i sekretów; nie znaleziono przypadkowo wersjonowanych danych tych kategorii. Przed commitem kontrola diff, odwołań i zakresu dokumentacji. Identyfikator końcowego commita i status po nim podano w handoffie do użytkownika; commit można odnaleźć po tytule `Document D4 MVP review and closure recommendation`.

Architektura i DATA odpowiadają implementacji D2.1, nie wymagają przepisywania. Historyczne raporty D0–D3 zachowano; aktualne statusy określają ten raport, CURRENT_STATE, DECISIONS i bieżący handoff. Stare ścieżki kontraktu w narracji D0 dotyczą ówczesnego układu, obecnie obowiązuje docs/PROJECT_CONTRACT.md. Nie analizowano projektu pilotażowego standardu ani nie zmieniano standardu/kontraktu.

**Rekomendacja: zamknąć MVP dla sprawdzonego stanowiska i profilu, jeżeli użytkownik świadomie akceptuje trzy wskazane luki dowodowe PARTIAL.** Implementacja i pilotaż są zakończone i zatwierdzone; narzędzie spełniło praktyczny cel D3. Jeżeli wymagane jest wykonawcze PASS dla każdego kryterium, pozostawić formalne zamknięcie otwarte do osobno zleconego uzupełnienia dowodów #1, #5 i #9. Nie przedstawiamy ograniczenia do obecnego stanowiska jako zmiany kontraktu.

D4 nie zamyka MVP samodzielnie. Ostateczna decyzja należy do użytkownika w głównej rozmowie ChatGPT. W D4 wyłącznie odczyt i dokumentacja: bez zmiany kodu, źródłowego WhisperX, konfiguracji, nagrań, wyników i środowiska; bez przetwarzania, instalacji, pobierania lub push. Nie wykonywano nowego pełnego audytu integralności źródła; podstawą historyczną pozostaje kontrola D3. Dalszych prac nie rozpoczęto.
