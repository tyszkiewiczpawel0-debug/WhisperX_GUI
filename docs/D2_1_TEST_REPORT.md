# D2.1 — weryfikacja initial_prompt, 14.10.2026

Status: COMPLETE wykonawczo, do odbioru użytkownika. D2 formalnie zatwierdzony zleceniem D2.1. D3 nie rozpoczęto.

## Potwierdzone API lokalne

Odczyt źródeł i importlib.metadata istniejącego środowiska: WhisperX 3.8.6, faster-whisper 1.2.1, CTranslate2 4.8.2. Nie importowano skryptu transcribe_trip_meeting.py.

- whisperx/asr.py: load_model (od linii 315) przyjmuje asr_options, scala słownik z domyślnymi opcjami (401–407), tworzy TranscriptionOptions. Domyślny initial_prompt to None (384).
- generate_segment_batched (47–56) używa `" " + options.initial_prompt.strip()`, tokenizuje i wywołuje odziedziczone get_prompt. W tym mechanizmie obsługiwane są str/None, nie lista tokenów, mimo deklaracji szerszego typu w faster-whisper.
- faster_whisper/transcribe.py: max_length=448 (722), get_prompt (1532 i dalej) zachowuje ostatnie max_length//2-1, czyli 223 tokeny poprzedniego kontekstu. Ten sam prompt jest używany dla próbek batcha. To nie jest limit 223 znaków ani gwarancja rozpoznania terminologii.
- Adapter podaje wyłącznie `asr_options={'initial_prompt': ...}` jako nowy argument load_model. ASR transcribe, VAD, alignment i przygotowanie audio zachowują parametry D2.

## Wyniki

Polecenie skonfigurowanym Pythonem z -B: `-m unittest discover -s tests -p 'test_*.py' -v` — **16/16 PASS**, 2,713 s.

| Kontrola | Wynik / rodzaj dowodu |
|---|---|
| Brak pola, null, pusty tekst i białe znaki | PASS, normalizacja do None, zgodność starego profilu |
| Domyślny tekst, polskie znaki, nowe linie i skrajne spacje | PASS, tekst niepusty zachowany dokładnie |
| Odrzucenie listy/liczby/bool/obiektu | PASS, walidacja |
| GUI: domyślny tekst, edycja i wyczyszczenie | PASS, rzeczywisty widget Tkinter, kontroler zastąpiony atrapą przy sprawdzaniu przekazywanych wartości |
| Profil po edycji GUI | PASS, porównanie bajtów pliku; brak mutacji słownika domyślnego |
| Adapter: dokładny tekst/None i pozostałe parametry | PASS, kontrolowane atrapy torch/whisperx, bez modeli |
| Worker: sukces/błąd przed load_model/w ładowaniu/w ASR | PASS, rzeczywisty zapis JSON, kosztowne operacje zastąpione atrapami; sprawdzone stany pośrednie i końcowe |
| Kontroler: błąd wejścia/natychmiastowe anulowanie | PASS, rzeczywisty worker; prompt skonfigurowany zachowany, nie oznaczony jako przyjęty |
| Regresja D2 | PASS, 11 dotychczasowych testów, w tym FFmpeg, Job Object, responsywność Tkinter i ochrona oryginału |
| Rzeczywisty ASR + alignment + eksport z promptem | PASS, jeden przebieg 20 s próbki D2, komplet pięciu plików, 6 segmentów, 25,047 s; nie benchmark |
| Składnia i układ GUI | PASS, AST wszystkich modułów/testów; widoczne okno 940x810 i 760x680, pole promptu/log/przyciski mieszczą się w oknie |
| Integralność źródła | PASS, wszystkie 46565 ścieżek/rozmiarów/mtime_ns identyczne przed/po testach |

Rzeczywisty run: `runs/jobs/20261014_184459_6d3c189f03194b9586b81fea97116ea8`. Profil large-v3/pl/cuda/float16/batch 8/alignment=true. Prompt kontrolny zawierał tekst polski, nowe linie oraz skrajne spacje. Asercje potwierdziły dokładny tekst w parameters.initial_prompt i głównym initial_prompt, stan accepted_by_engine, brak pełnego promptu w process.log i niezmienność SHA256 próbki. Test służył sprawdzeniu mechanizmu, nie ocenie jakości ani porównaniu tekstów transkrypcji.

Dowody lokalne poza Git: `runs/d21_40fc899cc42a4be0b03cb9e1950390b1` (spis źródła przed, wynik silnika, wynik integralności). Próbka: istniejące `runs/d2_checks/sample_pl_20s.wav`; SHA256 `501018c8f62666f4776755835852d585e74780139f003a6c29857660835a5ea8` przed/po identyczne. Każdy test utworzył nowy katalog, bez nadpisania poprzednich wyników.

## Metadane i ograniczenia

Brak/pusty prompt oznacza None/null. Niepusty jest przekazywany dokładnie; dopiero biblioteka normalizuje go i tokenizuje. `parameters.initial_prompt` jest konfiguracją, główne `initial_prompt` jest potwierdzoną wartością przyjętą przez load_model. Stan submission_unconfirmed jawnie oznacza niepewność podczas ładowania; null w tym stanie nie oznacza potwierdzonego braku promptu. Szczegóły: [DATA](DATA.md).

Nie powtarzano kosztownych testów anulowania GPU z D2; nowe testy sprawdzają trwałe checkpointy workera i wczesne anulowanie kontrolera. Nie testowano pełnego webinaru, jakości RUI, CPU/innych compute, długich nagrań ani drugiego stanowiska. Ręczny odbiór wyglądu i gest dwukliku pozostają po stronie użytkownika; launchery nie były zmieniane. Dotychczasowe ostrzeżenie TorchCodec nie zablokowało przebiegu.

Ochrona: istniejące mechanizmy offline i audit hook aktywne podczas rzeczywistego przebiegu. Bez instalacji, pobrań, drugiego venv, zmian modeli/konfiguracji środowiska i push. Kontrola integralności porównuje ścieżki/rozmiary/mtime_ns, nie pełne hashe całej instalacji. Kod i dane źródłowe pozostają tylko do odczytu.
