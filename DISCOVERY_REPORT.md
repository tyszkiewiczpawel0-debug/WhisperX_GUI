# WHISPERX_GUI — D0: raport discovery

Data: 14.10.2026. Status wykonania: **COMPLETE — do oceny użytkownika**. Nie stanowi zatwierdzenia D0 ani architektury i nie otwiera D1.

## 1. Podstawa i metoda

Przeczytano lokalny `C:\AI\WhisperX_GUI\PROJECT_CONTRACT.md`, v1.0, APPROVED, 14.10.2026. Kontrakt jest nadrzędny. Nie znaleziono lokalnej kopii pomocniczego `PROJECT_STANDARD_v0.2.md` w obu katalogach projektu; nie był podstawą ustaleń. Nie analizowano Progman_Kadry ani nie zmieniano standardów Ekosystemu.

Zastosowano odczyt plików, metadanych pakietów, cache, istniejących wyników oraz diagnostykę wersji, GPU i FFprobe. Python uruchamiano z `-I -B`, bez zapisu bytecode; importowano standardową bibliotekę i Tkinter, bez importowania silnika WhisperX/PyTorch. Izolowany test czystej funkcji SRT wykonano w pamięci po wydzieleniu jej z AST, bez wykonania skryptu. Nie uruchamiano konwersji, ładowania modeli ani transkrypcji.

Poziomy dowodów:

- **S — statyczny:** mechanizm potwierdzony w kodzie lub konfiguracji.
- **D — diagnostyczny:** wynik polecenia tylko do odczytu lub izolowanego testu bez silnika.
- **A — artefakt:** istniejący wynik; dowodzi istnienia danych, nie odtwarzalności na obecnym stosie.
- **N — nieweryfikowany wykonawczo:** wymaga późniejszego zatwierdzonego testu.

## 2. Struktura i Git

`C:\AI\WhisperX` zawiera `.venv`, `INPUT`, `OUTPUT` i `transcribe_trip_meeting.py`. W `INPUT` jest jedno nagranie M4A; w `OUTPUT` WAV i cztery pliki transkrypcji wskazane niżej. Nie znaleziono własnego README, manifestu zależności, testów, skryptu przygotowania audio, logów ani dokumentacji problemów w tej strukturze. Biblioteki w `.venv` są zależnościami, nie kodem aplikacji.

**Oba katalogi nie są obecnie repozytoriami Git.** `git -C <katalog> rev-parse --show-toplevel` zwrócił dla obu `fatal: not a git repository (or any of the parent directories): .git`. Nie ma więc dostępnej historii, branchy, remote ani stanu zmian do opisania. Nie inicjalizowano Git. Określenie „repozytorium źródłowe” w zleceniu oznacza w praktyce istniejący katalog rozwiązania. Źródło jest dostępne, więc brak Git nie blokuje D0. W katalogu GUI przed D0 był wyłącznie kontrakt. Nie znaleziono właściwych lokalnych AGENTS.md w projektach ani sprawdzonych katalogach nadrzędnych `C:\AI` i `C:\`.

## 3. Przepływ istniejącego skryptu

Dowód S: `C:\AI\WhisperX\transcribe_trip_meeting.py`, stałe modułu i kolejne sekcje AUDIO, TRANSKRYPCJA, ALIGNMENT, EXPORT.

1. Stałe wskazują `OUTPUT\Glos_261006_115924_16k_mono.wav`, wspólny katalog OUTPUT oraz bazę `Glos_261006_115924`.
2. Skrypt pyta PyTorch o nazwę GPU bez wcześniejszego sprawdzenia dostępności CUDA.
3. `whisperx.load_audio()` ładuje całość audio do pamięci.
4. `whisperx.load_model('large-v3', 'cuda', compute_type='float16', language='pl')`; `model.transcribe(audio, batch_size=8)`.
5. Zapisuje RAW JSON. Usuwa model ASR, wywołuje `gc.collect()` i `torch.cuda.empty_cache()`.
6. Ładuje `jonatasgrosman/wav2vec2-large-xlsr-53-polish`; wykonuje `whisperx.align(..., return_char_alignments=False)`; dopisuje `language='pl'` i zwalnia model alignmentu.
7. Własne pętle zapisują ALIGNED JSON, TXT ze znacznikami czasu i SRT.

To integracja przez **Python API**, bez diarizacji i bez własnego silnika rozpoznawania. Brak funkcji głównej i osłony `if __name__ == '__main__'`: import skryptu uruchomi przetwarzanie. Nie importować go z GUI. Wczytywanie i zapis korzystają ze ścieżek absolutnych. Zapisy `open('w')` nadpisują wcześniejsze wyniki. Nie ma walidacji, konfiguracji profili, kontrolera zadania, anulowania, obsługi wyjątków/finally, trwałego logowania ani automatycznego wznowienia. RAW jest wynikiem pośrednim, a nie wdrożonym checkpointem wznowienia. Komunikaty `[1/5]`–`[5/5]` mogą zostać wykorzystane jako wzorzec statusów.

## 4. Audio, narzędzia i oś czasu

Dowód S: `.venv\Lib\site-packages\whisperx\audio.py::load_audio`, `SAMPLE_RATE=16000`. FFmpeg jest uruchamiany jako proces z `-nostdin -threads 0 -i <plik> -f s16le -ac 1 -acodec pcm_s16le -ar 16000 -`. Surowe próbki trafiają przez stdout do NumPy float32. Funkcja konwertuje częstotliwość i kanały, lecz **nie zapisuje WAV** ani nie kontroluje długości. Nie modyfikuje oryginału. Przechwytuje błąd FFmpeg i zgłasza RuntimeError; brak binarki będzie innym wyjątkiem procesu.

Brak filtra rozszerzeń: możliwe są formaty audio/wideo dekodowane przez zainstalowany FFmpeg, ale nie jest to dowód obsługi każdego kodeka. D0 potwierdziło odczyt metadanych AAC/M4A i PCM/WAV; MP3, FLAC, MP4, MKV, wiele ścieżek audio, nietypowe timestampy i pliki uszkodzone nie były testowane. `load_audio` nie wybiera jawnie strumienia przez `-map`. GUI powinno wykrywać brak audio oraz niejednoznaczność wyboru ścieżki.

Dowód D: FFprobe `-v error -show_entries format=format_name,duration,start_time:stream=index,codec_type,codec_name,sample_rate,channels,duration,start_time -of json <plik>`:

| Plik względem źródła | Format | Hz / kanały | Czas |
|---|---|---|---|
| `INPUT\Głos 261006_115924.m4a` | AAC, kontener M4A | 48000 / 1 | 962.032958 s; start 0 |
| `OUTPUT\Glos_261006_115924_16k_mono.wav` | PCM s16le, WAV | 16000 / 1 | 962.048000 s |

Różnica **+0.015042 s**, około 0.00156%. To dowód zgodności długości tej pary, nie dowód zgodności próbek ani synchronizacji mowy. Nie znaleziono polecenia lub skryptu tworzącego WAV; jego pochodzenie i zastosowane filtry nie są potwierdzone. Pliki są rozdzielone między INPUT i OUTPUT. W obecnym skrypcie nie ma polityki plików pośrednich ani sprzątania.

Dowód S: `whisperx\asr.py::FasterWhisperPipeline.transcribe` wycina zakresy VAD z oryginalnej tablicy i zwraca ich czasy; `alignment.py::align` dodaje początek segmentu do czasu względnego. VAD nie oznacza tu sklejenia całej mowy na nowej osi czasu. Brak precyzyjnej walidacji offsetu audio względem obrazu; należy ją przeprowadzić w pilotażu. Rozdzielczość zapisu 0.001 s nie jest gwarancją dokładności akustycznej 1 ms.

## 5. Rzeczywiste środowisko

Dowód D: `python.exe -I -B`, `sys.version`, `importlib.metadata.version`, import Tkinter; S: `.venv\pyvenv.cfg`, `torch\version.py` i `*.dist-info\METADATA`.

| Składnik | Odczytana wersja / stan |
|---|---|
| Python | 3.11.9, AMD64, MSC 1938 |
| Interpreter | `C:\AI\WhisperX\.venv\Scripts\python.exe` |
| Python bazowy | `C:\Users\tyszk\AppData\Local\Python\pythoncore-3.11-64` |
| Tkinter | import działa; deklarowane Tcl/Tk 8.6 / 8.6; okna nie uruchamiano |
| WhisperX | 3.8.6 |
| torch / torchaudio | 2.8.0+cu128 / 2.8.0+cu128 |
| torchvision / torchcodec | 0.23.0+cu128 / 0.7.0 |
| CUDA kompilacji PyTorch | 12.8, z `torch/version.py`; nie jest to wersja globalnego CUDA Toolkit |
| faster-whisper / CTranslate2 | 1.2.1 / 4.8.2 |
| pyannote.audio | 4.0.7 |
| NumPy / transformers | 2.4.6 / 4.57.6 |
| huggingface-hub / NLTK | 0.36.2 / 3.10.3 (NLTK: metadane katalogu dist-info) |
| FFmpeg / FFprobe | 8.1.2-full_build-www.gyan.dev |
| GPU | NVIDIA GeForce RTX 5070 Ti |
| Sterownik / VRAM | 610.88 / 16303 MiB, wolne w pomiarze 14497 MiB |

FFmpeg i FFprobe są rozwiązywane przez `C:\Users\tyszk\AppData\Local\Microsoft\WinGet\Links\`; nvidia-smi przez `C:\WINDOWS\system32\nvidia-smi.exe`. GPU i pamięć odczytano `nvidia-smi --query-gpu=name,driver_version,memory.total,memory.free --format=csv`. Wolna pamięć jest chwilowym pomiarem.

W procesie diagnostycznym nie ustawiono HF_HOME, HF_HUB_CACHE, HUGGINGFACE_HUB_CACHE, TRANSFORMERS_CACHE, TORCH_HOME, XDG_CACHE_HOME, CUDA_PATH ani CUDA_VISIBLE_DEVICES. Nie przesądza to o ustawieniach innych sesji. Nie uruchamiano importów CUDA/CTranslate2 ani obliczeń: dostępność GPU dla nvidia-smi nie dowodzi działania bibliotek, zgodności DLL ani wystarczającej pamięci dla batch 8. Nie ustalono instalacji globalnego CUDA Toolkit; nie jest ona dowiedziona przez etykietę cu128.

## 6. Modele i zasoby lokalne

Dowody S/D: listing cache, pliki refs, kod `faster_whisper\utils.py::download_model`, `whisperx\asr.py::load_model`, `alignment.py::load_align_model`, `vads\pyannote.py::load_vad_model`.

Cache HF: `C:\Users\tyszk\.cache\huggingface\hub`.

| Zasób | Lokalna zawartość |
|---|---|
| `models--Systran--faster-whisper-large-v3` | refs/main = `edaa852ec7e145841d8ffdb056a99866b5f0a478`; snapshot zawiera model.bin 3087284237 B, config, tokenizer, vocabulary i preprocessor_config |
| `models--jonatasgrosman--wav2vec2-large-xlsr-53-polish` | refs/main = `6b1cea36bd8bc5f65ec8081667cd9c0207d51970`; pytorch_model.bin 1262097815 B, config, preprocessor_config, vocab i special_tokens_map |
| Dodatkowy snapshot alignmentu | `0b61f5638f60f68c00390ba76d05643b18571a25`, refs/pr/1, model.safetensors 1261971432 B; nie traktować jako kompletnego samodzielnego snapshotu |
| VAD pyannote | `.venv\Lib\site-packages\whisperx\assets\pytorch_model.bin`, 17719103 B |
| Filtry mel | w tym samym assets, `mel_filters.npz`, 4271 B |
| NLTK PL | `C:\Users\tyszk\AppData\Roaming\nltk_data\tokenizers\punkt_tab\polish`; abbrev_types.txt, collocations.tab, ortho_context.tab, sent_starters.txt |

Istnienie i rozmiary zasobów są potwierdzone; integralność wag, możliwość pełnego załadowania offline i zgodność z aktualnym stosem — N. Nie czytano tokenów, nie pobierano zasobów ani nie kopiowano modeli.

Istotne zachowania: ASR domyślnie stosuje VAD pyannote, niezależnie od wyłączonej diarizacji. `load_model` domyślnie ma `local_files_only=False`; polski alignment domyślnie `model_cache_only=False`. `alignment.py` przy braku Punkt wywołuje `nltk.download('punkt_tab')`. VAD tworzy katalog torch home (`os.makedirs`), a wariant Silero korzysta z `torch.hub.load`. Dlatego nie wykonywano próbnego ładowania. W przyszłym adapterze trzeba wyłączyć automatyczne pobieranie modeli i sprawdzić Punkt przed silnikiem; samo ustawienie offline HF nie blokuje pobrania NLTK. Nie rekomenduje się zmiany VAD na Silero w MVP.

## 7. Eksport, jakość danych i błędy

Dowód A/D: strukturalny odczyt istniejących plików, bez oceny treści rozmowy:

| Wynik w OUTPUT | Obserwacja |
|---|---|
| `Glos_261006_115924_RAW.json` | 42 segmenty, language=pl, zakres 0.031–962.075 s |
| `Glos_261006_115924_ALIGNED.json` | 155 segmentów, 2594 słowa, language=pl, segments i word_segments; zakres 0.031–961.975 s |
| `Glos_261006_115924_ALIGNED.srt` | 155 wpisów, brak niepoprawnych pól minut/sekund/milisekund w istniejącym pliku |
| `Glos_261006_115924_ALIGNED.txt` | istniejący eksport tekstu; kod dopisuje czas początku i końca segmentu |

W ALIGNED brak segmentów z ujemnym czasem, odwróconymi granicami, końcem poza WAV lub nakładaniem względem poprzedniego segmentu. Wszystkie 2594 słowa mają klucze start i end; nie jest to pełny audyt czasów każdego słowa. RAW kończy się **27 ms poza długością WAV**. To konkretne ograniczenie wymagające walidacji czasu, a nie dowód utraty audio.

Brak `run.json`, `process.log` i zapisu wersji/parametrów przy wynikach. Nie można przypisać istniejących artefaktów do obecnych wersji pakietów lub potwierdzić, że utworzono je dokładnie obecną wersją skryptu. Nie oceniano rozpoznawania mowy, kompletności semantycznej ani synchronizacji odsłuchem. Nagrania webinaru RUI z 14.10.2026 nie znaleziono w analizowanym INPUT; istniejący materiał nie jest dowodem pilotażu RUI.

**Potwierdzony błąd eksportera:** izolowana funkcja `srt_ts(59.9996)` zwraca `00:00:60,000`, a dla `3599.9996` — `00:59:60,000`. Przy przeniesieniu milisekund nie przenosi sekund do minut/godzin. Nie ujawnił się w istniejącym SRT. Należy wykorzystać poprawny mechanizm `whisperx\utils.py::format_timestamp` (najpierw zaokrągla całkowite milisekundy) lub biblioteczny WriteSRT. Nie poprawiano źródła.

Biblioteka ma `WriteTXT`, `WriteSRT`, `WriteJSON`, `get_writer` i CLI `whisperx.__main__:cli` (`entry_points.txt`). Wbudowany TXT jest bez czasów; kontrakt dopuszcza tekst transkrypcji. `get_writer('all')` daje dodatkowo VTT i TSV, więc dla MVP wybierać trzy writery jawnie. Biblioteczny ResultWriter też zapisuje przez `open('w')`: bezpieczeństwo katalogów musi zapewnić kontroler. Własny `json_default` potrafi zamienić nieznany obiekt na tekst, co może maskować problem schematu; adapter powinien walidować strukturalny JSON.

## 8. Wnioski, ograniczenia i późniejsza weryfikacja

Można wykorzystać bieżący interpreter i biblioteki bez drugiego stosu oraz zaadaptować sekwencję API i zwalniania modeli. Brak dowodów uzasadniających wymianę silnika lub interfejsu Tkinter. Nie ma natomiast gotowej aplikacyjnej obsługi przygotowania pliku, jego metadanych i długości, profili, zadań, anulowania i bezpiecznych wyników. Dokładny podział zawiera REUSE_MATRIX.md, propozycję integracji MVP_RECOMMENDATION.md.

Przeniesienie na inny komputer wymaga odtworzenia kompatybilnego Pythona/pakietów i dostępu do FFmpeg, zgodnego GPU/sterownika oraz lokalnych modeli, VAD i NLTK. `.venv` odwołuje się do Pythona bazowego w profilu użytkownika; nie jest przenośnym folderem do skopiowania. Brak lockfile i manifestu utrudnia odtwarzalność. Ich utworzenie i instrukcja instalacji należą do późniejszych etapów, bez instalowania czegokolwiek w D0.

Do późniejszego zatwierdzenia: test importu i ładowania lokalnych modeli bez sieci; krótka transkrypcja PL z alignmentem i pomiarem VRAM; test eksportu bibliotecznego, anulowania podczas FFmpeg/ASR/alignmentu, błędów i ponownego uruchomienia bez nadpisania; następnie pilotaż RUI i odsłuch początku/środka/końca. D0 nie wymaga tych uruchomień do zakończenia rozpoznania.

## 9. Kontrola zakresu i identyfikacja źródeł

Nie modyfikowano źródła, środowiska, modeli, nagrań ani istniejących wyników. Nie instalowano zależności, nie uruchamiano transkrypcji, nie pobierano zasobów i nie inicjalizowano Git. Utworzono wyłącznie trzy dokumenty D0 w katalogu GUI. Nie jest to pełny audyt integralności całego dysku; potwierdzenie dotyczy wykonanych czynności, a poniższe SHA256 identyfikują odczytane pliki:

- `transcribe_trip_meeting.py`: `031ef5c3d82a0cae5b7ae0d5ea2e4f24eafc28f7722670d9c65089dbc61fa13c`.
- `.venv\pyvenv.cfg`: `549e4eba21fd2309134eea8e5ba93db8b7d1927fd68d884d3e56b44ccc7657d0`.
- kontrakt GUI: `6fceb18b8e3170c78561182869c5d0ba542450eea61085b8994bf00f9594859c`.

Handoff do głównej rozmowy WHISPERX_GUI odbywa się za pośrednictwem użytkownika. Wykonawca nie zatwierdza D0 ani nie rozpoczyna D1.
