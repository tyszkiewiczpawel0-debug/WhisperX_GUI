# Decyzje — 14.10.2026

| ID | Status | Decyzja / uzasadnienie |
|---|---|---|
| D-01 | Zatwierdzone przez użytkownika | Kontrakt v1.0 APPROVED nadrzędny; D0 formalnie odebrany 14.10.2026, D1 autoryzowany w załączonym zleceniu. Brak zgody na D2 w tym zleceniu |
| D-02 | Wykonawcza D1 | Git lokalny, main, bez remote/push; obowiązujący kontrakt przeniesiony bez zmiany bajtów do docs/PROJECT_CONTRACT.md |
| D-03 | Wykonawcza D1 | Raporty D0 i standard pozostają w root jako materiały historyczne/referencyjne. Aktualny status jest w CURRENT_STATE i handoffie |
| D-04 | Wykonawcza D1 | TOML zamiast .env jako równoważny wzór; tomllib w Python 3.11 eliminuje potrzebę nowej zależności. Lokalny plik ignorowany |
| D-05 | Zlecenie D1 | Jeden profil WEBINAR_RUI_PL: large-v3/pl/cuda/float16/batch 8/alignment=true/diarization=false. Wartości startowe do testów, nie certyfikacja pipeline |
| D-06 | Rekomendacja D0 | Tkinter, osobny proces, adapter Python API, reuse venv/modeli/writerów. Dokumentacja nie traktuje tego jako zaimplementowanego rozwiązania |
| D-07 | Wykonawcza D1 | src i tests zawierają opis odpowiedzialności i plan kontroli; brak pustych modułów, klas i atrap. Manifest pakietów jest snapshotem, nie lockfile ani autoryzacją instalacji |

Przed D2: użytkownik odbiera D1 i autoryzuje implementację, rozstrzyga proponowany wariant integracji, politykę pośrednich/próg długości oraz zakres dozwolonych testów wykonawczych. Nie wymagają ponownego rozstrzygania drobne decyzje organizacyjne już objęte D1. Brak modeli/zależności w późniejszej weryfikacji wymaga osobnej decyzji o instalacji/pobraniu, a nie automatycznej naprawy. D3 wymaga dostarczenia nagrania RUI i autoryzacji pilotażu.

## D2 — autoryzacja i wykonanie 14.10.2026

Powyższe wpisy D1 są historyczne. Zlecenie użytkownika „D2: IMPLEMENTACJA MVP — AUTHORIZED” potwierdziło odbiór D0/D1, architekturę oraz zgodę na implementację, krótkie testy i lokalne commity. Zastępuje wcześniejsze oczekiwanie na autoryzację D2; nie otwiera D3.

| ID | Status | Decyzja / uzasadnienie |
|---|---|---|
| D-08 | Użytkownik D2 | Tkinter, istniejący Python w osobnym procesie, adapter API, FFprobe/FFmpeg i writery WhisperX; krótki test lokalny dozwolony |
| D-09 | Wykonawcza D2 | Zachować wszystkie pośrednie także po sukcesie; prostsza diagnostyka, brak automatycznego usuwania danych |
| D-10 | Użytkownik / wykonawcza D2 | Próg ostrzeżenia długości 0,1 s w TOML; odrzucać wiele ścieżek i offset >0,1 s, mniejsze offsety jawnie raportować |
| D-11 | Wykonawcza D2 | Jedna konfiguracja profilu; model/język large-v3/pl, edytowalne urządzenie, compute, batch i alignment, bez cichego fallbacku |
| D-12 | Wykonawcza D2 | Job Object z handshake przed pracą i kill-on-close; potwierdzono zabicie potomnego FFmpeg bez wpływu na niezależny proces |
| D-13 | Wykonawcza D2 | Konkretne lokalne snapshoty, preflight NLTK/CUDA, HF offline, blokada nltk.download i audit hook; cache tymczasowe w katalogu zadania |
| D-14 | Wykonawcza D2 | Nowy UUID dla każdej inspekcji/przygotowania/transkrypcji; pełna transkrypcja ponownie przygotowuje własny WAV z oryginału |
| D-15 | Wykonawcza D2 | Lokalny output w ignorowanym runs/jobs, prywatny TOML; bez kopiowania środowiska/modeli i bez instalacji |
| D-16 | Obserwacja D2 | TorchCodec ostrzega o niedostępnych DLL; używany pipeline FFmpeg + waveform działa. Nie zmieniamy środowiska na podstawie samego ostrzeżenia |

D2 jest gotowy do odbioru na podstawie krótkiego testu. D3 wymaga osobnej autoryzacji i wskazania webinaru. Jakość mowy, synchronizacja początku/środka/końca oraz RAM/VRAM długiego materiału pozostają zadaniem pilotażu. Nie wyciągamy z 20 s wniosku o wydajności całego webinaru ani o wszystkich kombinacjach parametrów.

## Poprawka launchera D2 — 14.10.2026

D-17 (wykonawcza, autoryzowana poprawka D2): Start.ps1 pozostaje ASCII, zgodne zarówno z Windows PowerShell 5.1, jak i PS7 bez zależności od BOM. Konfigurację czytamy jawnie jako UTF-8; Start.cmd wskazuje systemowy Windows PowerShell 5.1. Bez instalacji PS7 i zmian globalnych Windows. Rzeczywistym źródłem zgłoszonego błędu było odczytanie UTF-8 jako CP1250; wcześniejszy test PS7 nie pokrywał launchera.

D-18: Błędy konfiguracji przed otwarciem GUI trafiają do konsoli zachowanej przez pause; kod 1 przechodzi przez Python, PowerShell i CMD. Unikamy startowego modalu z ukrytym rodzicem, który w teście nie był widoczny. Błędy podczas pracy GUI pozostają bez zmian. Testy launchera nie uruchamiają silnika; wadliwe konfiguracje znajdują się w osobnych katalogach i nie zastępują local.toml użytkownika. Nie rozpoczynamy D2.1/D3.

## D2.1 — autoryzacja i wykonanie 14.10.2026

Powyższe stany są historyczne. Zlecenie użytkownika „D2.1: INITIAL PROMPT — AUTHORIZED” formalnie zatwierdza D2 i autoryzuje implementację promptu, proporcjonalne testy oraz lokalne commity. D3 nadal wymaga odrębnej zgody.

- D-19 (użytkownik): opcjonalny initial_prompt w profilu, edycja tylko dla uruchomienia, bez zarządzania promptami i zmiany innych parametrów.
- D-20 (wykonawcza, potwierdzone lokalne API): przekazanie przez load_model/asr_options; str/None, bez list tokenów i zastępowania mechanizmem hotwords. Profil pozostaje schema_version=1, pole opcjonalne, dostarczona wartość pusta.
- D-21 (wykonawcza): brak/null/pusty/białe znaki → None; pozostały tekst zachowany dokładnie. Nie przycinamy tekstu w GUI ani adapterze; biblioteczna tokenizacja ma własne ograniczenie kontekstu.
- D-22 (wykonawcza): oddzielić parameters.initial_prompt od głównego initial_prompt i stanu not_submitted/submission_unconfirmed/accepted_by_engine. Nie deklarować przyjęcia opcji po nieudanym ładowaniu; anulowanie zachowuje ostatni trwały stan. Bez pełnego promptu w logach aplikacji.
- D-23 (weryfikacja): ukierunkowane testy plus pojedynczy przebieg lokalnej próbki D2 z promptem; bez pełnego webinaru, powtarzania macierzy GPU i zmian środowiska. Odbiór D2.1 należy do użytkownika.

## D3 — autoryzacja i pilotaż 14.10.2026

- D-24 (użytkownik): zlecenie D3 potwierdza odbiór D0–D2.1, autoryzuje jeden pełny pilotaż nagrania RUI z INPUT, prompt terminologiczny, diagnostykę i lokalny checkpoint/Git. Nie otwiera D4 ani zgody na pobieranie/zmianę środowiska.
- D-25 (wykonawcza): wykorzystano istniejący kontroler i pełny pipeline bez zmian kodu; jeden przebieg succeeded. Prompt dotyczy uruchomienia, profil i local.toml pozostają bez zmian. Nie powtarzano ASR dla pomiarów lub porównania promptu.
- D-26 (obserwacja): ostatni segment/słowo 23,688 ms poza WAV, w istniejącej tolerancji 100 ms; wyniki zachowano bez przycinania. Struktura i wzajemna zgodność eksportów potwierdzone, ścisła granica audio nie jest PASS.
- D-27 (ograniczenie): D3 PARTIAL z powodu niewykonanej kontroli akustycznej. Przegląd tekstu i timestampów nie zastępuje odsłuchu ani oceny kompletności. Podejrzane fragmenty początku, przerwy i zakończenie wskazano w raporcie do odsłuchu. Nie testowano widocznego GUI podczas pełnego przebiegu D3; RAM niedostępny, VRAM tylko punktowo dla całej karty.
- D-28 (bramka): raport i jeden bieżący handoff do oceny użytkownika; D4 nie rozpoczęto. Nie przyjmujemy własnego sukcesu technicznego jako odbioru jakości lub MVP.

## D4 — autoryzacja, odbiór D3 i rekomendacja 14.10.2026

Wpisy D-24–D-28 i raport D3 opisują stan historyczny przed kontrolą użytkownika. Poniższe decyzje zastępują ówczesne oczekiwanie na odsłuch i autoryzację D4.

- D-29 (użytkownik, zlecenie D4): D0, D1, D2 po poprawce launchera Windows PowerShell, D2.1 i D3 APPROVED; D4 AUTHORIZED wyłącznie jako ocena, dokumentacja i lokalny commit. Bez zmian implementacji, środowiska, kontraktu lub standardu i bez nowej transkrypcji.
- D-30 (użytkownik): odsłuch 06:20–07:20, 58:00–59:00 i 1:42:00–1:43:00 potwierdził akceptowalną treść, kompletność i synchronizację tych fragmentów; D3 APPROVED. Pierwotne PARTIAL Work pozostaje historycznym faktem. Nie zweryfikowano wszystkich 11903 słów.
- D-31 (obserwacje użytkownika): cisza/szumy 01:30–03:40 i pożegnania z wysokim prawdopodobieństwem będące halucynacjami; słyszalne echo, podejrzenie aktywnego mikrofonu laptopa bez potwierdzenia przyczyny. Ograniczenia nie zablokowały odbioru; oryginalne wyniki pozostają bez zmian.
- D-32 (ocena wykonawcza D4): dziewięć kryteriów kontraktu: 6 PASS, 3 PARTIAL, 0 FAIL. Niepełne dowody pełnego przebiegu przez widoczne GUI, responsywności podczas silnika i przeniesienia na inne stanowisko. Szczegóły i granice PASS: [raport D4](D4_MVP_REVIEW.md).
- D-33 (rekomendacja, nie decyzja użytkownika): zamknąć MVP dla sprawdzonego stanowiska/profilu przy świadomej akceptacji trzech PARTIAL; w razie wymogu pełnego wykonawczego PASS pozostawić zamknięcie otwarte do osobno zleconej weryfikacji. Nie zmienia to kontraktu. Formalna decyzja wyłącznie w głównej rozmowie ChatGPT.
- D-34 (wykonawcza D4): jeden raport D4 i jeden bieżący handoff; historyczne raporty zachowane, ARCHITECTURE/DATA aktualne bez potrzeby zmiany. Propozycje rozwoju nie stanowią autoryzacji ani standardu Ekosystemu. D4 COMPLETE wykonawczo; po lokalnym commicie zakończyć pracę.

## Zamknięcie i utrwalenie repozytorium — 14.10.2026

- D-35 (użytkownik, zlecenie końcowego przeglądu): MVP v1 CLOSED / D4 APPROVED, 6 PASS / 3 PARTIAL / 0 FAIL. Zastępuje oczekiwanie na odbiór w D-33/D-34 i historycznym raporcie D4; bez zmiany trzech PARTIAL lub otwierania dalszego rozwoju.
- D-36 (użytkownik): jednorazowy przegląd, niezbędne uzupełnienia, lekka weryfikacja, lokalny commit i nowy tag mvp-v1.0; po pozytywnym przeglądzie bezpieczeństwa autoryzowane prywatne repozytorium GitHub WhisperX_GUI i push main oraz tego tagu. To odrębna autoryzacja zastępująca wcześniejszy brak zgody na remote/push; bez nadpisywania historii/tagów i bez repozytorium publicznego.
- D-37 (wykonawcza): kod, profil i środowisko bez zmian. Zachować raporty historyczne, uzupełnić status, wymagania/reuse i jeden bieżący handoff; zweryfikować jego odnośniki do korzenia. Git nie stanowi kopii zapasowej ignorowanych danych ani gotowej instalacji środowiska.
