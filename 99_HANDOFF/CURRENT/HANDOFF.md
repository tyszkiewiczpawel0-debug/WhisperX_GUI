# WHISPERX_GUI — checkpoint D2

Data: 14.10.2026. Odbiorca: główna rozmowa WHISPERX_GUI, za pośrednictwem użytkownika.

**D2: COMPLETE wykonawczo, do formalnego odbioru. D0/D1 zatwierdzone zleceniem D2. D3 nie rozpoczęto.**

## Aktualizacja — poprawka pierwszego uruchomienia D2

14.10.2026: naprawiono zgłoszony ParserError. Potwierdzona przyczyna: Start.ps1 UTF-8 bez BOM był interpretowany jako CP1250 przez Windows PowerShell 5.1.26100.9711; poprzednia kontrola składni używała PS7.6.5. Treść launchera jest teraz ASCII, TOML odczytywany jawnie jako UTF-8. Start.cmd wskazuje systemowy PowerShell, zachowuje kod błędu i otwarte okno konsoli. Błędy loadera GUI przy starcie są wypisywane do konsoli z kodem 1 zamiast niewidocznego w teście modalu.

PASS: rzeczywiste Start.cmd → Start.ps1 → Python → widoczne GUI, zamknięcie z kodem 0; katalog z polskimi znakami/spacjami; brak TOML, błędne pole python, nieistniejący interpreter i uszkodzona składnia TOML (czytelne komunikaty, kod 1). Test wykonywał cmd.exe /c, bez atrap GUI; gest dwukliku pozostaje do ręcznego odbioru. Początkowy test modalu dla uszkodzonego TOML przekroczył timeout; po poprawce komunikacji test przeszedł. [Raport i dowody](../../docs/D2_TEST_REPORT.md), test regresji tests/check_launcher.py.

Nie zmieniono silnika, źródłowego WhisperX, środowiska Python ani konfiguracji użytkownika; brak instalacji i pobrań. GPU nie testowano ponownie. Start użytkownika: dwuklik Start.cmd; przy błędzie przeczytaj zachowany komunikat konsoli i popraw local.toml według README.

Branch main. Bazowy checkpoint D2: 97b371c658c3133eb1a6307e6d8a0febf97edf38. Niniejsza poprawka ma osobny lokalny commit „Fix Windows PowerShell launcher encoding and startup errors”; jego SHA jest HEAD po zakończeniu poprawki i zostaje podane w odpowiedzi. Status/branch sprawdzane po commicie, bez push. Poniższe informacje o wcześniejszych commitach i testach opisują pierwotną implementację D2.

Poprawka zakończona, do odbioru D2. Nie rozpoczęto D2.1 ani D3.

## Funkcje i ponowne wykorzystanie

GUI Tkinter: pojedyncze audio/wideo, metadane, jeden profil z pliku, parametry urządzenia/compute/batch/alignment, osobne sprawdzenie i przygotowanie WAV, pełna transkrypcja, status/log, anulowanie i otwarcie wyników. Model large-v3 i język pl pozostają stałe dla jedynego profilu.

REUSE: istniejący Python/stos, Tkinter, FFprobe/FFmpeg, WhisperX/faster-whisper/CTranslate2, VAD pyannote, modele ASR/PL i writery TXT/SRT/JSON. ADAPT: sekwencja API i zwalniania modeli z transcribe_trip_meeting.py, bez jego importu. BUILD: kontroler/GUI, walidacja, Job Object, offline/preflight, unikatowe katalogi, manifest i kontrola kompletności. Nie przeniesiono błędnej srt_ts.

## Weryfikacja

PASS: 11 testów logiki/integracji, responsywność Tkinter, rzeczywista konwersja WAV/MKV, błędne wejście, brak/wiele ścieżek, ostrzeżenie długości, brak nadpisania, Job Object kończący potomny FFmpeg i zachowujący niezależny proces, biblioteczne eksporty i granice minuty/godziny, blokada sieci i zapisów poza zadaniem. Składnia Python/PowerShell, ignore, linki zmienianych dokumentów, staged diff bez danych wykonawczych i sygnatur sekretów — PASS.

GPU/offline: potwierdzono dwa pełne przebiegi próbki 20 s, large-v3/pl/cuda/float16/batch 8 + alignment PL na RTX 5070 Ti, 2 segmenty i 58 słów. Ostatni 23,766 s, komplet pięciu plików, succeeded. Anulowanie rzeczywistego ASR i alignmentu — PASS, cancelled, WAV zachowane. Offline oznacza lokalne zasoby i aktywne blokady bibliotek/Python, nie audyt sieci kodu natywnego.

Brak FAIL w końcowych testach. NOT TESTED: pełny RUI, odsłuch/terminologia/synchronizacja, RAM/VRAM długiego materiału, CPU/inne compute, pełny przebieg bez alignmentu, drugie stanowisko, brak GPU/OOM/dysk pełny/awaria systemu i ręczny odbiór wyglądu GUI. Nie przedstawiać tych elementów jako PASS.

Szczegóły i identyfikatory lokalnych dowodów: [D2_TEST_REPORT](../../docs/D2_TEST_REPORT.md). Końcowy pipeline: runs/jobs/20261014_181727_8d98f212a70f455ea3f9315c5f6d1d32, prywatne run.json i process.log poza Git.

## Ograniczenia i decyzje

TorchCodec zgłasza niedostępne DLL; ścieżka FFmpeg → audio w pamięci działa. Nie naprawiano ani nie aktualizowano środowiska. Lightning adaptuje checkpoint tylko w pamięci, bez migracji pliku. Brak koniecznej decyzji blokującej D2.

Próg długości 0,1 s jest konfigurowalny, bez gwarancji synchronizacji. Wiele ścieżek i offset >0,1 s są odrzucane; drobne offsety jawnie raportowane. Pośrednie zachowujemy także po sukcesie. Każda operacja tworzy nowy katalog; transkrypcja ponownie przygotowuje WAV z oryginału. Awaria całej aplikacji/systemu może pozostawić running; brak automatycznej naprawy/wznowienia.

## Ochrona i Git

Źródło C:\AI\WhisperX, .venv, modele, nagrania i wcześniejsze wyniki pozostały tylko do odczytu. Porównanie 46565 ścieżek/rozmiarów/mtime_ns przed i po D2 identyczne; nie jest to pełny hash zawartości. Kontrakt i standard zachowały oryginalne SHA256 wskazane w raporcie. Bez instalacji, pobrań, drugiego venv, zmian globalnych Windows i push.

Repozytorium C:\AI\WhisperX_GUI, branch main. Commit implementacji: **6c611e121ac290ee08807649913229b512fc44cb**. Po nim working tree był czysty. Niniejszy handoff stanowi osobny commit „Record D2 verification and handoff”; jego SHA jest bieżącym HEAD po zakończeniu D2 i jest przekazane w końcowej odpowiedzi. SHA własnego commita nie może być wpisane do jego treści bez zmiany SHA. Po commicie checkpointu kontrolowane są status i branch. Brak remote/push; dane i lokalny TOML ignorowane.

## Pierwszy start i proponowany D3

Dwuklik **Start.cmd** w repozytorium. Lokalny config/local.toml jest gotowy, output wskazuje runs/jobs. Wybierz plik → Sprawdź plik → opcjonalnie Przygotuj WAV → Transkrybuj. Przerwij kończy własne drzewo procesów; Otwórz wyniki pokazuje rezultaty. Pełna instrukcja i nowe stanowisko: [README](../../README.md).

Po odbiorze D2 użytkownik osobno autoryzuje D3 i wskazuje webinar RUI. Rekomendacja: inspekcja metadanych, przygotowanie i kontrola długości/offsetów, pełna transkrypcja w nowym katalogu, sprawdzenie pięciu wyników, odsłuch początku/środka/końca i ocena terminologii, raport jakości oraz RAM/VRAM. Bez streszczeń, diarizacji i analizy prawnej.

Prace D2 zakończone. Pilotażu RUI nie uruchomiono. Decyzja o odbiorze i dalszym etapie należy wyłącznie do użytkownika.
