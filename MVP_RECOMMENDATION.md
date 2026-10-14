# WHISPERX_GUI — D0: rekomendacja MVP

Data: 14.10.2026. **Propozycja do oceny użytkownika; nie zatwierdza architektury ani przejścia do D1.** Podstawa: PROJECT_CONTRACT.md v1.0 APPROVED oraz ustalenia DISCOVERY_REPORT.md i REUSE_MATRIX.md.

## 1. Rekomendowany wariant

**Python + Tkinter → kontroler pojedynczego zadania → FFprobe/FFmpeg → adapter Python API WhisperX w osobnym procesie → biblioteczne eksportery i metadane.**

Tkinter jest dostępny w istniejącym interpreterze (import potwierdzony). Brak ustaleń uzasadniających nowy framework GUI. Interfejs i proces roboczy mogą korzystać z `C:\AI\WhisperX\.venv\Scripts\python.exe`; kod aplikacji pozostaje w odrębnym katalogu GUI. Ścieżki interpretera, narzędzi, cache i wyników należy trzymać w konfiguracji lokalnej. Nie tworzyć drugiego venv ani kopii modeli.

Adapter w nowym projekcie powinien przejąć sekwencję API ze `transcribe_trip_meeting.py` i opisać jej pochodzenie. Nie uruchamiać tego skryptu bezpośrednio: ma zakodowany plik wejściowy, nadpisuje wspólne wyniki i nie obsługuje parametrów. Nie importować go: kod wykonuje się na poziomie modułu.

CLI WhisperX istnieje i obsługuje parametry modelu, batch, alignmentu i cache-only, ale format `all` generuje dodatkowe formaty, a nazwy wyników zależą od wejścia. CLI nadal wymaga kontrolera, przygotowania audio i run.json. Python API daje kontrolę nad fazami, lokalnymi zasobami i eksportem przy małym adapterze. Nie ma potrzeby zmieniania zainstalowanego WhisperX.

## 2. Profil WEBINAR_RUI_PL

Nazwa: **Webinar — Rejestr Urbanistyczny PL**. Jeden profil w pliku konfiguracyjnym, poza logiką GUI. Parametry pojedynczego uruchomienia mogą być zmieniane w zakresie udostępnionym przez interfejs; zapisywać wartości rzeczywiście zastosowane.

| Parametr | Rekomendacja | Podstawa i ograniczenie |
|---|---|---|
| Model | large-v3 | Używa go skrypt; lokalny cache Systran/faster-whisper-large-v3 istnieje. Nie wykonano benchmarku jakości RUI |
| Język | pl | Skrypt i istniejące wyniki mają pl; model alignmentu dla PL jest dostępny |
| Urządzenie | cuda | RTX 5070 Ti, 16303 MiB VRAM i torch cu128. Działanie obliczeń CUDA/CTranslate2 nie było testowane |
| Compute type | float16 | Taki parametr stosuje skrypt. Dotyczy ASR CTranslate2; nie obiecuje float16 dla całego alignmentu/VAD |
| Batch size | 8, jako wartość startowa | Zgodny ze skryptem i domyślnym CLI; niepotwierdzony dla webinaru. Po błędzie OOM zaproponować mniejszy batch i nowe zadanie; bez cichej zmiany parametrów |
| Alignment | włączony | Wymagany do lepszych znaczników; użyć jonatasgrosman/wav2vec2-large-xlsr-53-polish, dostępnego lokalnie |
| Diarizacja | wyłączona | Zgodnie z kontraktem i istniejącym skryptem |
| VAD | zachować pyannote | Obecny domyślny mechanizm; lokalne wagi w assets. VAD nie jest diarizacją |

Parametry mają podstawę w istniejącym rozwiązaniu, lecz **nie są wykonawczo zatwierdzonym profilem webinaru**. Wspólne zastosowanie large-v3/CUDA/float16/batch 8/alignment wymaga późniejszego testu. Nie wprowadzać automatycznego fallbacku CPU lub innego modelu bez odnotowania i decyzji użytkownika.

Przed uruchomieniem sprawdzić lokalne modele, VAD oraz NLTK Punkt PL. Dla ASR użyć `local_files_only=True`, dla polskiego alignmentu `model_cache_only=True`; skonfigurować offline HF dla procesu i wskazać lokalny NLTK_DATA. Brak/nieczytelność zasobu ma zakończyć preflight informacją, a nie pobraniem. Sam offline HF nie blokuje `nltk.download` w alignment.py, dlatego konieczna jest weryfikacja Punkt przed silnikiem. Kompletne działanie bez sieci pozostaje testem akceptacyjnym; D0 nie zatwierdza pobrań.

## 3. Przygotowanie i zachowanie czasu

FFprobe odczytuje kontener, strumienie, kodek, częstotliwość, kanały, start i długość. Przy braku ścieżki audio zadanie nie startuje; przy wielu ścieżkach wybór ma być jawny. Dla MVP przygotować PCM s16le 16 kHz mono w podkatalogu zadania, korzystając z istniejącego FFmpeg i parametrów dekodowania zgodnych z `load_audio`. Nie stosować skracania, usuwania ciszy ani zmiany szybkości. Oryginał otwierać wyłącznie do odczytu. Nie rekonstruować nieznanego polecenia użytego do starego WAV.

Ponownie odczytać długość WAV i porównać z wybraną ścieżką oraz czasem kontenera. Propozycja progu ostrzeżenia: bezwzględna różnica >0.1 s; to decyzja projektowa, nie wynik testu. Zachować wartości i różnicę w run.json. Brak wiarygodnej długości lub nietypowy niezerowy offset wymaga czytelnej informacji przed przetwarzaniem; nie uznawać zgodności długości za dowód synchronizacji. Ustalić referencję napisów względem nagrania źródłowego, zwłaszcza przy wideo i opóźnionej ścieżce audio; taki przypadek wymaga testu, a w razie braku obsługi — jawnego odrzucenia w MVP.

`load_audio` może wczytać przygotowany WAV bez ponownego budowania dekodera. Całość audio pozostaje w RAM, a model ASR i alignment powinny być ładowane kolejno, ze zwalnianiem jak w istniejącym skrypcie. Długie webinary wymagają późniejszego sprawdzenia RAM i VRAM.

## 4. Kontroler, logi i przerwanie

Jedno aktywne zadanie. GUI pozostaje w głównym wątku Tkinter; odczyt stdout/stderr działa poza nim, a aktualizacje przez kolejkę i `after()`. Proces roboczy uruchamiać bez widocznego dodatkowego okna i z niebuforowanym wyjściem. GUI nie wykonuje długiego FFprobe, konwersji ani importów silnika w obsłudze przycisku.

Minimalne stany: walidacja, przygotowanie, ASR, alignment, eksport, zakończone / błąd / anulowane. Istniejące logi i callbacki można przejąć, lecz procenty ASR/alignmentu nie określają czasu całego zadania. MVP może pokazywać etap i log bez procentu globalnego.

Anulowanie: sygnał kooperatywny między etapami oraz ograniczony czas oczekiwania; gdy biblioteka nie reaguje, zakończyć wyłącznie własny proces roboczy i jego procesy potomne (w tym FFmpeg), identyfikowane po uchwycie/PID zadania. Samo zatrzymanie wątku lub samego Pythona nie zapewnia usunięcia FFmpeg. Mechanizm drzewa procesów Windows wymaga testu; nie kończyć procesów po nazwie globalnie. Po zakończeniu zapisać stan anulowany, kod wyjścia i etap; częściowe pliki nie są sukcesem. Kontroler powinien umieć dopisać stan końcowy nawet po wymuszonym zakończeniu workera.

`process.log` obejmuje stdout, stderr, etapy, ostrzeżenia i wyjątki, bez tokenów/sekretów. `finally` zwalnia modele w normalnym przebiegu, a izolacja procesu ogranicza skutki awarii i zwalnia zasoby przy zakończeniu. Wznowienie od RAW, kolejka zadań i automatyczne ponawianie są poza MVP.

## 5. Wyniki i minimalne metadane

Propozycja struktury: `<lokalny katalog wyników>/<data-czas>_<krótki UUID>/`. Tworzenie ma być wyłączne, z wykryciem kolizji. Każde ponowienie otrzymuje nowy katalog, także dla tego samego wejścia. Materiał pośredni w `work/` tego zadania; nie w INPUT ani istniejącym OUTPUT źródła.

W udanym zadaniu wymagane są dokładnie wskazane przez kontrakt wyniki użytkowe: `transcript.txt`, `transcript.srt`, `transcript.json`, `run.json`, `process.log`. Do pierwszych trzech użyć istniejących WriteTXT/WriteSRT/WriteJSON lub get_writer dla każdego formatu osobno, z bazą nazwy `transcript` i pełnymi opcjami writerów (`max_line_width`, `max_line_count`, `highlight_words`). TXT może być zwykłym tekstem; nie ma potrzeby zachowywania starego formatu TXT z czasami. Nie używać wadliwego srt_ts ze skryptu.

Eksportować do obszaru tymczasowego nowego zadania, sprawdzić JSON, zakresy czasu i obecność trzech plików, następnie przenieść do nazw końcowych. Nie deklarować atomowości całego zestawu: stan `succeeded` w run.json zapisać dopiero po walidacji kompletu. Przy błędzie/anulowaniu zachować log i metadane, a pliki częściowe wyraźnie oddzielić. RAW nie jest wymaganym szóstym wynikiem MVP; nie budować na nim wznawiania.

Minimalny run.json: wersja schematu, id i stan zadania, początek/koniec i czas trwania, etap błędu/anulowania, wejście (ścieżka, rozmiar, mtime, wybrany strumień i metadane FFprobe), parametry profilu i rzeczywiście użyte wartości, identyfikatory modeli i dostępne rewizje cache, wersje Python/WhisperX/PyTorch/CTranslate2/faster-whisper/FFmpeg/FFprobe i istotnych zależności alignmentu, GPU/sterownik, właściwości WAV i różnica długości, ścieżki wyników i ostrzeżenia. Nie kopiować tokenów ani całego środowiska systemowego do manifestu.

Proponowana polityka pośrednich: po sukcesie usuwać wyłącznie własny WAV zadania; po błędzie zachować do świadomego sprzątnięcia. Ta polityka wymaga zatwierdzenia; nigdy nie obejmuje oryginałów, istniejącego OUTPUT ani cache modeli.

## 6. Minimalny nowy zakres i granice

BUILD: formularz GUI, jeden profil i lokalna konfiguracja, kontroler procesu/anulowania, preflight i cienka obsługa przygotowania audio, unikatowe katalogi, manifest i trwały log oraz kontrola kompletności. ADAPT: sekwencja istniejącego skryptu, statusy i zwalnianie modeli. REUSE: Python/Tkinter, FFmpeg/FFprobe, WhisperX i jego modele/VAD/alignment/writery.

Podział jest logiczny; nie wymaga rozbudowanego frameworka, systemu pluginów ani osobnych usług. Brak podstaw do wiarygodnego określenia liczby linii lub czasu implementacji przed zatwierdzeniem detali. Inicjalizacja Git, README, wzór konfiguracji i struktura plików aplikacji należą do D1; implementacja MVP do kolejnego zatwierdzonego etapu. W D0 nie utworzono żadnego z tych elementów.

Poza zakresem: diarizacja, wiele profili, przetwarzanie wsadowe, automatyczne streszczanie, analiza treści/prawna webinaru, integracje z innymi projektami i wznowienia z checkpointów.

## 7. Decyzje przed D1 i handoff

Użytkownik powinien ocenić D0 i zatwierdzić: (1) wariant Tkinter + osobny proces + adapter API ze współdzielonym venv; (2) startowy profil z batch 8 jako parametrem wymagającym testu; (3) lokalizację wyników, politykę pośrednich i próg różnicy długości; (4) późniejszy zakres testów offline/GPU/anulowania oraz pilotażu RUI. Zgoda na D1 nie oznacza zgody na instalacje, pobieranie modeli ani rozpoczęcie pełnej transkrypcji w tym zadaniu.

**Handoff za pośrednictwem użytkownika:** D0 COMPLETE w zakresie rozpoznania i trzech dokumentów, oczekuje oceny. Dokumenty: `C:\AI\WhisperX_GUI\DISCOVERY_REPORT.md`, `C:\AI\WhisperX_GUI\REUSE_MATRIX.md`, `C:\AI\WhisperX_GUI\MVP_RECOMMENDATION.md`.

Potwierdzone: Python 3.11.9, WhisperX 3.8.6, PyTorch cu128, RTX 5070 Ti, obecność lokalnych modeli, import Tkinter, dotychczasowy pipeline API i istniejące wyniki; M4A/WAV różnią się o 15.042 ms. Źródło i GUI nie mają Git. Błąd srt_ts potwierdzono izolowanym testem. Do ponownego użycia nadaje się zasadniczy stos, a do adaptacji skrypt; nowy kod jest potrzebny głównie do obsługi użytkownika i bezpiecznego zadania.

Nieweryfikowane: obecna zdolność wykonania ASR/alignmentu na GPU i offline, zapotrzebowanie VRAM batch 8, jakość/synchronizacja webinaru RUI, kompletna obsługa wideo i anulowania. Istniejące artefakty nie zastępują pilotażu. Brak modyfikacji źródła i środowiska; brak implementacji, instalacji, pobrań i pełnej transkrypcji. **D1 nie rozpoczęto.**
