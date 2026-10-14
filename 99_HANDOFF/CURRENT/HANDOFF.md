# WHISPERX_GUI — checkpoint D1

Data: 14.10.2026. Odbiorca: główna rozmowa ChatGPT WHISPERX_GUI za pośrednictwem użytkownika.

**D1: COMPLETE w zakresie wykonawczym, do formalnego odbioru użytkownika. D0 zatwierdzony 14.10.2026. D2 nie rozpoczęto.**

## Repozytorium i źródła prawdy

Lokalizacja: `C:\AI\WhisperX_GUI`; branch `main`; brak remote/push. Commit inicjalizacji: `558c9474b36fe2354c3604f04051d0777ba7a7b5`. Końcowy commit checkpointu wskazuje `HEAD` na main po zakończeniu D1; pełne SHA jest przekazane w końcowym handoffie w rozmowie i dostępne przez `git rev-parse HEAD`. Wpisywanie SHA commita w jego własnej treści zmieniłoby to SHA. Po późniejszych zmianach commit D1 można odnaleźć przez `git log --all --grep="Record D1 verification and handoff"`.

Obowiązują: [kontrakt](../../docs/PROJECT_CONTRACT.md), [standard pomocniczy](../../PROJECT_STANDARD_v0.2.md), [AGENTS](../../AGENTS.md), [stan](../../docs/CURRENT_STATE.md), [architektura](../../docs/ARCHITECTURE.md), [dane](../../docs/DATA.md), [decyzje](../../docs/DECISIONS.md). Raporty D0 pozostają w root; ich historyczny status zastępuje informacja o zatwierdzeniu w CURRENT_STATE. Jedyna obowiązująca kopia kontraktu jest w docs, bez zmiany treści i wersji.

Struktura: README.md, AGENTS.md, .gitignore; docs z pięcioma wymaganymi dokumentami i snapshotem pakietów; config z local.example.toml i jednym WEBINAR_RUI_PL.json; src/README.md i tests/README.md opisujące przyszły kod/testy; trzy raporty D0 i standard w root; jeden bieżący plik handoffu.

## Ustalenia i granice

Reuse istniejącego Pythona 3.11.9, WhisperX 3.8.6, torch 2.8.0+cu128, FFmpeg 8.1.2, lokalnych modeli oraz bibliotecznych mechanizmów. GPU rozpoznane w D0: RTX 5070 Ti. Zatwierdzono wyniki discovery i autoryzowano D1; rekomendowana architektura Tkinter → kontroler → przygotowanie → adapter API w osobnym procesie → eksport nie jest zaimplementowana. Profil ma startowe large-v3/pl/cuda/float16/batch 8/alignment=true/diarization=false.

Konfiguracja stanowiska: wzór TOML, przyszła lokalna kopia config/local.toml jest ignorowana. Brak loadera, entry pointu aplikacji, instalacji i drugiego venv. README opisuje obecne stanowisko i uczciwie ograniczoną procedurę odtworzenia na nowym komputerze. Snapshot pakietów nie zapewnia wheel/indeksów/hashy ani model cache.

Nieweryfikowane: pełne CUDA/CTranslate2 i offline, batch 8/VRAM, jakość i synchronizacja RUI, anulowanie drzewa procesów. Ryzyka D0: pobranie Punkt przez NLTK, błędne przeniesienie sekund w źródłowym srt_ts, nadpisywanie starych wyników przez skrypt. Nie importować skryptu źródłowego i nie traktować istniejących artefaktów jako testu nowej aplikacji.

## Kontrole i zakres zmian

PASS: składnia TOML/JSON, wartości i typy profilu, 19 reprezentatywnych ścieżek ignorowanych oraz 7 dozwolonych, wszystkie lokalne linki Markdown, pojedynczy kontrakt i hashe kontraktu/standardu także w pierwszym commicie. Przejrzano zakres staged diff: 18 plików tekstowych inicjalizacji, każdy poniżej 100 KB, bez danych wykonawczych; dodatkowy skan sygnatur kluczy/tokenów niczego nie wykrył. Checkpoint jest dziewiętnastym plikiem. Brak testów silnika.

Kontrola whitespace nowych dokumentów/konfiguracji przeszła. Pełna kontrola importowanych dokumentów wskazała 7 istniejących końcówek z dwiema spacjami Markdown w kontrakcie i standardzie; zachowano je celowo, aby nie zmieniać dostarczonej treści. `.gitattributes` wyłącza konwersję końców linii wyłącznie tych dwóch dokumentów. Powtórzony snapshot metadanych 46565 plików źródła ma identyczny hash jak przed pracą. Końcowy Git/main/remote/status jest sprawdzany po commicie checkpointu i przekazywany w rozmowie.

Bez zmian źródłowego WhisperX, venv, modeli, nagrań i wyników; wyłącznie odczyty. Referencyjny snapshot metadanych 46565 plików źródła (ścieżka, rozmiar, mtime_ns) przed D1: SHA256 `d6d182d80908b249c736ce9ad3f8494560f271cca884c5381652aa86da2fc2ad`. To kontrola metadanych, nie pełny hash zawartości środowiska. Kontrakt SHA256 `6fceb18b8e3170c78561182869c5d0ba542450eea61085b8994bf00f9594859c`; standard `b004ed052a224e3be2d3b4ec379cbfca819fc933b9e79b729c79cfc31cf30e1c`.

## Odstępstwa i start D2

Brak odstępstw od wymaganej minimalnej dokumentacji. Równoważny TOML zamiast .env jest dopuszczony zleceniem. Standardowy model snapshotów danych zastosowano proporcjonalnie: bez kopiowania dużych nagrań podczas inicjalizacji; pochodzenie wyników ma zapewnić run.json w D2. Raporty D0 pozostawiono historyczne, bez przepisywania ich treści.

Przed D2: odbiór D1 i autoryzacja implementacji przez użytkownika; potwierdzenie wariantu integracji oraz lokalizacji wyników, retencji pośrednich, progu długości i zakresu testów wykonawczych. Propozycja kolejności D2: walidacja konfiguracji/zasobów i bezpieczny katalog zadania → adapter/pipeline z logami → kontroler/anulowanie → GUI → uzgodnione testy. Stosować REUSE_MATRIX, nie budować silnika od nowa. Pilotaż RUI jest D3; instalacje/pobrania wymagają odrębnej zgody. Po D1 praca zostaje zatrzymana.
