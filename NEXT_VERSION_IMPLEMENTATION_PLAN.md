# Minimalny plan kolejnej wersji — 18.10.2026

**IMPLEMENTATION COMPLETE — PENDING ACCEPTANCE**

Zlecenie użytkownika IMPLEMENTATION AUTHORIZED z 18.10.2026 otworzyło wykonanie następnej wersji. Sekcje 1–4 poniżej zachowują plan sprzed zlecenia; rozstrzygające korekty i wyniki są w sekcji 5. Podstawa: [analiza](NEXT_VERSION_ANALYSIS.md). Zamknięte MVP i jego kontrakt pozostają punktem odniesienia; Work nie zatwierdza wyniku.

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

## 5. Wykonanie i wyniki — 18.10.2026

### Zakres i korekty planu

Zaimplementowano jawny rejestr dwóch profili i profile(id) z zachowaniem profile() → webinar. Nowy JSON sesji ma dokładnie parametry ze zlecenia. Webinarowy JSON pozostał bajtowo niezmieniony. GUI udostępnia wybór, resetuje wszystkie nadpisania, blokuje zmianę podczas pracy i odblokowuje po zakończeniu/błędzie/anulowaniu. Alignment sesji pozostaje edytowalny dla zadania. Bez edycji/importu/eksportu profili i bez zapisu przez GUI.

audio_timeline_mode jest opcjonalnym polem parametrów: brak → legacy, dopuszczalne tylko legacy/preserve. Oba dostarczone JSON nie mają pola, więc **oba domyślnie legacy**. To świadome odstępstwo od wcześniejszej rekomendacji preserve dla sesji: nowe zlecenie wymaga opcjonalności i sprawdzenia dostarczonego pojedynczego pliku. Nie wdrożono automatycznego wyboru na podstawie długości ani przełącznika GUI. Dla AUDIO-01 testy uzasadniają jawne użycie preserve. W GUI wymaga ono wcześniejszej ręcznej konfiguracji profilu i ponownego uruchomienia aplikacji, opisanej w README.

Kontroler zachował snapshot bez przebudowy; parameters.id i parameters.audio_timeline_mode w request/run oznaczają wybór dla zadania. Worker używa snapshotu, przekazuje tryb do media, nie odczytuje ponownie pliku profilu. Preserve dodaje jedynie filtr aresample=16000:async=1:first_pts=0. Stare polecenie legacy pozostało identyczne. Nowe addytywne pola preparation opisano w [DATA](docs/DATA.md). Domyślny próg 0,1 s, odrzucanie offsetów >0,1 s, normalizacja i potwierdzanie promptu, adapter, preflight, writery oraz safety/winjob bez zmiany logiki.

Dwa niewielkie odstępstwa wynikające z testów: media jawnie odrzuca istniejący target przed FFmpeg (-n nadal obowiązuje), aby odmowy konwersji nie można było uznać za przygotowanie starego WAV; artifacts.save ponawia tylko atomowe replace przy Windows WinError 5/32/33, maksymalnie 5 prób i łącznie 0,30 s oczekiwania. Ostatni/trwały lub inny błąd jest zgłaszany, poprzedni JSON nie jest usuwany. Rzeczywiste testy ujawniły sporadyczny WinError 5 na run.tmp → run.json; przyczyna zewnętrznej blokady nie została ustalona. Testy potwierdzają ograniczone ponowienie, brak utraty starego JSON i propagację błędów. W testach naprawiono także cykl życia obiektów Tk, który ujawnił błąd kolekcji w niewłaściwym wątku. Bez instalacji i nowej infrastruktury.

### AUDIO-01 — fakty pomiarowe

Plik INPUT/AUDIO-01.mp4 ma **5884,600 s (98:04,600)**, nie 76 min. Rozmiar 2015604191 bajtów. Jedna ścieżka H.264 (25 fps) i jedna AAC LC, 32 kHz, mono. Początki audio/kontenera/wideo 0. Ścieżka audio ma 5884,501 s, a wideo i kontener 5884,600 s.

| Przygotowanie | WAV | WAV minus audio | WAV minus kontener |
|---|---:|---:|---:|
| Dotychczasowe legacy | 5884,096 s | −0,405 s | −0,504 s |
| Jawne preserve | 5884,501 s | 0,000 s | −0,099 s |

FFprobe: 183878 pakietów AAC; 183875 mają duration 0,032 s, trzy mają 0,141 / 0,136 / 0,224 s przy PTS 10,208 / 1208,973 / 3308,341 s. Nie znaleziono przerw >1 ms między PTS pakietu a PTS poprzedniego + jego duration. Nadwyżki tych trzech duration sumują się do 0,405 s. To obserwacja zgodna z utratą dodatkowego czasu pakietów w legacy; nie dowodzi sposobu utworzenia pliku ani jego wcześniejszego łączenia.

Porównano **zdarzenia waveform, nie tylko długości**: niezależny seek MP4 po timestampie, wybór wyraźnego 1-sekundowego zdarzenia z 16-sekundowego okna, korelacja z pełnym WAV w zakresie ±1 s. Sprawdzone pozycje źródłowe obejmują początek słyszalnego materiału, pierwszą trzecią, środek, trzecią ćwiartkę i zakończenie. Początek pliku zawiera długie zerowe audio; początkowe próby na ciszy odrzucono jako niemiarodajne.

| Zdarzenie względem MP4 [s] | Legacy: WAV minus MP4 [ms] | Preserve [ms] |
|---:|---:|---:|
| 774,750 | −109 | 0 |
| 1967,000 | −213 | 0 |
| 2953,250 | −213 | 0 |
| 4417,750 | −405 | 0 |
| 5881,000 | −405 | 0 |

Korelacja znormalizowana ≈1 w każdym punkcie, rozdzielczość 1 próbki przy 16 kHz (0,0625 ms); nie jest to pełny odsłuch ani dowód zgodności w każdym miejscu nagrania. WAV rzeczywistego workera preserve jest bajtowo identyczny z wariantem eksperymentalnym użytym w porównaniu zdarzeń. Pozostałe 99 ms długości odpowiada różnicy końca ścieżki audio i wideo; nie dopełniano do kontenera. **Wniosek techniczny: legacy nie zachowuje wystarczającej synchronizacji dla tego pliku, preserve jest uzasadniony i sprawdzony w tych punktach.** Nie uogólniać na każde MP4 ani wszystkie offsety/uszkodzone PTS.

### Wyniki testów i ochrona

| Sprawdzenie | Wynik / granice |
|---|---|
| Istniejące i rozszerzone unittest | **PASS 22/22**, końcowy przebieg 5,238 s; rzeczywiste Tkinter, FFmpeg, kontroler/worker, oba profile i oba tryby; ASR w testach jednostkowych jest atrapą. 32 podprzypadki orkiestracji workera. |
| Eksporty i offline | **PASS**, rzeczywiste writery, PL i granice minut/godzin, słowa z czasami i bez, round-trip JSON; blokada sieci i zapisu poza zadaniem. |
| Krótki rzeczywisty ASR sesji | **PASS**, próbka 2950–2970 s z AUDIO-01, 20 s, large-v3/pl/cuda/float16/batch8/alignment=true/diarization=false, prompt=null, preserve; succeeded, 41,828 s z ładowaniem, 4 segmenty, 29/29 słów z czasami, ostatni koniec 19,707 s. Komplet TXT/SRT/JSON/run/request/log/work, accepted_by_engine. Bez oceny jakości 29 słów. |
| Anulowanie / Job Object | **PASS** dotychczasowych testów potomnego FFmpeg i niezależnego procesu, natychmiastowego anulowania oraz rzeczywistego przerwania aktywnego FFmpeg podczas preserve AUDIO-01; potomny proces zakończony, status cancelled, brak preparation potwierdzającego sukces. |
| AUDIO-01 | **PASS** przygotowania obu wariantów i pięciu opisanych zdarzeń waveform. Bez transkrypcji pełnych 98 min. |
| Oryginał i konfiguracje | **PASS** SHA-256 przed/po AUDIO-01: b3b0d503b8a640580347c671ebb51751174929179b5206a9b4bb1d11abf6f45c; webinarowy JSON i local.toml bez zmiany hashy. Testy potwierdzają brak zapisu obu profili przez GUI/kontroler. |
| Referencyjny WhisperX | **PASS w zakresie pomiaru**: 46565 plików, identyczne ścieżki/rozmiary/mtime_ns przed i po; nie pełne hashe zawartości instalacji. Nie wykonywano tam zapisów, instalacji/pobrań ani poleceń sugerowanych przez ostrzeżenia bibliotek. |
| Składnia/konfiguracja | **PASS** AST src/tests, TOML i oba profile. |
| Widoczny GUI z rzeczywistym ASR i odsłuch/lip-sync użytkownika | **NOT TESTED**: automatyczne testy Tkinter używają ukrytego okna; rzeczywisty ASR przez kontroler. Pomiar waveform nie zastępuje oceny człowieka. |
| Ponowne rzeczywiste anulowanie w ASR/alignment, osobny ASR webinaru, CPU/inne compute, drugie stanowisko | **NOT TESTED w tym zadaniu**, brak zmian adaptera/Job Object/preflight; użyto proporcjonalnej regresji, rzeczywistego ASR sesji i anulowania FFmpeg. Historycznych dowodów nie przedstawiono jako nowych testów. |

Końcowe FAIL: 0. Początkowe błędy nowych fixture'ów, problem cykli Tk i sporadyczny WinError 5 zostały zdiagnozowane; końcowe testy dotyczą poprawionego kodu. Nie instalowano brakującego narzędzia monitorowania procesów — do obserwacji potomnego FFmpeg użyto natywnego API Windows przez standardową bibliotekę. Krótki ASR wykonano przed końcową poprawką ponawiania replace i neutralnym komunikatem drobnego offsetu; finalne testy zapisu/eksportów pokrywają te zmiany, bez ponawiania silnika.

Dowody wyłącznie lokalne, ignorowane:

- `runs/next_version_b511b9f604ef4d2e857eacb639e22032`: proof.json, inwentarz źródła, pakiety FFprobe, timeline_comparison.json, wyniki testów i krótka próbka. Niekompletne początkowe pomiary ciszy w timeline_legacy.json nie są dowodem synchronizacji; rozstrzygające jest timeline_comparison.json.
- Legacy prepare: `runs/jobs/20261018_104131_b8055a792551454cacb942ba0865a3b5`.
- Preserve prepare: `runs/jobs/20261018_104557_1349cdc0f0ac4971a278d69d0c4ce840`.
- Krótki ASR: `runs/jobs/20261018_104559_fa87a8beb0d24ba99ebde224f6420be5`.
- Anulowanie aktywnego FFmpeg: `runs/jobs/20261018_104834_501f98e0ab2543de9cc6ba34a29e0df9`.

Testy nie usuwają własnych danych ani wcześniejszych wyników. Nagrania/transkrypcje/logi i lokalna konfiguracja nie trafiają do Git. Nie wykonano push ani zmiany tagu mvp-v1.0. Rekomendacja Work: gotowe do odbioru w powyższym zakresie, z jawnymi NOT TESTED i trzema historycznymi PARTIAL MVP; decyzja należy do użytkownika i głównej rozmowy.
