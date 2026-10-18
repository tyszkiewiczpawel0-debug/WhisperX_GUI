# Architektura D2

Zaimplementowano Tkinter → kontroler → FFprobe/FFmpeg → adapter Python API WhisperX → biblioteczne writery.

| Moduł w src | Odpowiedzialność |
|---|---|
| gui.py | Tkinter w głównym wątku; wybór jednego z dwóch profili, parametry, metadane, etapy, log i wyniki |
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

## Kolejna wersja — profile i opcjonalny timeline

Jawny rejestr configuration.PROFILES mapuje dwa ID na stałe pliki JSON; profile() bez argumentu nadal webinar. GUI wczytuje definicje przy starcie, przełączenie resetuje cały formularz. Nie zapisuje plików i nie importuje dowolnych profili. Parametry zadania są kopiowane i walidowane przez kontroler i worker, bez ponownego odczytu profilu w workerze; parameters.id jest jedynym identyfikatorem profilu w request/run.

audio_timeline_mode jest płaską opcją parametrów: brak → legacy, jawnie legacy/preserve, pozostałe wartości odrzucane. Oba dostarczone profile mają domyślne legacy. Worker przekazuje wybór do wspólnego media.prepare(); preserve dodaje tylko jawny filtr aresample=16000:async=1:first_pts=0. Nie zmienia adaptera, writerów, Job Object, offline ani preflight. Przygotowanie nie stosuje heurystyki przełączania, łączenia materiałów, przesuwania wyników ani dopełniania do długości wideo. Przed wywołaniem FFmpeg odrzuca istniejący target, zachowując także -n. Próby nadpisania nie mogą zostać uznane za udane przygotowanie starego WAV.

Gdy źródło ma drobny offset, komunikat inspekcji zaleca kontrolę synchronizacji, zamiast zakładać metodę dekodowania przed wyborem trybu. Próg odrzucenia >0,1 s pozostaje bez zmian. Dowody i granice obsługi w [wynikach kolejnej wersji](../NEXT_VERSION_IMPLEMENTATION_PLAN.md#5-wykonanie-i-wyniki--18102026).

Testy ujawniły krótkotrwałe Windows WinError 5 podczas podmiany manifestu. artifacts.save zachowuje atomowy replace i poprzedni JSON, ponawia tylko WinError 5/32/33 najwyżej pięć razy (łącznie 0,30 s oczekiwania). Nie usuwa celu i nie ukrywa trwałych/innych błędów. Format eksportów i walidacja timestampów bez zmian.

## D2.1 — opcjonalny prompt

JSON `initial_prompt` → wielowierszowy widget Tkinter → kopia parametrów w kontrolerze/request.json → worker → `whisperx.load_model(asr_options={'initial_prompt': ...})`. Pole nie jest argumentem `model.transcribe`. Brak/null/pusty tekst/białe znaki normalizujemy do None; pozostały tekst zachowujemy dokładnie. Edycja nie zapisuje profilu. Inne parametry i etapy pozostają bez zmian.

WhisperX 3.8.6 scala asr_options z domyślnymi opcjami; jego batched ASR oczekuje str/None, mimo szerszego typu w faster-whisper. Biblioteka tokenizuje spację + strip tekstu, stosuje ten sam prompt w batchu; get_prompt z faster-whisper 1.2.1 ogranicza poprzedni kontekst do ostatnich 223 tokenów (max_length=448). Nie implementujemy własnego tokenizera ani limitu znaków. Stan przyjęcia opcji jest utrwalany przed transkrypcją; [semantyka metadanych](DATA.md).
