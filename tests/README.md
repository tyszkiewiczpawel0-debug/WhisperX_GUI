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

## Regresja launchera

`tests/check_launcher.py` uruchamiaj istniejącym Pythonem z `-B` i argumentem:

- `errors`: brak TOML, błędne pole python, brak interpretera — automatycznie sprawdza komunikaty i kod 1.
- `invalid-toml`: uszkodzony TOML — komunikat konfiguracji w konsoli, kod 1.
- `valid`: produkcyjny Start.cmd → Windows PowerShell 5.1 → rzeczywiste GUI; sprawdź okno i zamknij je, oczekiwany kod 0.
- `unicode`: identyczne launchery i moduły w katalogu ze spacjami/polskimi znakami; sprawdź i zamknij rzeczywiste GUI, kod 0.

Testy nie zastępują GUI atrapą i nie uruchamiają silnika. Błędne konfiguracje są tworzone wyłącznie w nowych katalogach runs/launcher_UUID; hash konfiguracji użytkownika jest kontrolowany. Limit 120 s; po jego przekroczeniu test kończy tylko własne drzewo procesów. Skrypt PowerShell musi pozostać ASCII, co sprawdza test. Dla ręcznego odbioru końcowego użyj dwukliku Start.cmd.
