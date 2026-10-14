# Raport weryfikacji D2 — 14.10.2026

Status wykonawczy: COMPLETE, do odbioru użytkownika. Testy nie stanowią pilotażu RUI.

## Poprawka pierwszego uruchomienia — 14.10.2026

Zgłoszony przez użytkownika FAIL odtworzono: Start.ps1:3 char:64, Unexpected token 'nij'. Plik miał UTF-8 bez BOM; Start.cmd wywoływał powershell.exe, czyli systemowy Windows PowerShell **5.1.26100.9711**, z domyślną stroną kodową **1250**. Bajty UTF-8 litery ł (C5 82) zostały odczytane jako Ĺ oraz znak U+201A rozpoznawany przez parser jako cudzysłów. Wcześniejsza kontrola składni była wykonana w PowerShell **7.6.5**, a test Tkinter omijał launcher. Jej PASS nie dowodził poprawnego pierwszego uruchomienia przez Start.cmd.

Poprawka: bootstrap ASCII, jawne czytanie konfiguracji UTF-8, systemowy pełny adres powershell.exe, kontrola obecności TOML/pola python/interpretera, zachowanie kodu wyjścia także po pause. Startowy błąd loadera GUI jest wypisywany do konsoli i zwraca 1. Konsola pozostaje otwarta. Nie zmieniono silnika, środowiska ani konfiguracji użytkownika.

Testowana była rzeczywista ścieżka cmd.exe /c Start.cmd → Windows PowerShell 5.1 → skonfigurowany Python → niezmokowane GUI, również z innym katalogiem roboczym. Potwierdzono widoczne okno przez computer-use, bez uruchamiania transkrypcji; zamknięcie okna daje kod 0. Nie wykonano gestu dwukliku w Explorerze — uruchomiono tę samą ścieżkę CMD programowo. Końcowy ręczny odbiór użytkownika pozostaje wymagany.

| Test | Wynik | Dowód w ignorowanym runs/ |
|---|---|---|
| Produkcyjny launcher, rzeczywiste GUI i zamknięcie | PASS, kod 0 | launcher_f001eea7bdce48b986856a9b98e4a2cc/results.json |
| Brak TOML / błędne pole python / brak interpretera | PASS, 3 czytelne komunikaty, kod 1 | launcher_fa398d0b27f04d26b5ccfbcabd5f9005/results.json |
| Niepoprawna składnia TOML po korekcie obsługi błędu | PASS, komunikat i wskazanie local.toml, kod 1 | launcher_32de8942a9f743f4a6382218a173df02/results.json |
| Katalog ze spacjami i polskimi znakami | PASS, widoczne GUI i kod 0 | launcher_9914621a437c48f19aa2d0a12133b3eb/results.json |

Pierwszy test niepoprawnego TOML z poprzednim modalnym komunikatem przekroczył 120 s; nie znaleziono targetowalnego okna komunikatu. Po zmianie na trwały komunikat konsoli test przeszedł. Kontrola procesów po timeout nie wykazała pozostałych procesów tego katalogu testowego. Test regresji: tests/check_launcher.py; błędne przypadki na wydzielonych kopiach, porównanie hasha local.toml przed/po. Nie nadpisywano konfiguracji użytkownika. Nie wykonywano ponownie GPU ani testów silnika. Poniższe wyniki są historycznym zapisem implementacji D2 sprzed poprawki launchera.

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
