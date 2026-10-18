# Minimalny plan kolejnej wersji — 18.10.2026

**ANALYSIS COMPLETE — IMPLEMENTATION PENDING APPROVAL**

Plan do zatwierdzenia przez użytkownika i rozmowę ChatGPT prowadzącą projekt. Podstawa i uzasadnienie: [analiza](NEXT_VERSION_ANALYSIS.md). Nie jest autoryzacją implementacji ani rozszerzeniem kontraktu zamkniętego MVP.

## 1. Zakres i kolejność po zatwierdzeniu

1. Uzgodnić zakres następnej wersji, reprezentację wyboru przygotowania i addytywnych metadanych, semantykę alignmentu sesji oraz źródło/test odbioru osi czasu. Zachować tag `mvp-v1.0`; pracować na nowej gałęzi `codex/…`, bez publikacji wynikającej z tego planu.
2. `src/configuration.py`: mały jawny rejestr dwóch ID → pliki; parametryzacja `profile()` z domyślnym webinarem; walidacja ID, zgodności pliku i przyszłej opcji przygotowania. Bez znoszenia pozostałych ograniczeń. Dodać wyłącznie `config/sesja_rady_gminy.json` z wartościami z analizy i zatwierdzoną deklaracją przygotowania; stary JSON bajtowo bez zmian. Bez migracji local.toml.
3. `src/gui.py`: readonly wybór profilu i pełne przeładowanie formularza, reset nadpisań przy zmianie profilu, domyślnie webinar; blokada wyboru podczas pracy, przywrócenie po sukcesie/błędzie/anulowaniu. Wszystkie zmiany parametrów nadal dotyczą tylko uruchomienia.
4. `src/controller.py`, `src/worker.py`: przenieść zwalidowany, rozstrzygnięty wybór przygotowania w snapshot parametrów request/run; przekazać go do media. Pozostawić jeden worker, kolejkę, handshake GO po przypisaniu Job Object i obsługę końcowych stanów. Nie wczytywać ponownie profilu w workerze.
5. `src/media.py`: jedna implementacja i dwie gałęzie listy argumentów — stara identyczna dla webinaru/braku opcji, nowa z `-af aresample=16000:async=1:first_pts=0`. Zachować ochronę oryginału, mapowanie, `-n`, PCM/16 kHz/mono, kontrolę offsetów i błędów. Dla nowej gałęzi porównać długości oddzielnie z audio i kontenerem, zachować stare znaczenie istniejącej delty; zapisać faktyczne polecenie i referencję czasu. Bez automatycznej zmiany trybu, przesunięć napisów i dopełnienia do długości filmu.
6. Rozszerzyć istniejące `tests/test_mvp.py` i `tests/test_prompt.py`, wykorzystać obecne skrypty eksportów i kontroli. Dopiero po odpowiedniej zgodzie krótki rzeczywisty przebieg offline i anulowanie silnika. Uaktualnić README, ARCHITECTURE/DATA, tests/README, CURRENT_STATE, DECISIONS i jeden handoff; bez przebudowy infrastruktury.

Bez planowanych zmian `engine.py`, `artifacts.py`, `safety.py`, `winjob.py`, launcherów i środowiska, chyba że konkretny test wykaże błąd w zatwierdzonym zakresie. Każde takie odstępstwo najpierw ocenić wobec ograniczeń projektu.

## 2. Minimalna macierz testów i odbioru

| Kryterium | Minimalne sprawdzenie / oczekiwany dowód |
|---|---|
| PROFILE-01/03 | Oba ID i nazwy w rzeczywistym Tkinter; domyślnie webinar. Sesja large-v3/pl/cuda/float16/8/alignment=true/diarization=false, pusty prompt; po walidacji prompt=null. Odrzucenie nieznanego ID, rozbieżnego ID pliku, złej wersji, niepoprawnych wartości i nieznanej jawnej opcji przygotowania. |
| PROFILE-02, REGRESSION-01 | `profile()` nadal webinar; jego JSON ma ten sam hash co tag. Dokładna lista argumentów starego FFmpeg, opcje ASR i normalizacja promptu zgodne z tagiem; stare requesty bez nowej opcji wybierają stare przygotowanie. Dotychczasowe 16 testów PASS. |
| PROFILE-04 | A → edycja wszystkich dostępnych pól/promptu → B → A: pełny reset według profilu, brak wycieku parametrów. Hashe obu JSON przed/po identyczne. Zapisany request nie zmienia się po dalszej zmianie obiektu/formularza. W trakcie pracy wybór zablokowany, po zakończeniu ponownie dostępny. |
| PROFILE-05, AUDIO-02 | Dla obu profili kontroler i rzeczywisty worker prepare; dla transcribe atrapa adaptera. `request.parameters.id == run.parameters.id`, faktyczne argumenty workera/adaptera zgodne z zapisanymi parametrami. Wybrana opcja vs faktyczne polecenie; błąd przed prepare, podczas FFmpeg, podczas ASR i anulowanie nie potwierdzają niewykonanej operacji. Zachować trzy stany promptu oraz dokładny tekst/null. |
| AUDIO — konstrukcja | Atrapa command: jedyna zamierzona różnica to filtr, zawsze -n/map/16k/mono/PCM i nowy katalog. Zwykły WAV oraz syntetyczny materiał z kontrolowanym zaburzeniem timestampów: zmierzyć oczekiwane pozycje sygnałów po obu wariantach, nie tylko długość. Wywołania FFmpeg w istniejącym unittest, bez nowego frameworka. |
| AUDIO-01 — rzeczywiste źródło | Wskazany problematyczny MP4 XXV lub równoważny z udokumentowanym skróceniem zwykłego WAV. Dwa przygotowania w nowych katalogach; hashe oryginału przed/po. FFprobe obu WAV i źródła, długości strumienia/kontenera, starty; w razie potrzeby odczyt PTS pakietów. Punkty referencyjne na początku/środku/końcu i po rozbieżnościach porównać z master. Sam syntetyczny plik lub zgodna długość nie zastępuje tej bramki. |
| AUDIO — granice | Brak audio, wiele ścieżek, offset >0,1 s, mały offset, brak długości strumienia, brak obu długości, odrzucenie niepoprawnego WAV, duża różnica długości. Brak danych daje jawny brak możliwości porównania, nie PASS synchronizacji. Nie rozszerzać przy okazji ogólnej obsługi uszkodzonych mediów. |
| OUTPUT-01/02 | Rozszerzyć `check_exports.py` na stałym wyniku (PL, segmenty, słowa z czasami i bez nich): dokładna zgodność TXT/SRT/JSON przed/po zmianie dla tego samego obiektu, granice minut/godzin, walidacja zakresu względem WAV i komplet pięciu plików. Oddzielnie sprawdzić provenance request/run; nie żądać identycznego tekstu dwóch losowych przebiegów ASR. |
| Offline i ochrona | Obecny `check_exports.py`: blokada sieci i zapisu poza zadaniem. Testy niekompletnych lokalnych zasobów bez pobierania. Dla obu profili konfiguracja środowiska workera i opcje adaptera bez zmian; późniejszy krótki rzeczywisty test sprawdza, że nadal działają z aktywnymi blokadami. Nic nie zapisuje do referencyjnego WhisperX. |
| Worker, anulowanie, Job Object | Obecne testy przygotowania/błędów/powtórzenia/GUI i zabicia potomnego FFmpeg z zachowaniem niezależnego procesu. Dodać przerwanie podczas nowego przygotowania (z kontrolowaną synchronizacją testu) i zachowanie pośrednich/status cancelled. Po autoryzacji krótki `check_cancellation.py` dla ASR/alignmentu, parametryzowany profilem zamiast mnożenia skryptów. |
| Rzeczywisty przebieg / GUI | Po osobnej zgodzie krótka próbka PL dla obu profili przez obecny pipeline, sprawdzenie request/run, eksportów, synchronizacji i niezmienności źródła; bez pełnej transkrypcji sesji. Osobno widoczny GUI: wybór, zmiana parametrów, start, responsywność i anulowanie. Test prepare nie jest dowodem responsywności podczas ASR. |

Syntetyczny przypadek może zawierać celową przerwę PTS i weryfikować mechanizm filtra, ale nie potwierdza zgłoszonej przyczyny AAC w XXV. Jeśli nie odtwarza skrócenia, nie oznaczać go jako test regresji XXV. Dopiero dostęp do wskazanego materiału pozwoli zamknąć AUDIO-01. Nie dodawać nagrań ani wyników do Git; testowe dane tworzyć w nowych ignorowanych katalogach runs.

## 3. Kryteria odbioru i ryzyka

Gotowość do odbioru wymaga spełnienia PROFILE-01…05, AUDIO-01…02, OUTPUT-01…02 i REGRESSION-01 z handoffu, udokumentowanych wyników macierzy oraz braku regresji offline/anulowania/Job Object. Parametry sesji są baseline, nie zadaniem optymalizacji. Nie gwarantować czasów każdego słowa ani jakości nazw własnych.

Proponowany cel synchronizacji to błąd wybranych zdarzeń najwyżej 100 ms względem master; należy go zatwierdzić przed testem, z uwzględnieniem dokładności pomiaru. Różnica długości 112 ms z relacji XXV nie spełnia automatycznie takiego celu ani go sama nie obala: trzeba zlokalizować różnicę i porównać zdarzenia. Nie zwiększać progu ostrzegania, nie przycinać wyników ani nie dopisywać ciszy dla uzyskania PASS.

Główne ryzyka i zabezpieczenia: przypadkowa zmiana webinaru → identyczny JSON i polecenie; wyciek stanu GUI → test A/B/A i snapshot; mylna referencja czasu → osobne długości i punkty kontrolne; niewykonane przygotowanie → rozdzielenie wyboru i wykonania; szerszy refaktor → ograniczenie do wskazanych funkcji. Brak materiału lub dowodów referencji czasu blokuje odbiór AUDIO-01, a potrzeba instalacji/pobrania, modyfikacji źródła lub destrukcji zatrzymuje zależną pracę.

DoD implementacji nie oznacza własnego odbioru Work. Użytkownik i główna rozmowa zatwierdzają wynik i ewentualny kolejny etap. Historyczne trzy PARTIAL D4 pozostają oddzielnymi ograniczeniami zamkniętego MVP.

## 4. Bieżący checkpoint analizy

Obecnie wykonano tylko analizę i dokumenty; istniejące 16 testów, eksporty/blokady i AST/config PASS, szczegóły w analizie. Nie dodano profilu, pola `audio_timeline_mode`, filtra ani testów nowej funkcjonalności. Najbliższy krok to decyzja o powyższej rekomendacji i autoryzacji zakresu; aktualny [handoff](99_HANDOFF/CURRENT/HANDOFF.md) zawiera stan do kontynuacji.
