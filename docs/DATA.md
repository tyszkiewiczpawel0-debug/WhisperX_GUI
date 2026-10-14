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

Próg różnicy długości 0,1 s jest konfigurowalnym założeniem. Brak audio, wiele ścieżek i offset ponad 0,1 s są odrzucane. Drobny offset jest raportowany; napisy względem początku dekodowanego audio. Przy braku długości ścieżki używana jest długość kontenera jako przybliżenie. Brak obu uniemożliwia porównanie. Bez korekty ciszy, tempa i osi czasu.

D2 użył syntetycznych WAV/MKV oraz wycinka 30–50 s istniejącego źródłowego WAV, zapisanego w runs/d2_checks. To nie webinar RUI. W Git są tylko kod, konfiguracja przykładowa/profil, testy i dokumenty; źródło, środowisko i modele pozostają tylko do odczytu.

## D2.1 — prompt i potwierdzenie przekazania

`parameters.initial_prompt` w run.json i request.json oznacza wartość wybraną dla zadania: dokładny niepusty tekst albo null dla braku/pustego tekstu/samych białych znaków. Główne `initial_prompt` w run.json to dokładny tekst potwierdzony po pomyślnym powrocie load_model, albo null. Zawsze interpretuj je razem z `initial_prompt_state`:

| Stan | Znaczenie |
|---|---|
| not_submitted | Nie rozpoczęto przekazywania opcji ASR; dotyczy także inspect/prepare i wcześniejszego błędu/anulowania |
| submission_unconfirmed | Rozpoczęto ładowanie ASR; błąd/przerwanie nie pozwala potwierdzić przyjęcia opcji. Główne initial_prompt pozostaje null; nie oznacza to dowodu, że silnik dostał pusty prompt |
| accepted_by_engine | load_model przyjął opcje; główne initial_prompt zawiera tekst albo null dla świadomie pustego promptu |

Stan accepted_by_engine nie gwarantuje wygenerowania segmentów ani jakości użycia kontekstu. Późniejszy błąd/anulowanie zachowuje potwierdzoną wartość. Zapis przed wywołaniem i po powrocie jest celowo ostrożny: zabicie procesu między powrotem biblioteki a zapisem może pozostawić submission_unconfirmed. Nie udajemy atomowości operacji biblioteki i zapisu JSON. Pełny tekst nie jest dopisywany przez aplikację do process.log; pozostaje prywatną zawartością request.json/run.json poza Git.
