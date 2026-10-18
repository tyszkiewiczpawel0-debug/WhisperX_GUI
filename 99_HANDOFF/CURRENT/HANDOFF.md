# WHISPERX_GUI — finalizacja i publikacja v1.1.1

Data: 18.10.2026. Odbiorcy: **użytkownik i główna rozmowa ChatGPT projektu WhisperX_GUI**.

Poprawka odebrana przez użytkownika; **RELEASE AND PUBLICATION AUTHORIZED**. Status końcowy po potwierdzeniu push i referencji: **v1.1.1 PUBLISHED — PENDING FINAL VERIFICATION**.

## Integracja i zakres

Wejście: czysty codex/provenance-1-1-1, b8a0ef5d5fd5fe7f4591b10b64631d7cd521acfc; main=origin/main=zdalny main=v1.1.0 na fc5e2c76966c4219c50c0955ff3898c064614613. Brak lokalnego/zdalnego v1.1.1. Main przesunięto fast-forward do odebranej poprawki. Po nim wyłącznie minimalny dokumentacyjny checkpoint wydania.

Nowy manifest: application=WHISPERX_GUI, application_version=1.1.1; jedyne źródło APPLICATION_ID/APPLICATION_VERSION w configuration.py. Reszta schema 1/provenance/request i eksportów bez zmian; brak migracji wyników. Profile pozostają webinar=legacy i sesja=preserve. Bez nowych zmian kodu, konfiguracji, testów, środowiska, zależności lub zakresu funkcji. Poprzedni lokalny kandydat i jego dowody zostały formalnie odebrane przez użytkownika.

## Weryfikacja

- **PASS:** po integracji 24/24 unittest, 7,366 s; realny worker inspect/prepare, nowe pola/wersja, oba profile, request/run, błędy/anulowanie, Job Object i dotychczasowa regresja. ASR w testach jednostkowych jest atrapą.
- **PASS:** prawdziwe eksporty TXT/SRT/JSON, znaczniki czasu/słowa, blokady sieci i zapisu; nowe manifesty identyfikują WHISPERX_GUI/1.1.1. 149 zastanych run.json bez zmiany SHA-256. Poprzednie 134 niezmienione manifesty i 24/24 PASS pozostają historycznym dowodem odbioru, nie zastępują opisanej końcowej kontroli main.
- **FAIL:** brak w zakończonych testach. Integralność publikacji wymaga zgodności lokalnego main, origin/main, zdalnego main i commita tagu; zwykły push bez force, bez nadpisywania kolidujących tagów/historii.
- **NOT TESTED:** nowy rzeczywisty ASR i pełna transkrypcja (celowo nieponawiane), pełny preserve 98 min, pełny odsłuch/jakość, inne stanowisko/compute. Poprzedni pełny test użytkownika używał legacy; wcześniejsze preserve było sprawdzone na pięciu zdarzeniach i krótkim ASR.

## Git, publikacja i odtworzenie

Repozytorium: https://github.com/tyszkiewiczpawel0-debug/WhisperX_GUI. Publikowane wyłącznie main i v1.1.1 wskazujące ten sam finalny commit. Mvp-v1.0 i v1.1.0 zachowane, bez force. Nie publikować INPUT/runs/transkrypcji/modeli/cache/local.toml. Cały osiągalny zakres publikacji jest kontrolowany przed push; working tree weryfikowany po operacjach.

Dokładny pełny SHA main i commita tagu, obiekt tagu oraz wynik porównania ze zdalnym stanem: końcowe przekazanie i runs/release_1_1_1_a27c2caf26d14d78a01f8a9d5cbef213/release_refs.json. Po wykonaniu procedury odtworzenie przez git rev-parse main i git rev-parse 'v1.1.1^{commit}'; oba mają być zgodne z git ls-remote origin dla main i rozwiązanego tagu. URL commita ma postać adresu repozytorium + /commit/<pełny SHA>, tagu + /tree/v1.1.1. Końcowe przekazanie zawiera gotowe linki i wynik publikacji; nie zastępować go samym komunikatem utworzenia lokalnego tagu.

[Stan](../../docs/CURRENT_STATE.md), [decyzje D-59–D-62](../../docs/DECISIONS.md), [metadane](../../docs/DATA.md), [testy](../../tests/README.md). Dowody finalizacji i logi pozostają tylko w podanym ignorowanym katalogu runs. Start.cmd bez zmian; do oceny wersji użyć nowego zadania, nie historycznego wyniku. Work nie zatwierdza własnego rezultatu i nie rozpoczyna kolejnej wersji.
