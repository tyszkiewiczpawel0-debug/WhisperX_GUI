# WHISPERX_GUI — checkpoint D2.1

Data: 14.10.2026. Odbiorca: główna rozmowa ChatGPT projektu WHISPERX_GUI, za pośrednictwem użytkownika.

**Status: COMPLETE wykonawczo, do odbioru.** Zlecenie „D2.1: INITIAL PROMPT — AUTHORIZED” formalnie zatwierdza D2. D3 nie rozpoczęto; wymaga osobnej autoryzacji.

## Implementacja i API

Lokalnie potwierdzono WhisperX 3.8.6/faster-whisper 1.2.1: `whisperx.load_model(..., asr_options={'initial_prompt': tekst_lub_None})`. Nie jest to argument model.transcribe. Kod batched ASR oczekuje str/None; strip i tokenizacja należą do biblioteki. Kontekst jest ograniczony do ostatnich 223 tokenów. Nie zmieniono VAD, alignmentu, audio ani pozostałych parametrów.

Profil JSON dopuszcza opcjonalne initial_prompt i zachowuje zgodność wcześniejszego schematu. Dostarczona wartość jest pusta. Brak/null/pusty tekst/same białe znaki → brak promptu; inny tekst jest przekazywany i zapisywany dokładnie. GUI wczytuje domyślną wartość, pozwala edytować/wyczyścić tekst; zmiana dotyczy uruchomienia i nie zapisuje profilu. Pole pozostaje w głównym oknie.

run.json: parameters.initial_prompt to konfiguracja; główne initial_prompt + initial_prompt_state potwierdzają przyjęcie opcji przez silnik. not_submitted oznacza etap przed przekazaniem, submission_unconfirmed przerwanie/błąd w okolicy load_model, accepted_by_engine pomyślny powrót load_model. Nie mylić niepotwierdzonego null z potwierdzonym pustym promptem. Późniejszy błąd/anulowanie zachowuje potwierdzoną wartość. [Pełna semantyka](../../docs/DATA.md).

## Zmienione pliki

Kod: src/configuration.py, gui.py, controller.py, engine.py, worker.py. Konfiguracja: config/WEBINAR_RUI_PL.json. Testy: tests/test_prompt.py, tests/README.md. Dokumentacja: README.md, docs/ARCHITECTURE.md, DATA.md, DECISIONS.md, CURRENT_STATE.md, D2_1_TEST_REPORT.md i ten jeden bieżący handoff. Bez zmian kontraktu, standardu i launcherów.

## Testy i ochrona

PASS: 16/16 testów (11 regresji D2 + 5 nowych z podprzypadkami). Pokryte brak/pusty/domyslny prompt, nieprawidłowe typy, rzeczywisty widget Tkinter, edycja/wyczyszczenie, niezmienność profilu, dokładne argumenty adaptera, trwałe metadane przy sukcesie/błędach i wczesnym anulowaniu. Testy adaptera/orkiestracji workera używają atrap kosztownych operacji; test kontrolera uruchamia prawdziwy worker.

Rzeczywisty krótki pipeline z promptem: 20 s próbki D2, large-v3/pl/cuda/float16/batch 8/alignment, succeeded, 6 segmentów, 25,047 s, komplet pięciu wyników. Dokładny prompt potwierdzony w run.json, brak pełnego tekstu w process.log. Wynik: runs/jobs/20261014_184459_6d3c189f03194b9586b81fea97116ea8. Dowody: runs/d21_40fc899cc42a4be0b03cb9e1950390b1. [Raport](../../docs/D2_1_TEST_REPORT.md).

Składnia Python i granice układu rzeczywiście utworzonego GUI przy 940x810 i 760x680 — PASS. Ręczny odbiór wyglądu/dwukliku pozostaje po stronie użytkownika. Launchery niezmienione; wcześniejsza poprawka Windows PowerShell i jej testy są w [raporcie D2](../../docs/D2_TEST_REPORT.md).

Źródło C:\AI\WhisperX: 46565 plików bez zmian ścieżki/rozmiaru/mtime_ns przed/po; nie pełny hash instalacji. SHA256 próbki identyczne. Brak modyfikacji źródła, .venv, modeli, konfiguracji użytkownika, nagrań i poprzednich wyników. Bez instalacji/pobrań/drugiego venv/push. Każdy przebieg miał osobny katalog poza Git.

NOT TESTED w D2.1: pełny RUI, jakość/terminologia/synchronizacja długiego nagrania, CPU/inne compute i drugie stanowisko. Nie powtarzano kosztownych testów anulowania GPU z D2. Ostrzeżenie TorchCodec nadal nie blokuje ścieżki FFmpeg.

## Git i kolejny krok

Branch: main. Lokalny commit zamykający: „Add optional transcription prompt with execution provenance”. Jego SHA zostaje podane w odpowiedzi końcowej po kontroli statusu/brancha; nie można wpisać SHA własnego commita do jego treści. Przegląd staged diff obejmuje zakres i dane wrażliwe; dane wykonawcze i local.toml pozostają ignorowane. Bez remote/push.

Gotowość techniczna do D3 po odbiorze D2.1 i odrębnej autoryzacji użytkownika. Prompt terminologiczny można ustalić w pilotażu. Start: dwuklik Start.cmd, wybór nagrania, opcjonalna edycja promptu, Transkrybuj. Na D2.1 prace zakończono; pilotażu nie uruchomiono.
