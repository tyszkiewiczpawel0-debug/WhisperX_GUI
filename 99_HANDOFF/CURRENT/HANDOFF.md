# WHISPERX_GUI — checkpoint implementacji kolejnej wersji

Data: 18.10.2026. Odbiorcy: **użytkownik i główna rozmowa ChatGPT projektu WhisperX_GUI**.

**IMPLEMENTATION COMPLETE — PENDING ACCEPTANCE**

## Git i zakres

Gałąź: `codex/multiple-profiles`. HEAD implementacji w chwili sporządzenia: `459fd15b7e84892762aab972fb80a3556f54275f`; wcześniejszy lokalny commit analizy `23d0786`. Następny commit „Record implementation tests and acceptance checkpoint” utrwala wyłącznie dokumentację, zatem dokładny końcowy HEAD checkpointu odczytuje `git rev-parse HEAD` (podany także w odpowiedzi końcowej). Tag mvp-v1.0 nadal wskazuje `a677fc6f62620752156fd2565edac6e3585090e0`. Bez push/nowego tagu, stan zdalny nie był sprawdzany.

Zlecenie IMPLEMENTATION AUTHORIZED otworzyło wykonanie po analizie, nie odbiór nowej wersji. Zamknięte MVP/D4 APPROVED i historyczne 6 PASS / 3 PARTIAL / 0 FAIL pozostają bez zmian.

Kod: jawny rejestr dwóch stałych profili, profile() nadal webinar; sesja_rady_gminy z dokładnymi parametrami zlecenia. GUI wybiera profil, resetuje nadpisania, blokuje wybór w trakcie zadania, odblokowuje po stanach końcowych. Nie zapisuje JSON. Alignment sesji edytowalny, diarizacja wyłączona. Kontroler bez przebudowy, worker korzysta z request snapshot i parameters.id; bez profile_id, zmiany promptu/preflight/offline/Job Object lub logiki writerów.

Opcjonalny audio_timeline_mode=legacy|preserve, brak → legacy. Oba dostarczone profile pozostają legacy; preserve trzeba wybrać jawnie w konfiguracji przed startem GUI lub parametrach wywołania. Nie ma przełącznika GUI ani heurystyki. Prepare zachowuje stare polecenie dla legacy, preserve dodaje aresample=16000:async=1:first_pts=0. Wybrany tryb jest w parameters, wykonany w preparation wraz z poleceniem, referencją i oddzielnymi długościami/deltami. Nie potwierdza przygotowania po jego przerwaniu.

## AUDIO-01 i decyzja

MP4 5884,600 s (98:04,600), H.264 + jedna AAC LC 32 kHz mono, starty 0; audio 5884,501 s. Legacy WAV 5884,096 s (−405 ms do audio, −504 ms do kontenera). Preserve WAV 5884,501 s (0 do audio, −99 ms do wideo).

Pięć wyraźnych zdarzeń waveform w źródle: 774,750 / 1967,000 / 2953,250 / 4417,750 / 5881,000 s. Legacy wyprzedza je o 109 / 213 / 213 / 405 / 405 ms; preserve daje 0 ms w punktach przy rozdzielczości 0,0625 ms i korelacji ≈1. Niezależny seek MP4 porównano z pełnym WAV; cisza nie była użyta jako zdarzenie. Potwierdzono identyczność WAV rzeczywistego workera z eksperymentem. 183878 pakietów AAC, trzy wydłużone duration dają łącznie 405 ms dodatku, bez przerw PTS >1 ms. Nie dowodzi to wcześniejszego łączenia pliku.

**Decyzja wykonawcza: opcja preserve uzasadniona dla AUDIO-01; brak zmiany domyślnych profili.** Nie dopełniać końca do długości wideo. To pomiar wybranych zdarzeń, nie pełny odsłuch ani uniwersalna gwarancja synchronizacji.

## Testy i ochrona

- **PASS:** końcowe 22/22 unittest (5,238 s), w tym A → B → A, wszystkie pola/prompt, stany wyboru GUI, oba profile/tryby przez rzeczywisty worker, niezmieniony JSON/polecenie webinaru, snapshoty, syntetyczny PTS, Job Object i niezależny proces. ASR w unit testach jest atrapą.
- **PASS:** prawdziwe eksporty TXT/SRT/JSON ze słowami z/bez czasów, granice minut/godzin, blokady sieci i zapisu; AST/TOML/profile.
- **PASS:** rzeczywisty ASR próbki 2950–2970 s, sesja/preserve, batch8/alignment=true, prompt=null: succeeded, 41,828 s z ładowaniem, 4 segmenty, 29/29 słów z czasami, komplet wyników. Znane ostrzeżenia TorchCodec/TF32 i zmiana checkpointu w pamięci bez blokady; nie zmieniano bibliotek/wag.
- **PASS:** przerwanie obserwowanego aktywnego potomnego FFmpeg w preserve na AUDIO-01: cancelled, potomny proces zakończony, brak preparation potwierdzającego wykonanie.
- **PASS w zakresie pomiaru:** SHA-256 oryginału przed/po identyczny, webinarowy JSON/local.toml bez zmiany hashy; 46565 plików źródła z identycznymi ścieżkami/rozmiarami/mtime_ns, nie pełny hash instalacji.
- **FAIL końcowe:** 0. Ujawniony sporadyczny Windows WinError 5 podczas replace manifestu obsługuje ograniczone ponowienie (5 prób, 0,30 s łącznie), bez usuwania celu/maskowania trwałych błędów. Media jawnie odmawia istniejącego WAV; w testach poprawiono cykle Tk i fixture'y. Brak nowych zależności.
- **NOT TESTED:** ręczna obsługa widocznego GUI podczas ASR, treść/odsłuch/lip-sync użytkownika, ponowne realne anulowanie ASR/alignmentu, osobny ASR webinaru, CPU/inne compute i drugie stanowisko. Bez pełnej transkrypcji 98 min. Historyczne trzy PARTIAL D4 nadal obowiązują.

## Dowody i powrót

[Plan i raport](../../NEXT_VERSION_IMPLEMENTATION_PLAN.md#5-wykonanie-i-wyniki--18102026) podaje pełne dane i zakres testów, [CURRENT_STATE](../../docs/CURRENT_STATE.md), [DECISIONS D-44–D-50](../../docs/DECISIONS.md), [DATA](../../docs/DATA.md). Lokalne dowody poza Git: `runs/next_version_b511b9f604ef4d2e857eacb639e22032`; ASR: `runs/jobs/20261018_104559_fa87a8beb0d24ba99ebde224f6420be5`. Nie sprzątano dawnych ani nowych wyników. Bez instalacji/pobrań, zapisu w referencyjnym WhisperX, zmian kontraktu/standardu lub publikacji.

Uruchom Start.cmd, sprawdź listę dwóch profili, przełącz A → B → A po edycji promptu/batch/alignment; formularz ma wracać do defaultów. Wybierz krótką próbkę i Transkrybuj; sprawdź parameters.id w request/run i komplet eksportów. Dla AUDIO-01 użyj jawnego preserve: zgodnie z README dopisz audio_timeline_mode do JSON sesji i uruchom GUI ponownie (ręczna trwała konfiguracja, GUI jej nie zapisuje). Sam wybór sesji z dostarczonego JSON nadal oznacza legacy. Nie uruchamiać pełnej transkrypcji tylko do kontroli wersji.

Odstępstwa od planu: oba domyślne legacy, obecny plik ma 98 min i mimo pojedynczego wejścia wykazał przesunięcia; niewielka poprawka trwałości zapisu JSON wynikająca z testu. Work rekomenduje gotowość do odbioru z wymienionymi ograniczeniami. Użytkownik i główna rozmowa zatwierdzają wynik; kolejnego etapu nie rozpoczęto.
