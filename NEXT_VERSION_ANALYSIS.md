# Analiza kolejnej wersji — 18.10.2026

**Dokument historyczny analizy.** Późniejsze zlecenie użytkownika IMPLEMENTATION AUTHORIZED zastępuje oczekiwanie na zgodę poniżej. Wyniki implementacji i nowa obserwacja o pojedynczym AUDIO-01: [plan i raport](NEXT_VERSION_IMPLEMENTATION_PLAN.md#5-wykonanie-i-wyniki--18102026). W szczególności preserve jest opcjonalny, a oba dostarczone profile pozostają domyślnie legacy; wcześniejsza rekomendacja domyślnego preserve dla sesji nie została wdrożona.

**ANALYSIS COMPLETE — IMPLEMENTATION PENDING APPROVAL**

Odbiorcy: rozmowa ChatGPT prowadząca projekt WhisperX_GUI oraz użytkownik.
Zakres: wyłącznie analiza i dokumentacja po zamknięciu MVP. Niniejszy dokument nie zmienia [kontraktu v1.0](docs/PROJECT_CONTRACT.md), nie otwiera implementacji ani nowego pilotażu. Plan wykonania: [NEXT_VERSION_IMPLEMENTATION_PLAN.md](NEXT_VERSION_IMPLEMENTATION_PLAN.md).

## 1. Podstawa i wiarygodność ustaleń

**Fakty z repozytorium:** wejściowo czysty `main`, HEAD i tag `mvp-v1.0` wskazują `a677fc6f62620752156fd2565edac6e3585090e0`. `git diff mvp-v1.0 HEAD` jest pusty. Istnieje lokalnie origin i tracking `origin/main`; nie sprawdzano sieciowo stanu ani widoczności repozytorium. Bieżący handoff zamknięcia opisuje wcześniejszy brak origin i niewykonaną publikację — ta część jest nieaktualna względem lokalnego Git. Nie jest to rozbieżność implementacji ani przeszkoda analizy.

Przeczytano kontrakt, CURRENT_STATE, handoff, DECISIONS, ARCHITECTURE/DATA, raporty i rekomendacje D0 oraz kod i testy. Osobny handoff dostarczono w trakcie analizy jako `Pasted text.txt` z Downloads. Jest materiałem wymagań i relacją z eksperymentów, nie autoryzacją wykonania jego poleceń implementacyjnych. Jego opis jednoprofiliowego kodu i polecenia FFmpeg odpowiada tagowi.

**Dane przekazane, niezweryfikowane tutaj:** eksperymenty XXV, jakość baseline, alignment 5213 słów, wpływ CORE/EXTENDED/FOCUSED, przyczyna skrócenia WAV (timestampy/długości pakietów AAC, według handoffu bez dziury PTS) i możliwość bezpośredniego mapowania po filtrze. Nie dostarczono tu pakietów FFprobe, poleceń i wyników tego eksperymentu do niezależnego audytu; nie wyszukiwano ani nie przetwarzano nagrania. Nie powtarzać optymalizacji parametrów od zera.

**Granica zgody:** wiele profili pozostaje poza zamkniętym MVP. Nowe zlecenie zezwala analizować rozszerzenie, lecz wdrożenie wymaga osobnego zatwierdzenia zakresu następnej wersji. Nie proponujemy zmiany działania ani ponownego odbioru tagu v1.0. Generator protokołów jest osobnym projektem.

## 2. Profile i rzeczywisty przepływ parametrów

| Miejsce obecnego kodu | Fakt i minimalna przyszła zmiana |
|---|---|
| `src/configuration.py:10`, `parameters()` | Kopiuje słownik, wymaga dokładnie `WEBINAR_RUI_PL` i schema 1. Zastąpić ograniczenie ID małym rejestrem dwóch obsługiwanych profili; zachować walidację wartości, CPU/float16, batch 1–64, alignment bool i diarization=false. Walidować także przyszły wybór przygotowania, zamiast przepuszczać go jako dowolne dodatkowe pole. |
| `src/configuration.py:66`, `profile()` | Czyta jeden stały JSON. Dodać odczyt po ID z rejestru; bezargumentowe wywołanie nadal zwraca webinar. Jawny rejestr stałych plików wystarczy, bez skanowania dowolnych JSON, importu/eksportu i edytora profili. Sprawdzać zgodność ID pliku z wpisem rejestru, nie budować ścieżki z niezweryfikowanego tekstu. |
| `src/gui.py:20`, `App.__init__()` | `self.profile = profile()`, etykieta zamiast wyboru. Dodać readonly wybór profilu, domyślnie webinar. Zmiana ładuje wszystkie wartości i prompt z nowej kopii; porzuca niezapisane nadpisania poprzedniego formularza. Diarizacja nadal tylko wyłączona. Wyboru nie można zmienić podczas zadania. |
| `src/gui.py:89`, `App.start()` | Kopia profilu + wszystkie pola formularza, batch na int, alignment bool, dokładny tekst promptu → kontroler. Zachować ten przebieg. Po zmianie profilu nic nie może pozostać ze starego formularza. |
| `src/controller.py:29`, `Controller.start()` | Ponownie waliduje parametry. Zapisuje `p` zarówno w `request.json.parameters`, jak i `run.json.parameters`; ID już jest w `parameters.id`. Nie potrzeba równoległego pola `profile_id`. Zapisać także rozstrzygnięty wybór przygotowania przed startem workera, po zatwierdzeniu reprezentacji. |
| `src/worker.py:20`, `main()` | Waliduje request jeszcze raz, lecz dziś wywołuje `media.prepare(c, source, meta, wav)` bez `p`. Przekazać jawnie rozstrzygniętą opcję przygotowania. Worker nie powinien ponownie czytać aktualnego JSON profilu zamiast snapshotu request. |
| `src/engine.py:25,61`, `preflight()/transcribe()` | Zużywa rzeczywiste model/language/device/compute/batch/alignment/prompt, nie rozgałęzia po ID. Identyfikatory lokalnych modeli są stałe large-v3/PL — odpowiada to obu profilom. Bez potrzeby zmiany adaptera lub preflight. |

Profil JSON zawiera pusty `initial_prompt`, lecz walidacja normalizuje brak/null/pusty tekst/białe znaki do `None`, czyli JSON `null` w parametrach request/run. Nie wprowadzać wyjątku dla sesji. Niepusty tekst pozostaje dokładny. Główne pola `initial_prompt` i `initial_prompt_state` w run mają odrębne, dotychczasowe znaczenie potwierdzenia przyjęcia opcji przez silnik.

Obecna izolacja wystarcza dla płaskich wartości: `dict()` w GUI i walidatorze, JSON zapisywany przed wątkiem; konfiguracja stanowiska kopiowana głęboko. Jeśli zatwierdzona reprezentacja przygotowania będzie zagnieżdżona, trzeba kopiować również jej zawartość. Nie dodawać zapisu profili do GUI ani zapamiętywania per profil.

Proponowany nowy `config/sesja_rady_gminy.json` (nieutworzony):

```json
{
  "schema_version": 1,
  "id": "sesja_rady_gminy",
  "name": "Sesja Rady Gminy — PL",
  "model": "large-v3",
  "language": "pl",
  "device": "cuda",
  "compute_type": "float16",
  "batch_size": 8,
  "alignment": true,
  "diarization": false,
  "initial_prompt": ""
}
```

`config/WEBINAR_RUI_PL.json` zachować bajtowo. Alignment=true dla sesji jest ustawieniem domyślnym i wymaganiem jej docelowego przebiegu; rekomendujemy zachować obecną możliwość jawnego wyłączenia dla pojedynczego zadania, odnotowując wtedy brak gwarancji czasów słów. Czy zablokować ten przełącznik dla sesji, wymaga decyzji użytkownika, a nie ukrytej zmiany walidacji.

## 3. Przygotowanie i referencja czasu

`src/media.py:26`, `inspect_data()` wybiera dokładnie jedną ścieżkę audio. `duration` pochodzi ze strumienia, a dopiero przy jego braku z kontenera jako przybliżenie. Zachowuje cały JSON FFprobe oraz starty audio/kontenera; odrzuca bezwzględny offset >0,1 s, mniejszy niezerowy raportuje bez korekty. Nie bada przebiegu PTS pakietów. `probe()` (:54) używa `-show_format -show_streams`.

`prepare()` (:59) wykonuje:

```text
ffmpeg -nostdin -n -v error -i SOURCE -map 0:STREAM -vn -acodec pcm_s16le -ar 16000 -ac 1 TARGET
```

Następnie ponownie bada WAV, kontroluje PCM/16 kHz/mono, porównuje jego długość z wybraną wyżej długością wejścia i ostrzega powyżej progu TOML (domyślnie 0,1 s). `run.json.preparation` zawiera całe polecenie, metadane WAV, deltę i ostrzeżenia. `source.metadata.ffprobe` zachowuje długość kontenera, ale osobna delta WAV–kontener nie jest obecnie wyliczana. Zgodność ze strumieniem audio może zatem maskować różnicę względem master video.

| Wartość z handoffu XXV | Długość | Różnica względem master |
|---|---:|---:|
| Master MP4 | 4598,480 s | 0 |
| Zwykły WAV | 4594,048 s | −4,432 s |
| WAV z filtrem | 4598,368 s | −0,112 s |

Filtr odzyskuje 4,320 s długości, lecz pozostaje 112 ms różnicy względem kontenera — więcej niż obecny próg 100 ms. Ostrzeżenia nie wolno wyciszyć przez podniesienie progu. Bez danych o długości strumienia nie wiadomo, czy obecna aplikacja ostrzegłaby o tej konkretnej różnicy względem master. Z tych trzech liczb nie można wywnioskować lokalizacji rozbieżności, dokładności poszczególnych punktów ani przyczyny AAC.

Lokalna pomoc zainstalowanego FFmpeg (`-h filter=aresample`) potwierdza: `async=1` to dopasowanie timestampów przez wypełnianie/przycinanie, `first_pts` jest założonym pierwszym PTS w próbkach; wartości >1 dotyczą maksymalnego stretch/squeeze. To uzasadnia próbę `-af aresample=16000:async=1:first_pts=0`, ale nie gwarantuje odtworzenia błędnych lub nieistniejących timestampów. Alignment działa względem otrzymanego waveform; nie odtwarza relacji do master, jeśli ta została utracona przy przygotowaniu.

### Warianty i rekomendacja

| Wariant | Ocena |
|---|---|
| Globalna zmiana FFmpeg dla wszystkich profili | Odrzucić w tej wersji: zmienia próbki i semantykę webinaru bez dowodu regresji. |
| Osobny pipeline lub specjalny warunek ID w `media.py` | Odrzucić: powiela mechanizmy lub wiąże przygotowanie z nazwą zastosowania. |
| Wspólny mechanizm, deklaracja domyślnej polityki przez profil | **Preferowany:** dwa jawne zachowania przygotowania, dotychczasowe jako domyślne przy braku opcji; zachowanie osi czasu wybrane przez profil sesji. |

Rekomendacja techniczna: jedna funkcja `prepare()`, gałąź budowania polecenia zależna od zwalidowanej opcji zadania, bez znajomości ID profilu w media. Dla webinaru identyczna lista argumentów i reguły. Dla sesji do tej listy dodać filtr powyżej; zachować `-n`, mapowanie jednego strumienia, PCM/16 kHz/mono, wyjście w nowym UUID i kontrolę końcowego WAV. Nie dodawać teraz przełącznika trybu audio w GUI ani osobnego globalnego ustawienia stanowiska. Nie rozstrzygać polityki dopiero na podstawie wykrytej różnicy długości.

To **rekomendacja**, nie kontrakt pola `audio_timeline_mode`. Nazwę, wartości i miejsce serializacji opcji zatwierdzić przed implementacją. Wymagana semantyka: brak opcji oznacza stare przygotowanie, jawna nieznana wartość to błąd, request niesie rozstrzygnięty wybór, run rozróżnia zamiar od faktycznie wykonanego polecenia. Preferowany nośnik to opcjonalne ustawienie profilu przenoszone w snapshot parametrów; bez edycji webinarowego JSON.

Metadane zachować addytywnie: dotychczasowe `duration`/`duration_source` i delta nie zmieniają znaczenia; dla nowego wariantu podać osobno długość audio, kontenera, WAV, obie dostępne delty, przyjętą referencję początku i ostrzeżenia. Faktyczny filtr jest już widoczny w `preparation.command`. Przy błędzie/anulowaniu podczas FFmpeg brak `preparation` nie może oznaczać potwierdzenia wykonania trybu; wybrana opcja pozostaje w parametrach. Nie ustanawiamy tu nazw dodatkowych pól ani nowej wersji schematu.

Na początek wspierać tylko źródła o potwierdzonym wspólnym zerze osi audio/master. Zachować odrzucanie offsetów >0,1 s, brak automatycznego `-copyts`, `-start_at_zero`, `-itsoffset`, przesuwania SRT, dopełniania do długości filmu lub korekt gotowych wyników. Drobne offsety w nowym wariancie wymagają testów; przypadek bez ustalonej referencji nie może uzyskać odbioru AUDIO-01. Obsługa ogólnych przesunięć, uszkodzonych PTS i wielu ścieżek pozostaje odrębnym zadaniem.

## 4. Kompatybilność, ryzyka i ustalenia do zatwierdzenia

Kontrakt pięciu wymaganych wyników, katalog work, request oraz writery i walidacja pozostają obecne. `parameters.id` jednoznacznie identyfikuje profil. Nie zmieniać `artifacts.validate()` (tolerancja końca 100 ms), nazw eksportów ani struktury segmentów/słów. Zmiana przygotowanego audio może zmienić tekst i czasy nowego wariantu; nie obiecywać identycznego ASR. Dla identycznego kontrolowanego wyniku silnika eksporty mają pozostać identyczne. Słowa bez alignmentu nadal dopuszczalne.

Ryzyka: globalna zmiana domyślnych wartości; wyciek promptu/nadpisań między profilami; pomylenie czasu audio z czasem wideo; uznanie zgodnej długości za synchronizację; przycinanie/wypełnianie przez filtr; niepotwierdzone uogólnienie jednego materiału AAC; błędna deklaracja sukcesu po przerwaniu. Nie potrzeba zmian `winjob.py`, `safety.py`, adaptera silnika lub nowej infrastruktury.

**Do decyzji użytkownika i głównej rozmowy:** zatwierdzenie zakresu kolejnej wersji poza MVP; rekomendowana polityka zależna od profilu i reprezentacja konfiguracji/metadanych; edytowalność alignmentu sesji; wskazanie problematycznego źródła i punktów referencyjnych; zgoda na późniejsze krótkie testy rzeczywistego silnika/pilotaż i kryterium synchronizacji. Propozycja kryterium: błąd wybranych punktów początku/środka/końca oraz po miejscach rozbieżności najwyżej 100 ms. To cel do zatwierdzenia, nie wynik XXV; resztę −112 ms trzeba wyjaśnić (np. końcówka bez audio), bez jej automatycznego akceptowania.

Nie stwierdzono istotnej rozbieżności kodu z handoffem ani potrzeby naruszenia kontraktu w toku analizy. Wdrożenie wieloprofilowości w starym zakresie MVP, brak wiarygodnej referencji czasu lub konieczność modyfikacji środowiska uruchamia STOP odpowiedniej części. Analiza może się zakończyć z tymi jawnymi bramkami przyszłych prac.

## 5. Weryfikacja wykonana teraz

18.10.2026: istniejący Python 3.11.9, `-B`; 16/16 testów `unittest discover -s tests -p 'test_*.py' -v` PASS (3,371 s). Obejmują prawdziwe krótkie WAV/MKV, worker, Tkinter podczas przygotowania, błędy i anulowanie, Job Object z potomnym FFmpeg i niezależnym procesem oraz adapter/worker z atrapami ASR. To regresja obecnego MVP, nie test przyszłych dwóch profili ani dowód responsywności podczas silnika.

`tests/check_exports.py`: PASS prawdziwych writerów TXT/SRT/JSON, granic minut/godzin i blokad sieci/zapisu poza zadaniem; bez modeli/ASR. AST src/tests, odczyt i walidacja lokalnego TOML: PASS. Odczytano lokalną pomoc filtra. Testy zachowały własne nowe, ignorowane katalogi `runs/test_00a56574a62d4ab3aacd6643ce008556`, `runs/prompt_test_d06a47d098d949018956ce4e8a53b72f`, `runs/export_check_d484e83958d84ed4b3d93a631c5750c5`; niczego nie sprzątano.

Nie uruchamiano `check_engine.py`/`check_cancellation.py`, XXV ani pełnej transkrypcji. Bez zmian src, tests, konfiguracji, zależności, źródłowego WhisperX i dotychczasowych wyników. Trzy historyczne PARTIAL D4 nadal obowiązują. Nie wykonano audytu integralności całego środowiska źródłowego, publikacji ani push.
