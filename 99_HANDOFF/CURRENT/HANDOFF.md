# WHISPERX_GUI — lokalny kandydat poprawki provenance v1.1.1

Data: 18.10.2026. Odbiorcy: **użytkownik i główna rozmowa ChatGPT projektu WhisperX_GUI**.

**PATCH READY — PENDING ACCEPTANCE**

Punkt wyjścia: czysty main=origin/main=opublikowany v1.1.0, `fc5e2c76966c4219c50c0955ff3898c064614613`. Poprawka na lokalnej gałęzi `codex/provenance-1-1-1`. Dokładny SHA commita z kodem i tym checkpointem jest w końcowym przekazaniu i lokalnym runs/patch_1_1_1_00312c231de54295b715b44ebfe0d963/patch_commit.json; na gałęzi odtworzysz go przez git rev-parse HEAD. main, mvp-v1.0 i v1.1.0 nie są przesuwane. Nie utworzono tagu v1.1.1 ani nie wykonano push/publikacji poprawki.

## Zakres i kompatybilność

Jedynym miejscem nadawania starego identyfikatora był Controller.start; nie było centralnego źródła wersji aplikacji. Wykorzystano istniejący configuration.py: APPLICATION_ID=WHISPERX_GUI, APPLICATION_VERSION=1.1.1. Controller tworzy z tych stałych pola application/application_version i używa tego samego ID jako dotychczasowego prefiksu logu. Bez nowego modułu lub runtime zależnego od Git.

Dodane pole wersji jest metadaną schema 1. Pozostałe pola provenance, request, TXT/SRT/transcript.json i ich znaczenie bez zmian. Stare manifesty z WHISPERX_GUI D2.1 bez application_version pozostają historyczne; brak migracji, nowych wymagań przy odczycie i modyfikacji wyników. Zmiany produkcyjne ograniczone do configuration.py i controller.py; profili, domyślnego preserve sesji/legacy webinaru, ASR, worker/offline/anulowania/Job Object ani środowiska nie zmieniono.

## Weryfikacja i kontynuacja

- **PASS:** 24/24 unittest (6,717 s), w tym nowy test tożsamości/wersji z realnym workerem inspect/prepare obu profili, schema 1, parametry request/run, hashe kodu i lista wyników. Pola sprawdzane także po błędzie wejścia i anulowaniu.
- **PASS:** rzeczywiste writery TXT/SRT/JSON oraz blokady offline/zapisu, AST; nadal poprawne profile i istniejąca regresja pipeline'u.
- **PASS:** 134 wcześniejsze run.json z identycznymi SHA-256 przed/po; 15 nowych manifestów ma application=WHISPERX_GUI/application_version=1.1.1. Produkcyjne moduły i konfiguracje poza zakresem bez zmian w diff względem v1.1.0.
- **FAIL:** 0. **NOT TESTED w poprawce:** rzeczywisty ASR i pełna transkrypcja; brak zmian silnika nie uzasadniał ich ponawiania. Wcześniejsze ograniczenia v1.1.0 (pełny preserve, pełny odsłuch/jakość, inne stanowisko/compute) nie otrzymują nowych ocen PASS.

Logi i proof.json wyłącznie w powyższym ignorowanym katalogu runs. [CURRENT_STATE](../../docs/CURRENT_STATE.md), [DATA](../../docs/DATA.md), [DECISIONS D-55–D-58](../../docs/DECISIONS.md), [testy](../../tests/README.md). Uruchomienie Start.cmd bez zmian; nowa operacja inspect/prepare/transcribe tworzy manifest z nowymi polami. Nie używać starych wyników do oceny nowej wersji pola application.

Rekomendacja Work: poprawka v1.1.1 gotowa do odbioru w opisanym zakresie. Odbiór, integracja z main, tag i publikacja wymagają osobnej decyzji użytkownika; nie rozpoczynano tych operacji.
