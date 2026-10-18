# Dane i pochodzenie — D2

| Warstwa | Lokalizacja | Ochrona |
|---|---|---|
| SOURCE | Wybrany oryginał | Tylko odczyt; ścieżka, rozmiar, mtime i metadane w manifeście |
| DERIVED | UUID/work/audio.wav | PCM 16 kHz mono; polecenie i różnica długości w run.json |
| WORKING | UUID/work/cache i work/export | Cache procesu i etap eksportu |
| OUTPUT | UUID/transcript.txt, .srt, .json, run.json, process.log | Status succeeded dopiero po kontroli kompletu |

Każda operacja tworzy nowy katalog data/czas + UUID, również inspekcja i przygotowanie. Walidacja odrzuca nakładanie output z projektem interpretera, input_dir i katalogami zasobów; rozwiązuje ścieżki przed porównaniem. Plik wejściowy nie może należeć do bazy wyników.

run.json: identyfikator, status/etap, źródło, parametry, modele/revizje, wersje, GPU, hashe kodu, czas UTC i czas wykonania, rezultaty, błędy/ostrzeżenia. request.json zawiera tylko dozwolone pola konfiguracji. Nie zapisujemy tokenów ani całego środowiska. Log i metadane są prywatnymi danymi poza Git.

Zachowujemy pośrednie po sukcesie, błędzie i anulowaniu. Aplikacja nie usuwa istniejących plików. Awaria całego GUI/systemu może pozostawić running; ponowienie tworzy nowe zadanie bez automatycznej naprawy. TXT/SRT przy failed/cancelled nie oznaczają sukcesu.

Próg różnicy długości 0,1 s jest konfigurowalnym założeniem. Brak audio, wiele ścieżek i offset ponad 0,1 s są odrzucane. Drobny offset jest raportowany; w legacy napisy względem początku dekodowanego audio. Przy braku długości ścieżki używana jest długość kontenera jako przybliżenie. Brak obu uniemożliwia porównanie. Legacy nie koryguje ciszy, tempa i osi czasu.

D2 użył syntetycznych WAV/MKV oraz wycinka 30–50 s istniejącego źródłowego WAV, zapisanego w runs/d2_checks. To nie webinar RUI. W Git są tylko kod, konfiguracja przykładowa/profil, testy i dokumenty; źródło, środowisko i modele pozostają tylko do odczytu.

## D2.1 — prompt i potwierdzenie przekazania

`parameters.initial_prompt` w run.json i request.json oznacza wartość wybraną dla zadania: dokładny niepusty tekst albo null dla braku/pustego tekstu/samych białych znaków. Główne `initial_prompt` w run.json to dokładny tekst potwierdzony po pomyślnym powrocie load_model, albo null. Zawsze interpretuj je razem z `initial_prompt_state`:

| Stan | Znaczenie |
|---|---|
| not_submitted | Nie rozpoczęto przekazywania opcji ASR; dotyczy także inspect/prepare i wcześniejszego błędu/anulowania |
| submission_unconfirmed | Rozpoczęto ładowanie ASR; błąd/przerwanie nie pozwala potwierdzić przyjęcia opcji. Główne initial_prompt pozostaje null; nie oznacza to dowodu, że silnik dostał pusty prompt |
| accepted_by_engine | load_model przyjął opcje; główne initial_prompt zawiera tekst albo null dla świadomie pustego promptu |

Stan accepted_by_engine nie gwarantuje wygenerowania segmentów ani jakości użycia kontekstu. Późniejszy błąd/anulowanie zachowuje potwierdzoną wartość. Zapis przed wywołaniem i po powrocie jest celowo ostrożny: zabicie procesu między powrotem biblioteki a zapisem może pozostawić submission_unconfirmed. Nie udajemy atomowości operacji biblioteki i zapisu JSON. Pełny tekst nie jest dopisywany przez aplikację do process.log; pozostaje prywatną zawartością request.json/run.json poza Git.

## Kolejna wersja — tożsamość profilu i przygotowanie

parameters.id w request.json i run.json identyfikuje WEBINAR_RUI_PL albo sesja_rady_gminy. Nie ma dodatkowego profile_id. Schema_version pozostaje 1; rozszerzenia są addytywne. Pusty prompt obu profili nadal normalizowany jest do null.

parameters.audio_timeline_mode zapisuje wybrany tryb legacy/preserve, także gdy przygotowania jeszcze nie wykonano. Brak pola w starszym request oznacza legacy. Od finalizacji v1.1.0 profil sesji zawiera jawne audio_timeline_mode=preserve. Webinar pozostaje legacy; jego JSON bez zmiany bajtów. Brak pola nadal oznacza legacy także dla starszych requestów sesji; worker nie zastępuje snapshotu nowymi wartościami domyślnymi z pliku profilu.

Po udanym przygotowaniu preparation zawiera dodatkowo:

| Pole | Znaczenie |
|---|---|
| audio_timeline_mode | Faktycznie ukończony wariant przygotowania |
| timeline_reference | decoded_audio_start dla legacy; source_timestamps_zero dla preserve, gdzie filtr przyjmuje first_pts=0 |
| source_audio_duration_seconds | Długość ścieżki, null jeśli użyto przybliżenia kontenerem |
| source_container_duration_seconds | Długość kontenera z FFprobe, albo null |
| container_duration_delta_seconds | WAV minus kontener, albo null |

Istniejące preparation.metadata.duration to długość WAV, a duration_delta_seconds nadal porównuje z source.metadata.duration (audio albo dotychczasowe przybliżenie). preparation.command zachowuje pełne polecenie z filtrem tylko dla preserve. Ten wariant ostrzega także o różnicy względem kontenera powyżej tego samego progu, bez zmiany znaczenia starej delty. Pełne surowe metadane źródła i WAV pozostają zachowane.

Brak preparation po błędzie/anulowaniu nie potwierdza wykonania wybranego wariantu. Częściowy WAV jest zachowywany. timeline_reference opisuje założenie polecenia, nie certyfikat synchronizacji mowy/wideo. Ograniczenia offsetów i wyboru ścieżki pozostają bez zmian; preserve nie odtwarza nieznanej referencji ani nie przesuwa gotowych eksportów.
