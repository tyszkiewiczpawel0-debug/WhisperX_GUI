# WHISPERX_GUI — checkpoint D2

Data: 14.10.2026. Odbiorca: główna rozmowa WHISPERX_GUI, za pośrednictwem użytkownika.

**D2: COMPLETE wykonawczo, do formalnego odbioru. D0/D1 zatwierdzone zleceniem D2. D3 nie rozpoczęto.**

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
