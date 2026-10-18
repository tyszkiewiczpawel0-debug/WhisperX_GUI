# Bieżący stan — 18.10.2026, poprawka provenance v1.1.1

**PATCH READY — PENDING ACCEPTANCE**

Punkt wejścia: czysty main i origin/main równy opublikowanemu v1.1.0, commit `fc5e2c76966c4219c50c0955ff3898c064614613`. Minimalna poprawka jest na lokalnej gałęzi `codex/provenance-1-1-1`; main i historyczne tagi pozostają bez zmian. Bez push, nowego tagu v1.1.1 i publikacji poprawki. Dokładny SHA lokalnego commita podaje przekazanie końcowe; na gałęzi odczytuje go git rev-parse HEAD.

Nowy run.json: application=WHISPERX_GUI i application_version=1.1.1. Jedno źródło obu wartości: APPLICATION_ID/APPLICATION_VERSION w istniejącym src/configuration.py. Kontroler używa stałych przy tworzeniu manifestu; dalszy worker zachowuje te pola. Schema_version=1, pozostałe pola i kontrakt eksportów bez zmian. Historyczne wyniki z identyfikatorem WHISPERX_GUI D2.1 i bez application_version nie są poprawiane ani migrowane.

Regresja: **24/24 PASS (6,717 s)**, prawdziwe eksporty TXT/SRT/JSON i blokady sieci/zapisu PASS, AST PASS. Potwierdzono poprawną tożsamość i wersję w 15 nowych manifestach oraz brak zmiany SHA-256 wszystkich 134 wcześniejszych run.json. Nie zmieniono profili (sesja=preserve, webinar=legacy), ASR, przygotowania audio, transcript.json, writerów, offline, anulowania, Job Object, zależności i środowiska. Testy tworzą wyłącznie nowe katalogi. Bez transkrypcji i ładowania modeli; wcześniejsze dowody AUDIO-01/ASR z v1.1.0 pozostają historyczne.

[Semantyka metadanych](DATA.md), [decyzje D-55–D-58](DECISIONS.md), [testy](../tests/README.md), [bieżący handoff](../99_HANDOFF/CURRENT/HANDOFF.md). Lokalne dowody: runs/patch_1_1_1_00312c231de54295b715b44ebfe0d963. Gotowość poprawki jest rekomendacją Work, odbiór należy do użytkownika i głównej rozmowy. Nie otwarto dalszego rozwoju ani publikacji.
