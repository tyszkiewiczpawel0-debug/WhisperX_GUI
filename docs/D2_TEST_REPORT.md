# Raport weryfikacji D2 — 14.10.2026

Status wykonawczy: COMPLETE, do odbioru użytkownika. Testy nie stanowią pilotażu RUI.

## PASS

- `tests/test_mvp.py`: 11 testów, ostatnie wykonanie 2,117 s. Konfiguracja i parametry, brak modeli, brak/wiele ścieżek, offsety (walidacja metadanych), znaczniki poza zakresem, uszkodzone wejście, rzeczywiste WAV i MKV, konwersja PCM/16 kHz/mono, ostrzeżenie różnicy długości, ponowienie bez nadpisania i niezmienność wejścia, natychmiastowe anulowanie.
- Tkinter: cykliczne zdarzenia podczas przygotowania, odstęp <0,5 s; test tworzy rzeczywiste okno ukryte. Nie jest ręcznym odbiorem interfejsu.
- Windows Job Object: rzeczywisty potomny FFmpeg został zakończony; niezależny proces kontrolny pozostał aktywny. Handshake eliminuje uruchomienie potomków przed przypisaniem.
- `tests/check_exports.py`: rzeczywiste get_writer TXT/SRT/JSON, polskie znaki, 59.9996 → 00:01:00,000 i 3599.9996 → 01:00:00,000. Blokowane próby DNS oraz zapisu poza katalogiem zadania.
- Pełna krótka transkrypcja: 20 s wydzielone z istniejącego źródłowego WAV (30–50 s), bez zapisu w źródle. large-v3/pl/cuda/float16/batch 8, VAD pyannote i alignment PL. Dwa przebiegi succeeded; 2 segmenty, 58 słów, komplet 5 artefaktów. Pierwszy 45,156 s, końcowy 23,766 s. Różnica długości przygotowanego WAV: 0 s.
- Anulowanie realnego silnika w etapach ASR i alignment: oba cancelled, pośrednie WAV zachowane, proces zakończony, brak zadeklarowanego sukcesu.
- Składnia 13 plików Python przez AST (bez bytecode); składnia Start.ps1; ignore lokalnej konfiguracji, requestów, wyników i snapshotów. Kontrole Markdown/Git w końcowym checkpointcie.
- Stan źródła: 46565 plików, identyczne ścieżki/rozmiary/mtime_ns przed/po. To kontrola metadanych, nie pełny hash zawartości środowiska.

## Lokalne dowody poza Git

W `runs/jobs/`:

| Zadanie | Identyfikator katalogu | Stan |
|---|---|---|
| Pierwszy pełny pipeline | 20261014_181317_3b7c75241f13423189e18b25975f7e91 | succeeded |
| Końcowy pełny pipeline | 20261014_181727_8d98f212a70f455ea3f9315c5f6d1d32 | succeeded |
| Przerwanie ASR | 20261014_181457_b2aafc5bbded456ca3109e91be465172 | cancelled |
| Przerwanie alignmentu | 20261014_181510_a89f08e8cb1b4acdb635ece15bafc858 | cancelled |

Każdy ma run.json i process.log. Końcowy manifest zawiera hashe wersji kodu wykonującego próbę i dwa ostrzeżenia bibliotek. Próbka i snapshoty ochrony źródła: runs/d2_checks. Dane nie trafiają do Git. Katalogi z testów są zachowane.

GPU: NVIDIA GeForce RTX 5070 Ti; Python 3.11.9; WhisperX 3.8.6; torch/torchaudio 2.8.0+cu128; CTranslate2 4.8.2; faster-whisper 1.2.1; transformers 4.57.6; pyannote.audio 4.0.7; NLTK 3.10.3; FFmpeg/FFprobe 8.1.2. Rewizje modeli zapisano w manifestach.

## Ostrzeżenia i NOT TESTED

Nie stwierdzono FAIL w końcowym zestawie. TorchCodec ostrzega o niedostępnych DLL dekodera; używany przepływ FFmpeg → tablica próbek przeszedł. Lightning adaptuje checkpoint w pamięci; nie wykonano sugerowanej migracji pliku. Pyannote wyłącza TF32 i ostrzega o odtwarzalności — zachowano zachowanie biblioteki.

Offline PASS oznacza zakończony pipeline z lokalnych zasobów, HF offline, zablokowanym nltk.download, siecią Python i zapisami poza zadaniem; nie test firewall ani audyt sieci bibliotek natywnych. Nie pobierano zasobów.

NOT TESTED: pełny RUI, jakość merytoryczna/polska terminologia, odsłuch synchronizacji, długie nagrania i VRAM/RAM, CPU i alternatywne compute, pełny przebieg bez alignmentu, wszystkie kontenery/kodeki, fizyczny brak GPU, OOM/dysk pełny/awaria zasilania, drugie stanowisko i ręczny odbiór wyglądu GUI. Te ograniczenia nie są przedstawiane jako PASS.

Kontrakt SHA256: 6fceb18b8e3170c78561182869c5d0ba542450eea61085b8994bf00f9594859c.
Standard SHA256: b004ed052a224e3be2d3b4ec379cbfca819fc933b9e79b729c79cfc31cf30e1c.
