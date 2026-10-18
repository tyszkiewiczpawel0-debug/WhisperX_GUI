# Testy D2

Uruchamiaj w repozytorium skonfigurowanym Pythonem 3.11 z -B:

```powershell
& '<python z config/local.toml>' -B tests/test_mvp.py
& '<python z config/local.toml>' -B tests/check_exports.py
& '<python z config/local.toml>' -B tests/check_engine.py '<krótka wydzielona próbka PL>'
& '<python z config/local.toml>' -B tests/check_cancellation.py '<krótka wydzielona próbka PL>'
```

test_mvp: 11 testów konfiguracji, brakujących modeli, metadanych, błędów wejścia, WAV/MKV, wielu ścieżek/braku audio, różnicy długości, ponowienia, Tkinter i Job Object z potomnym FFmpeg oraz niezależnym procesem kontrolnym. Wymaga Windows/Tkinter i lokalnego TOML.

check_exports: rzeczywiste writery, polski tekst, granice minut/godzin, blokada sieci i zapisu poza zadaniem, bez modeli. check_engine: pełny krótki pipeline. check_cancellation: przerwanie w ASR i alignment z kontrolą stanu i zachowania WAV. Nie podawaj pełnego webinaru D3.

Testy tworzą własne katalogi runs i nie sprzątają ich automatycznie. Nie instalują ani nie pobierają zasobów. Wyniki: [raport D2](../docs/D2_TEST_REPORT.md).

## D2.1

`-B -m unittest discover -s tests -p 'test_*.py' -v` uruchamia 16 testów: dotychczasowe 11 oraz 5 z test_prompt.py (z podprzypadkami). Nowe testy sprawdzają zgodność profilu, walidację, rzeczywisty widget Tkinter, edycję/wyczyszczenie bez zapisu profilu, dokładne opcje adaptera, trwałe metadane etapów i błędów, kontroler z błędem wejścia i natychmiastowym anulowaniem. Wywołania silnika w testach jednostkowych są zastąpione atrapami; testy kontrolera używają prawdziwego procesu workera. Oddzielny krótki przebieg rzeczywistego silnika opisuje [raport D2.1](../docs/D2_1_TEST_REPORT.md).

## Regresja launchera

`tests/check_launcher.py` uruchamiaj istniejącym Pythonem z `-B` i argumentem:

- `errors`: brak TOML, błędne pole python, brak interpretera — automatycznie sprawdza komunikaty i kod 1.
- `invalid-toml`: uszkodzony TOML — komunikat konfiguracji w konsoli, kod 1.
- `valid`: produkcyjny Start.cmd → Windows PowerShell 5.1 → rzeczywiste GUI; sprawdź okno i zamknij je, oczekiwany kod 0.
- `unicode`: identyczne launchery i moduły w katalogu ze spacjami/polskimi znakami; sprawdź i zamknij rzeczywiste GUI, kod 0.

Testy nie zastępują GUI atrapą i nie uruchamiają silnika. Błędne konfiguracje są tworzone wyłącznie w nowych katalogach runs/launcher_UUID; hash konfiguracji użytkownika jest kontrolowany. Limit 120 s; po jego przekroczeniu test kończy tylko własne drzewo procesów. Skrypt PowerShell musi pozostać ASCII, co sprawdza test. Dla ręcznego odbioru końcowego użyj dwukliku Start.cmd.

## Kolejna wersja — dwa profile i opcjonalny preserve

Dotychczasowe discover uruchamia teraz 24 testy (w tym 32 podprzypadki orkiestracji workera). Dodano: rejestr i zgodność ID pliku, domyślne wartości, bajtową zgodność webinarowego JSON z tagiem, walidację trybu, A → B → A i reset wszystkich pól w prawdziwym Tkinter, blokadę wyboru i przywrócenie dla stanów końcowych, snapshoty obu profili/trybów przez rzeczywisty worker, niezmienione polecenie legacy, syntetyczną przerwę PTS, odmowę nadpisania WAV i ograniczone ponowienie podmiany JSON przy blokadzie Windows. Atrapy ASR pozostają jawne. Czyszczenie cykli Tk w testach odbywa się w głównym wątku, aby nie trafiły do kolektora wątku kontrolera.

check_engine.py i check_cancellation.py przyjmują opcjonalnie po ścieżce próbki ID profilu i tryb audio, np. `'<krótka próbka.wav>' sesja_rady_gminy preserve`. Bez nowych argumentów nadal używają webinaru/legacy. Nie używaj pełnej sesji do testu silnika. check_exports.py dodatkowo sprawdza zachowanie słów z timestampami i bez nich w JSON.

[Raport wykonania i AUDIO-01](../NEXT_VERSION_IMPLEMENTATION_PLAN.md#5-wykonanie-i-wyniki--18102026) odróżnia rzeczywisty krótki ASR, pomiary waveform, atrapy i niewykonane kontrole użytkownika. Dane i pełne logi pozostają poza Git w runs.


Finalizacja v1.1.0: test wartości domyślnych oczekuje sesja=preserve, webinar=legacy i nadal brak pola=legacy. Dodatkowy test uruchamia rzeczywisty worker prepare dla obu profili bez nadpisania trybu oraz porównuje request/run i wykonane polecenie. Test przełączania GUI sprawdza także przeniesienie domyślnego trybu do parametrów zadania. W finalizacji nie powtarza się pełnej transkrypcji ani wcześniejszych pomiarów AUDIO-01; wyniki i odbiór użytkownika w sekcji 6 planu.


Poprawka provenance v1.1.1: test_application_provenance sprawdza stałe aplikacji/wersji i ich zgodność z manifestami realnego workera inspect/prepare dla obu profili, zachowanie schema_version=1, parametrów request/run, hashy kodu i listy wyników. Dotychczasowe testy błędu wejścia i anulowania sprawdzają również zachowanie application/application_version. Bez uruchamiania ASR; check_exports.py nadal używa prawdziwych writerów i blokad offline/zapisu.
