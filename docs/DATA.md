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
