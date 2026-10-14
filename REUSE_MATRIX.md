# WHISPERX_GUI — D0: macierz ponownego wykorzystania

Data: 14.10.2026. Propozycja do zatwierdzenia, zgodna z lokalnym PROJECT_CONTRACT.md v1.0 APPROVED. REUSE nie oznacza gwarancji wykonania całego pipeline: poziom weryfikacji podano oddzielnie.

Źródła: **SRC** = `C:\AI\WhisperX`; **PKG** = `C:\AI\WhisperX\.venv\Lib\site-packages`. Szczegółowe wyniki diagnostyki i ograniczenia zawiera DISCOVERY_REPORT.md. S = analiza kodu; D = diagnostyka; A = istniejący artefakt; N = brak nowego testu wykonawczego silnika.

| Komponent i co istnieje | Lokalizacja / dowód | Klasyfikacja | Potwierdzenie działania | Zastosowanie w GUI i wymagane zmiany |
|---|---|---|---|---|
| Interpreter i istniejący stos | SRC `.venv`, `pyvenv.cfg`, dist-info | REUSE | D: Python 3.11.9; odczyt wersji. Silnik N | Wskazać interpreter w lokalnej konfiguracji; nie klonować ani aktualizować venv. Osobny proces zadania używa tego samego środowiska |
| Tkinter | biblioteka bazowego Pythona | REUSE | D: import, Tcl/Tk 8.6; okno N | Użyć istniejących widgetów; własny układ GUI pozostaje BUILD |
| FFmpeg i FFprobe | WinGet Links w profilu użytkownika | REUSE | D: wersje i FFprobe dla M4A/WAV; konwersja N | Wywoływać istniejące narzędzia; ścieżki konfigurowalne |
| Dekodowanie/downmix/resampling | PKG `whisperx/audio.py::load_audio` | REUSE | S; WAV istnieje, ale nie dowodzi jego utworzenia tą funkcją | Użyć do wczytania przygotowanego audio. Funkcja zwraca tablicę, nie plik; nie duplikować dekodera |
| Przygotowanie trwałego WAV i kontrola długości | istniejący WAV w SRC OUTPUT; brak skryptu przygotowania | BUILD | D: właściwości i różnica 15.042 ms; procedura nieustalona | Cienka obsługa FFprobe/FFmpeg, wybór strumienia, kontrola długości i osobny katalog pośredni. Nie budować własnego DSP |
| ASR / Python API | PKG `whisperx/asr.py`, `faster_whisper`, `ctranslate2` | REUSE | S; A: RAW; obecny stos N | Użyć istniejącego load_model/transcribe z jawnymi parametrami i lokalnymi zasobami |
| Przepływ skryptu transkrypcji | SRC `transcribe_trip_meeting.py`, sekcje ASR/alignment/export | ADAPT | S i A; brak manifestu pochodzenia wyników | Przenieść minimalną sekwencję do adaptera w GUI z opisem pochodzenia; parametry zamiast stałych, funkcja main, obsługa błędów; nie importować skryptu źródłowego |
| Modele ASR i polskiego alignmentu | cache HF, snapshoty podane w raporcie | REUSE | D: pliki/refs/rozmiary; ładowanie N | Użyć lokalnych zasobów, bez kopiowania i pobrań; sprawdzić kompletność i zgodność offline |
| VAD pyannote | PKG `whisperx/vads/pyannote.py`, assets/pytorch_model.bin | REUSE | S i obecność wag; ładowanie N | Zachować obecny VAD. Wyłączenie diarizacji nie wyłącza VAD |
| Alignment PL | PKG `whisperx/alignment.py::load_align_model`, `align` | REUSE | S; A: 155 segmentów i 2594 słowa; nowy przebieg N | Zachować model PL i alignment, walidować zakresy czasu, zachować ostrzeżenia o niedopasowanych segmentach |
| Dane Punkt PL | AppData/Roaming/nltk_data/tokenizers/punkt_tab/polish | REUSE | D: obecność 4 plików; użycie przez silnik N | Sprawdzić dostępność przed startem i jawnie wskazać lokalny katalog; nie dopuścić automatycznego pobierania |
| Zwalnianie modeli/GPU | skrypt: del, gc.collect, empty_cache; PKG transcribe.py | ADAPT | S; wydajność N | Zachować rozdzielenie faz ASR/alignment, dołożyć finally i zakończenie procesu przy anulowaniu |
| Eksport TXT/SRT/JSON | PKG `whisperx/utils.py::get_writer`, WriteTXT/WriteSRT/WriteJSON | REUSE | S; biblioteczne writery N | Użyć trzech writerów, bazowa nazwa transcript i jawne options. Walidacja, staging i bezpieczny katalog są nową otoczką |
| Dotychczasowy własny eksport | skrypt: ts, srt_ts, json_default, pętle zapisujące | ADAPT | A: istniejące pliki; D: błąd srt_ts na granicy minuty | Zachować potrzebną semantykę wyniku; zastąpić ręczne formatowanie istniejącym writerem/format_timestamp. Nie kopiować błędu ani ślepego str(obj) |
| CLI WhisperX | PKG `whisperx/__main__.py`, `transcribe.py`, entry_points.txt | REUSE (alternatywa) | S; nie uruchamiano | Dostępna alternatywa, lecz mniej wygodna dla kontroli etapów i dokładnie 3 eksportów. Nie jest odrzucona z powodu braku funkcji ASR |
| Statusy i komunikaty | print w skrypcie; log_utils i callbacki ASR/align | ADAPT | S; trwałe logi nie istnieją | Przechwycić stdout/stderr, dodać zdarzenia etapów i process.log. Procent tylko lokalny dla etapu, nie pozorny procent całego zadania |
| GUI, profile i lokalna konfiguracja | brak w źródle | BUILD | brak implementacji | Minimalny formularz Tkinter i jeden profil WEBINAR_RUI_PL w konfiguracji niezależnej od logiki |
| Kontroler zadania i anulowanie | brak w źródle | BUILD | brak implementacji | Jeden proces roboczy, kolejka komunikatów, responsywny GUI, anulowanie własnego drzewa procesów |
| Bezpieczne katalogi, run.json i kompletność | brak; istniejące zapisy używają open(w) | BUILD | S: ryzyko nadpisania | Unikatowy katalog na każde uruchomienie, stany końcowe i zapis zastosowanych parametrów/wersji, walidacja kompletu wyników |
| Wznawianie po RAW | skrypt zapisuje RAW, nie ma odczytu checkpointu | DEFER | S: brak wznowienia | W MVP ponowienie to nowe zadanie; nie budować resumera |
| Diarizacja i dodatkowe formaty | PKG diarize.py i utils.py | DEFER | S; nie testowano | Poza MVP: diarizacja wyłączona, VTT/TSV/Audacity nie są wymagane |
| Wiele profili, kolejka wielu nagrań | brak warstwy aplikacyjnej | DEFER | brak | Nie tworzyć w MVP; jeden profil, jedno nagranie |

Minimalny BUILD dotyczy wyłącznie warstwy użytkowej i kontroli wykonania. Silnik ASR, alignment, VAD, narzędzia multimedialne, biblioteczne writery, Python oraz modele pozostają istniejącymi komponentami. REUSE zasobów jest rekomendacją warunkową do czasu późniejszego testu wykonania, bez zgody na ich zmianę.
