# WHISPERX_GUI

Lokalne GUI Tkinter do przygotowania i transkrypcji pojedynczego nagrania. Jeden profil WEBINAR_RUI_PL, bez diarizacji, streszczeń i kolejki.

**D0–D3: APPROVED. D4: COMPLETE wykonawczo — formalne zamknięcie MVP oczekuje na decyzję użytkownika.** [Ocena MVP: 6 PASS, 3 PARTIAL, 0 FAIL](docs/D4_MVP_REVIEW.md). [Raport D3](docs/D3_PILOT_REPORT.md). Dowody: [raport D2.1](docs/D2_1_TEST_REPORT.md), [raport D2](docs/D2_TEST_REPORT.md), [stan](docs/CURRENT_STATE.md), [handoff](99_HANDOFF/CURRENT/HANDOFF.md).

## Pierwsze uruchomienie

1. Otwórz `Start.cmd` dwuklikiem. Korzysta z interpretera w ignorowanym `config/local.toml`; nie instaluje pakietów. Polityka PowerShell dotyczy wyłącznie procesu uruchomienia, bez zmiany ustawień Windows.
2. Kliknij **Wybierz plik**, następnie **Sprawdź plik**. Zobaczysz format, kodek, czas, częstotliwość, kanały i ostrzeżenia.
3. Opcjonalnie **Przygotuj WAV** sprawdza konwersję bez silnika.
4. Sprawdź urządzenie, typ obliczeń, batch i alignment. Pole **Prompt transkrypcji (opcjonalny)** zawiera domyślny tekst profilu; możesz go edytować lub wyczyścić dla bieżącego uruchomienia. Profil nie zostanie zmieniony. **Transkrybuj** wykonuje pełny przebieg od oryginału, z własnym przygotowaniem WAV. Każda operacja tworzy osobny katalog; nie wznawia poprzedniego zadania.
5. **Przerwij** kończy wyłącznie procesy bieżącego zadania. Zamknięcie okna podczas pracy również anuluje zadanie i czeka na zapis stanu. **Otwórz wyniki** pokazuje ostatni katalog.

Lokalną konfigurację przygotowano w D2. Wyniki są w `runs/jobs/`, poza Git; dane testowe w innych podkatalogach `runs/`. Alternatywa: uruchom `Start.ps1` z PowerShell albo skonfigurowanym Pythonem `-B src/gui.py`. Nie uruchamiaj ani nie importuj źródłowego transcribe_trip_meeting.py.

Launcher korzysta jawnie z systemowego Windows PowerShell 5.1. Start.ps1 ma treść ASCII, a local.toml jest czytany jako UTF-8 (również ścieżki z polskimi znakami). Przy braku lub błędnej konfiguracji komunikat pozostaje w oknie konsoli do naciśnięcia klawisza; popraw wskazany plik według wzoru. Nie jest potrzebna instalacja PowerShell 7 ani zmiana globalnej polityki Windows.

## Wyniki i ograniczenia

Udana transkrypcja zawiera transcript.txt, transcript.srt, transcript.json, run.json i process.log. Manifest opisuje źródło, parametry, modele/revizje, wersje, czasy, ostrzeżenia i hashe kodu. request.json i work/ służą diagnostyce. Wszystkie pliki pośrednie pozostają również po sukcesie; nie ma automatycznego sprzątania.

Przygotowanie: PCM s16le / 16 kHz / mono. Próg ostrzeżenia długości 0,1 s jest konfigurowalny i nie gwarantuje synchronizacji. MVP odrzuca wiele ścieżek audio i offsety powyżej 0,1 s. Drobne niezerowe offsety są raportowane; napisy odnoszą się do początku zdekodowanego audio. Długość kontenera zastępuje brakującą długość ścieżki wyłącznie jako przybliżenie. Nie ma cichej korekty czasu.

Model large-v3 i język pl są stałe dla jedynego profilu. Można zmieniać urządzenie cuda/cpu, float16/float32/int8, batch 1–64 i alignment. CPU z float16 jest odrzucany. Nie ma automatycznej zmiany parametrów po błędzie. CPU i alternatywne typy obliczeń nie przeszły pełnego testu D2.

Opcjonalne pole JSON `initial_prompt` przyjmuje tekst albo null. Brak pola, null, pusty tekst lub same białe znaki oznaczają brak promptu. Dostarczony profil ma pustą wartość. Niepusty tekst jest przekazywany bez zmian i zapisywany w metadanych; biblioteka usuwa skrajne białe znaki przed tokenizacją i wykorzystuje najwyżej ostatnie 223 tokeny promptu. Stosuj krótki kontekst lub terminologię; prompt nie gwarantuje poprawnej transkrypcji. Szczegóły zapisu przy błędzie/anulowaniu: [dane](docs/DATA.md).

Brak lokalnych modeli, NLTK lub CUDA kończy zadanie czytelnym błędem. Pobieranie i automatyczne naprawy są wyłączone. Obecne ostrzeżenie TorchCodec nie zablokowało ścieżki FFmpeg → audio w pamięci. Długie nagrania są wczytywane do RAM. Pilotaż D3: webinar 1:58:43 przetworzony w 196,781 s; nie jest to benchmark ani gwarancja dla innych materiałów. RAM i szczyt VRAM nie zostały zmierzone. Użytkownik zaakceptował treść, kompletność i synchronizację w trzech odsłuchanych fragmentach; nie sprawdzono wszystkich 11903 słów. Cisza/szumy 01:30–03:40 prawdopodobnie wywołały halucynacyjne pożegnania; słychać echo o niepotwierdzonej przyczynie. Możliwe błędy terminologiczne wymagają kontroli. Końcowy znacznik jest 23,688 ms poza WAV, w tolerancji aplikacji 100 ms. Szczegóły i luki dowodowe GUI/drugiego stanowiska: [ocena D4](docs/D4_MVP_REVIEW.md).

## Nowe stanowisko

1. Uzyskaj lokalną kopię repozytorium. Nie skonfigurowano remote ani publikacji.
2. Wymagany Windows, Python 3.11 z Tkinter i istniejący zgodny stos WhisperX oraz FFmpeg/FFprobe. [Snapshot pakietów](docs/ENVIRONMENT_PACKAGES.txt) nie jest lockfile ani instrukcją automatycznej instalacji. Odtworzenie brakującego środowiska wymaga osobnej decyzji; nie kopiuj .venv.
3. Skopiuj config/local.example.toml do config/local.toml tylko jeśli nie istnieje. Wpisz pełne ścieżki, bez zmiennych i `~`. Pole python zachowaj jako pojedynczo cytowany literał TOML, jak we wzorze.
4. Wskaż HF hub z kompletnymi lokalnymi snapshotami Systran/faster-whisper-large-v3 i jonatasgrosman/wav2vec2-large-xlsr-53-polish, torch home, NLTK punkt_tab/polish oraz narzędzia. Wagi VAD należą do pakietu WhisperX. Pobranie brakujących zasobów wymaga osobnej autoryzacji.
5. Wybierz istniejący katalog nagrań i oddzielny katalog wyników poza źródłem i zasobami. Interpreter powinien mieć układ .venv/Scripts/python.exe; jego katalog projektu jest chroniony przez walidację.
6. Uruchom Start.cmd i testy z [tests/README.md](tests/README.md) na krótkim lokalnym materiale. Drugie stanowisko nie zostało zweryfikowane.

## Dokumentacja

- [Kontrakt](docs/PROJECT_CONTRACT.md), [AGENTS](AGENTS.md), [standard pomocniczy](PROJECT_STANDARD_v0.2.md) — bez zmian.
- [Architektura](docs/ARCHITECTURE.md), [dane](docs/DATA.md), [decyzje](docs/DECISIONS.md).
- Historyczne D0: [discovery](DISCOVERY_REPORT.md), [reuse](REUSE_MATRIX.md), [rekomendacja](MVP_RECOMMENDATION.md).
- [Konfiguracja](config/local.example.toml), [profil](config/WEBINAR_RUI_PL.json), [moduły](src/README.md), [testy](tests/README.md).

D3 zatwierdzono po dodatkowym odsłuchu użytkownika 14.10.2026. Pierwotny raport D3 zachowuje historyczny status PARTIAL. Formalne zamknięcie MVP należy do użytkownika w głównej rozmowie ChatGPT; dalszy rozwój wymaga osobnego zlecenia.
