# Bieżący stan — 18.10.2026, wydanie v1.1.1

**v1.1.1 — RELEASE AND PUBLICATION AUTHORIZED**

Użytkownik odebrał poprawkę provenance b8a0ef5d5fd5fe7f4591b10b64631d7cd521acfc i zatwierdził finalizację/publikację. Zastano czysty branch codex/provenance-1-1-1; lokalny main i zdalny main zgodne z opublikowanym v1.1.0 (fc5e2c76966c4219c50c0955ff3898c064614613). Nie było tagu v1.1.1. Poprawkę zintegrowano z main przez fast-forward; bez nowych zmian funkcjonalnych.

Nowe run.json zawierają application=WHISPERX_GUI, application_version=1.1.1 z jednego źródła w src/configuration.py. Schema 1, request i transcript.json/TXT/SRT oraz pozostałe provenance bez zmian. Historyczne manifesty bez migracji. Profile bez zmian: WEBINAR_RUI_PL legacy, sesja_rady_gminy preserve; brak pola nadal legacy.

Końcowa regresja po integracji: **24/24 PASS (7,366 s)**, prawdziwe writery i blokady sieci/zapisu PASS. Potwierdzono wersję nowych manifestów i hashe wszystkich 149 zastanych run.json bez zmian. Przyjęto wcześniejsze dowody odbioru poprawki; bez nowego ASR, pełnej transkrypcji, instalacji lub zmian referencyjnego WhisperX. Checkpoint wydania aktualizuje tylko dokumentację, src/config/tests identyczne z odebranym b8a0ef5.

Publikacja autoryzowana: repozytorium https://github.com/tyszkiewiczpawel0-debug/WhisperX_GUI, zwykły push main i tagu v1.1.1 wskazującego finalny checkpoint main. Tag mvp-v1.0 nadal a677fc6f62620752156fd2565edac6e3585090e0; v1.1.0 nadal fc5e2c76966c4219c50c0955ff3898c064614613. Pełne końcowe lokalne/zdalne SHA, wynik push i czystość working tree są potwierdzane po operacjach w przekazaniu i runs/release_1_1_1_a27c2caf26d14d78a01f8a9d5cbef213/release_refs.json. Pozwala to identyfikować commit zawierający również ten dokument bez samoodwołania do własnego SHA. Oczekiwany status po potwierdzeniu: **v1.1.1 PUBLISHED — PENDING FINAL VERIFICATION**.

Zachowane ograniczenia: brak nowego rzeczywistego ASR w tej finalizacji; pełny preserve 98 min, całościowy odsłuch/jakość, drugie stanowisko i alternatywne compute nie uzyskują nowego PASS. Wcześniejszy pełny przebieg użytkownika był legacy, a dowody preserve dotyczą pięciu zdarzeń i krótkiego ASR. Bez rozszerzania kontraktu lub dalszego etapu.

[Handoff](../99_HANDOFF/CURRENT/HANDOFF.md), [decyzje D-59–D-62](DECISIONS.md), [DATA](DATA.md), [testy](../tests/README.md). Uruchomienie Start.cmd bez zmian. Odbiorcy: użytkownik i główna rozmowa ChatGPT projektu; Work publikuje i dostarcza dowody, ale nie zatwierdza własnego rezultatu.
