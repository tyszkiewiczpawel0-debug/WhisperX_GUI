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


## Analiza kolejnej wersji — 18.10.2026

- D-38 (użytkownik, bieżące zlecenie): analiza aktualnego repozytorium i tagu, wielu profili, sesja_rady_gminy i osi czasu; dokumenty i nieinwazyjne testy dozwolone. Bez implementacji, zmian środowiska, pełnej transkrypcji i publikacji. Nie otwiera nowej fazy wykonawczej i nie zmienia zamkniętego MVP.
- D-39 (obserwacja): czysty wejściowy main/HEAD równy mvp-v1.0, a677fc6f62620752156fd2565edac6e3585090e0. Kod zgodny z technicznym opisem dostarczonego handoffu XXV; jego eksperymentów nie powtarzano. Wcześniejszy brak origin w handoffie jest nieaktualny lokalnie; stan zdalny i prywatność nie były sprawdzane.
- D-40 (rekomendacja, DO ZATWIERDZENIA): jawny rejestr dwóch profili i wybór GUI; domyślnie webinar, bez zmiany jego JSON, walidacji parametrów i polecenia FFmpeg. Snapshot rzeczywistych parametrów z parameters.id wystarcza do identyfikacji w request/run.
- D-41 (rekomendacja, DO ZATWIERDZENIA): wspólny mechanizm przygotowania z polityką deklarowaną przez profil, stary wariant przy braku opcji, filtr aresample=16000:async=1:first_pts=0 dla sesji. Nie ustanowiono kontraktu audio_timeline_mode; reprezentacja i metadane do zatwierdzenia przed wdrożeniem.
- D-42 (ograniczenie): filtrowany WAV XXV według handoffu jest o 112 ms krótszy od kontenera. To nie dowód pełnej synchronizacji ani wynik własnego pomiaru. Odbiór wymaga wskazanego materiału i punktów referencyjnych; proponowany cel 100 ms oraz edytowalność alignmentu sesji pozostają do decyzji.
- D-43 (weryfikacja): 16 istniejących testów PASS, prawdziwe writery i blokady PASS, AST/config PASS, bez ASR/pobrań/zmian źródła. Dokumenty NEXT_VERSION_ANALYSIS i NEXT_VERSION_IMPLEMENTATION_PLAN oraz jeden bieżący handoff. ANALYSIS COMPLETE — IMPLEMENTATION PENDING APPROVAL; bez własnego odbioru Work.

## Implementacja kolejnej wersji — 18.10.2026

- D-44 (użytkownik, IMPLEMENTATION AUTHORIZED): zatwierdza wykonanie wieloprofilowości, sesja_rady_gminy, GUI/snapshotów i lokalnych testów/commitów na gałęzi roboczej. Alignment sesji edytowalny. AUDIO-01 jest wskazanym materiałem; poprzedni problem XXV dotyczył materiału łączonego, więc nie zakładać takiej samej wady aktualnego pojedynczego MP4. Opcjonalny preserve tylko po uzasadnieniu testami, bez przełącznika GUI i automatycznego wyboru. Bez pełnej transkrypcji, instalacji, modyfikacji źródła i publikacji. Zastępuje oczekiwanie na zgodę w D-38–D-43; nie zmienia zamkniętego MVP.
- D-45 (wykonawcza): jawny rejestr dwóch stałych JSON; profile() nadal webinar, profile(id) waliduje ID pliku. Wybór GUI resetuje formularz i nie zapisuje profilu, jest blokowany podczas pracy. Parametry snapshotu nadal przez parameters.id, bez profile_id. Webinarowy JSON bajtowo niezmieniony.
- D-46 (obserwacja i rekomendacja oparta na teście): AUDIO-01 ma 5884,600 s, audio 5884,501 s; legacy WAV 5884,096 s i wyprzedzenie zdarzeń o 109/213/405 ms. Preserve WAV 5884,501 s, pięć zdarzeń zgodnych z osią MP4 przy rozdzielczości 0,0625 ms. Trzy wydłużone duration pakietów AAC sumują się do 405 ms, bez przerw PTS >1 ms. To uzasadnia opcję preserve dla tego pliku, nie dowodzi jego łączenia ani poprawności dla każdego źródła.
- D-47 (wykonawcza, koryguje wcześniejszą rekomendację D-41): opcjonalne audio_timeline_mode=legacy|preserve, brak → legacy, inna wartość to błąd; oba dostarczone profile pozostają legacy. Preserve wymaga jawnej konfiguracji; faktyczne wykonanie, filtr i długości zapisuje preparation, zamiar parameters. Nie dopełniać końcowych 99 ms do wideo, nie przesuwać eksportów. Nazwy addytywnych pól opisano w DATA.
- D-48 (wykonawcza poprawka ujawniona testem): jawna odmowa istniejącego target WAV oraz ograniczone ponawianie atomowego replace manifestu na Windows WinError 5/32/33 (5 prób, łącznie 0,30 s), bez usuwania poprzedniego JSON lub maskowania trwałego błędu. Poprawka cykli Tk dotyczy testów, nie architektury GUI. Bez nowych zależności.
- D-49 (weryfikacja): końcowo 22/22 testów PASS, prawdziwe eksporty/offline PASS, 20-sekundowy rzeczywisty ASR sesji/preserve succeeded (4 segmenty, 29/29 słów z czasami), anulowanie aktywnego FFmpeg PASS. SHA-256 AUDIO-01 i hashe webinarowego JSON/local.toml bez zmian; 46565 plików źródła bez zmian ścieżek/rozmiarów/mtime_ns (nie pełny hash instalacji). NOT TESTED: widoczny GUI podczas ASR, odsłuch/lip-sync i jakość przez użytkownika, ponowne rzeczywiste anulowanie ASR/alignmentu, osobny ASR webinaru, inne compute/CPU i drugie stanowisko. Szczegóły i lokalne dowody w NEXT_VERSION_IMPLEMENTATION_PLAN.
- D-50 (checkpoint, nie odbiór): gałąź codex/multiple-profiles; analiza utrwalona w 23d0786, kod w 459fd15b7e84892762aab972fb80a3556f54275f, po nim dokumentacyjny checkpoint. IMPLEMENTATION COMPLETE — PENDING ACCEPTANCE. Rekomendacja gotowości dotyczy opisanego zakresu i ograniczeń; odbiór należy do użytkownika/głównej rozmowy. Bez push i nowego tagu.


## Finalizacja v1.1.0 — 18.10.2026

- D-51 (użytkownik, FINALIZATION AUTHORIZED): pozytywny odbiór funkcjonalny GUI (start, dwa profile, reset po przełączeniu, responsywność podczas rzeczywistego WhisperX) i potwierdzony pełny AUDIO-01 succeeded z wymaganymi wynikami. Przebieg korzystał z legacy i ostrzegł −405 ms. Nie przypisywać tego dowodu preserve. Zgoda obejmuje finalizację, lokalne commity, integrację z main i nowy lokalny tag, bez push/publikacji i dalszego rozwoju.
- D-52 (zatwierdzone przez użytkownika): sesja_rady_gminy domyślnie preserve przez jawne pole JSON. Zastępuje domyślne legacy sesji w D-47; webinarowy JSON bajtowo niezmieniony i legacy, brak pola nadal legacy dla każdego ID. Bez globalnej zmiany i przełącznika GUI. Uzasadnienie: wcześniejsze pięć zdarzeń AUDIO-01 (legacy do 405 ms przesunięcia, preserve zgodny w granicach pomiaru).
- D-53 (weryfikacja finalizacji): 23/23 testy PASS na gałęzi roboczej, 6,585 s; rzeczywiste writery/JSON/offline PASS. Dodano sprawdzenie domyślnych trybów w request/run realnego workera prepare bez nadpisania; GUI A → B → A sprawdza również tryb. Brak pola=legacy nadal testowane. Produkcyjny src bez zmian; bez ponawiania pełnej transkrypcji i bez instalacji/zmian referencyjnego WhisperX. Po fast-forward main ponownie: 23/23 PASS, 6,082 s, eksporty/offline PASS. Commit konfiguracji i testów: 387c1786a23211075aa4658a870be96e093a05ef; po nim wyłącznie dokumentacyjny checkpoint wydania.
- D-54 (lokalny kandydat, nie końcowy odbiór Work): nazwa v1.1.0 nie koliduje z zastanym jedynym tagiem mvp-v1.0. Integracja roboczej gałęzi do main bez utraty historii; tag v1.1.0 na finalnym checkpointcie, mvp-v1.0 bez zmian. Końcowe SHA main/tag i status w protokole finalizacji i odpowiedzi. RELEASE CANDIDATE READY — PENDING FINAL ACCEPTANCE. Pozostają ograniczenia z sekcji 6 planu, w szczególności brak pełnego ASR preserve i brak pełnego odsłuchu.


## Poprawka provenance v1.1.1 — 18.10.2026

- D-55 (użytkownik): minimalna poprawka nowych run.json: application=WHISPERX_GUI i application_version=1.1.1. Lokalny commit i handoff, bez push, nowej publikacji lub zmiany historycznych tagów/wyników. Profile, ASR, eksporty, offline i anulowanie bez zmian.
- D-56 (rozpoznanie i wybór wykonawczy): wejściowo czysty main=origin/main=v1.1.0=fc5e2c76966c4219c50c0955ff3898c064614613. Jedyny historyczny identyfikator nadawano w Controller.start; brak istniejącego źródła wersji aplikacji/metadata pakietu. Dwie stałe APPLICATION_ID/APPLICATION_VERSION dodano do istniejącego configuration.py, bez nowego modułu, pliku wersji, odczytu Git w runtime lub zależności. Kontroler używa ich także do niezmienionego prefiksu logu.
- D-57 (kompatybilność): application_version jest addytywną metadaną schema 1, nie zmienia formatu transcript.json/TXT/SRT ani pozostałego provenance. Starsze manifesty z application=WHISPERX_GUI D2.1 i brakiem nowego pola pozostają poprawnymi historycznymi wynikami, bez migracji. Ograniczenia kontraktu wynikowego nie wymagają zmiany.
- D-58 (weryfikacja i kandydat): 24/24 unittest PASS (6,717 s), prawdziwe eksporty/offline PASS, AST PASS; 134 wcześniejsze run.json bez zmiany SHA-256, 15 nowych manifestów z poprawnym ID/wersją, w tym stany błędu i anulowania. config/profilów, silnika, mediów, worker/safety/winjob i writerów nie zmieniono. Gałąź codex/provenance-1-1-1, lokalny kandydat PATCH READY — PENDING ACCEPTANCE; main i tag v1.1.0 zachowane. Pełna transkrypcja i nowy test rzeczywistego ASR nie były uruchamiane.
