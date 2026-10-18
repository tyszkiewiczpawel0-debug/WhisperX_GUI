# Bieżący stan — 18.10.2026, kolejna wersja

**IMPLEMENTATION COMPLETE — PENDING ACCEPTANCE**

Użytkownik zleceniem IMPLEMENTATION AUTHORIZED zatwierdził implementację po analizie. Zamknięte MVP v1 / D4 APPROVED pozostaje w tagu `mvp-v1.0` (`a677fc6f62620752156fd2565edac6e3585090e0`), z historycznym wynikiem 6 PASS / 3 PARTIAL / 0 FAIL. Nowa wersja nie jest jeszcze odebrana przez użytkownika.

Gałąź robocza: `codex/multiple-profiles`. Analiza: commit `23d0786`; implementacja: `459fd15b7e84892762aab972fb80a3556f54275f`. Po nim checkpoint dokumentacyjny; bieżący identyfikator HEAD odczytuje `git rev-parse HEAD`. Bez push, nowego tagu lub operacji zdalnych.

Dwa profile w GUI: WEBINAR_RUI_PL (domyślny) i sesja_rady_gminy. Wybór resetuje wszystkie nadpisania, podczas pracy jest zablokowany; GUI nie zapisuje plików profili. Nowa sesja: large-v3/pl/cuda/float16/batch8/alignment=true/diarization=false/pusty prompt, alignment można wyłączyć dla zadania. Webinarowy JSON bez zmiany bajtów. Worker używa snapshotu, parameters.id i rzeczywistych ustawień, normalizacja promptu i potwierdzenie silnika zachowane.

Opcjonalne audio_timeline_mode=legacy|preserve; brak oznacza legacy, więc oba dostarczone profile pozostają legacy. Preserve dodaje tylko aresample=16000:async=1:first_pts=0 i addytywne metadane. Brak automatycznego wyboru/przełącznika GUI. Dla AUDIO-01 zalecane jawne preserve: zwykły WAV przesuwa sprawdzone zdarzenia o 109–405 ms, filtrowany zachowuje ich pozycje w pięciu punktach. AUDIO-01 ma 98:04,600, nie 76 min; audio/WAV preserve 5884,501 s, legacy 5884,096 s. Różnica 99 ms do końca wideo pozostaje bez dopełniania. Aktywacja preserve przed startem GUI opisana w [README](../README.md).

Końcowa weryfikacja: **22/22 unittest PASS**, rzeczywiste eksporty i blokady sieci/zapisu PASS, krótkie 20 s ASR sesji/preserve succeeded (4 segmenty, 29/29 słów z czasami), anulowanie aktywnego FFmpeg i Job Object PASS, AST/config PASS. Windows sporadycznie blokował atomowy replace JSON; dodano ograniczone ponowienie bez usuwania poprzedniego pliku i test trwałego błędu. Nie ma pełnej transkrypcji sesji.

SHA-256 AUDIO-01 przed/po identyczny, webinarowy profil/local.toml bez zmian hashy. 46565 plików referencyjnego WhisperX bez zmian ścieżek/rozmiarów/mtime_ns; nie pełne hashe instalacji. Bez instalacji, pobrań, zapisu do źródła, usuwania dawnych wyników i zmiany kontraktu/standardu.

**NOT TESTED:** ręczna obsługa widocznego GUI podczas rzeczywistego ASR, ocena treści/odsłuch/lip-sync przez użytkownika, ponowne realne anulowanie ASR/alignmentu, osobny ASR webinaru, CPU/inne compute i drugie stanowisko. Automatyczny pomiar waveform nie zastępuje pełnego odsłuchu. Trzech historycznych PARTIAL D4 nie przekwalifikowano na PASS.

[Zakres i raport z dowodami](../NEXT_VERSION_IMPLEMENTATION_PLAN.md#5-wykonanie-i-wyniki--18102026), [historyczna analiza](../NEXT_VERSION_ANALYSIS.md), [decyzje D-44–D-50](DECISIONS.md), [bieżący handoff](../99_HANDOFF/CURRENT/HANDOFF.md). Uruchomienie: Start.cmd → wybór profilu → krótkie nagranie → Transkrybuj. Rekomendacja Work: gotowe do odbioru w opisanym zakresie; decyzja należy do użytkownika i głównej rozmowy, kolejnego etapu nie rozpoczęto.
