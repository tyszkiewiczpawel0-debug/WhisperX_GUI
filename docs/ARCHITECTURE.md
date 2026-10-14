# Architektura D2

Zaimplementowano Tkinter → kontroler → FFprobe/FFmpeg → adapter Python API WhisperX → biblioteczne writery.

| Moduł w src | Odpowiedzialność |
|---|---|
| gui.py | Tkinter w głównym wątku; jeden profil, parametry, metadane, etapy, log i wyniki |
| configuration.py | TOML, JSON, walidacja parametrów i separacji chronionych katalogów |
| controller.py | Jeden worker, katalog UUID, wątek odczytu logów, kolejka zdarzeń, końcowy manifest |
| winjob.py | Windows Job Object z kill-on-close; anulowanie wyłącznie własnego drzewa |
| worker.py | Tryby inspect/prepare/transcribe, etapy, ostrzeżenia i manifest |
| media.py | Cienkie wywołania FFprobe/FFmpeg; diagnostyka długości/offsetów |
| safety.py | Offline, cache zadania i Python audit hook blokujący sieć/zapisy poza zadaniem |
| engine.py | Preflight, ASR/VAD, zwalnianie pamięci, alignment |
| artifacts.py | get_writer TXT/SRT/JSON, walidacja zakresów i kompletności, zapis manifestu |

Worker korzysta z istniejącego interpretera z -B -u. Czeka na stdin GO, zanim wykona pracę: kontroler najpierw przypisuje go do Job Object. Potomny FFmpeg dziedziczy przynależność. Błąd przypisania kończy oczekujący proces; brak globalnego taskkill. Zamknięcie uchwytu kończy pozostałych potomków. UI odbiera ograniczoną liczbę zdarzeń co 100 ms, bez importów silnika.

REUSE: Tkinter, Python/stos, FFprobe/FFmpeg, WhisperX/faster-whisper/CTranslate2, modele, VAD i get_writer. ADAPT: sekwencja load_audio → ASR → gc/empty_cache → alignment → gc/empty_cache ze źródłowego transcribe_trip_meeting.py, bez importu tego skryptu i jego błędnej srt_ts. BUILD: warstwa użytkowa, kontroler, walidacja, ochrona i provenance.

Preflight sprawdza lokalny snapshot refs/main i wymagane pliki, NLTK PL, CUDA i wspierany typ obliczeń. Adapter przekazuje lokalne ścieżki modeli i local_files_only/model_cache_only. nltk.download jest blokowany, HF offline i wyłączenie telemetryki aktywne przed importem silnika. Cache TEMP/CUDA/MPL/Numba trafiają do work/cache. Audit hook stanowi ochronę dla operacji Python, nie systemowy sandbox bibliotek natywnych; krótki przebieg przeszedł z aktywną ochroną.

Eksport powstaje w work/export, jest walidowany i przenoszony do nazw końcowych. succeeded wymaga kompletu pięciu plików. Zestaw nie jest jedną transakcją; po przerwaniu częściowe wyniki nie oznaczają sukcesu. Rozstrzyga run.json. Brak wznawiania i sprzątania.
