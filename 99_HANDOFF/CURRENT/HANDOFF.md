# WHISPERX_GUI — finalizacja lokalnego kandydata v1.1.0

Data: 18.10.2026. Odbiorcy: **użytkownik i główna rozmowa ChatGPT projektu WhisperX_GUI**.

**RELEASE CANDIDATE READY — PENDING FINAL ACCEPTANCE**

## Zatwierdzony zakres i stan Git

FINALIZATION AUTHORIZED zezwala na zmianę defaultu sesji po odbiorze funkcjonalnym GUI, testy, lokalną integrację i tag. Bez nowego rozwoju, instalacji, modyfikacji C:\AI\WhisperX, nadpisywania wyników i publikacji.

Punkt wejścia: czyste codex/multiple-profiles / d446143ce5ff9074bfc3b119170d4fcfe5ade472; main=mvp-v1.0=a677fc6f62620752156fd2565edac6e3585090e0. Zastany jedyny tag mvp-v1.0, brak kolizji v1.1.0. Commit konfiguracji/testów/dokumentacji 387c1786a23211075aa4658a870be96e093a05ef zintegrowano lokalnie z main przez fast-forward bez konfliktów i utraty historii. Lokalny tag v1.1.0 identyfikuje finalny checkpoint main po dodaniu niniejszego podsumowania; pliki kodu i konfiguracja są identyczne z przetestowanym 387c178. Dokładny końcowy SHA HEAD main i commita tagu podaje odpowiedź końcowa oraz lokalny protokół runs/finalization_2e0513d7a00f425cb68da196ff457360/release_refs.json. Polecenia odtworzenia: git rev-parse HEAD oraz git rev-parse 'v1.1.0^{commit}'; oba mają dawać ten sam commit. Working tree jest kontrolowany po integracji i tagowaniu. Nie zmieniać mvp-v1.0. Bez push i operacji zdalnych.

## Zachowanie wydania

sesja_rady_gminy domyślnie **preserve**, przez jawne audio_timeline_mode w JSON. WEBINAR_RUI_PL nadal **legacy** i bajtowo niezmieniony względem mvp-v1.0. Brak pola nadal legacy dla dowolnego ID. Jedyna zmiana działania od d446143 to default sesji; src, offline, worker, Job Object, anulowanie, preflight, writery i struktury wyników bez zmian. Nie dodano przełącznika GUI. Przełączenie profilu resetuje formularz, a parameters.id/audio_timeline_mode w request/run wskazują wybór; worker nie wczytuje ponownie profilu.

Po ponownym uruchomieniu Start.cmd wybierz sesję: preserve jest już domyślny, nie trzeba edytować JSON. Webinar pozostaje legacy. Już uruchomione okno wymaga restartu, ponieważ definicje ładowane są przy starcie.

## Odbiór użytkownika i dowody audio

**Potwierdzone przez użytkownika:** start GUI, oba profile, reset parametrów po zmianie, responsywność podczas rzeczywistego WhisperX, pełny AUDIO-01 succeeded i komplet eksportów/metadanych. Był to przebieg **legacy**, ostrzeżenie −405 ms. Work dodatkowo odczytał wyłącznie techniczny run.json i obecność wymaganych plików zadania runs/jobs/20261018_110836_9aeb60370a554010b1df99798e1486a8; nie oceniał treści transkrypcji. Tego przebiegu nie przedstawiać jako pełnego preserve.

Ponownie wykorzystano dowody poprzedniego etapu: MP4 5884,600 s, audio 5884,501 s; legacy WAV 5884,096 s, preserve 5884,501 s. Pięć zdarzeń 774,750 / 1967,000 / 2953,250 / 4417,750 / 5881,000 s: legacy wyprzedza o 109 / 213 / 213 / 405 / 405 ms, preserve zgodny w granicach pomiaru 0,0625 ms. Pozostałe 99 ms do końca wideo nie są automatycznie dopełniane. To uzasadnienie zmiany defaultu przez użytkownika, nie uniwersalna gwarancja dla dowolnego źródła. Krótki wcześniejszy ASR preserve miał succeeded (20 s, 4 segmenty, 29/29 słów z czasami).

## Testy i ograniczenia

- **PASS:** 23/23 testów regresji na gałęzi roboczej (6,585 s), defaulty obu profili, brak pola=legacy, A → B → A, reset nadpisań, request/run i wykonanie realnego workera prepare bez nadpisania trybu, niezmienność webinarowego JSON, regresja obu trybów/anulowania/Job Object/promptu. ASR w unit testach orkiestracji jest atrapą.
- **PASS:** rzeczywiste writery TXT/SRT/JSON, granice czasu i słowa z/bez alignmentu, blokady offline i zapisu. Po integracji na main ponownie **PASS 23/23 (6,082 s)** i eksporty/offline. Walidacja obu defaultów, kontraktu wynikowego, AST, linków/UTF-8 i Git/ignore PASS. Finalny checkpoint zmienia następnie wyłącznie niniejsze podsumowanie/dokumenty wyników; kod i konfiguracja pozostają identyczne z testem main.
- **FAIL:** brak w zakończonych testach. Logi nowej finalizacji w powyższym katalogu runs; dawne dowody i wyniki zachowane.
- **NOT TESTED:** pełna transkrypcja 98 min w preserve, całościowy odsłuch/lip-sync i jakość wszystkich słów, inne stanowisko, CPU/inne compute, ponowne realne anulowanie ASR/alignmentu. Finalizacja nie powtarza pełnego ASR. Odbiór użytkownika usuwa wcześniejszą niewiadomą funkcjonalnego GUI dla tej wersji; historyczne trzy PARTIAL MVP pozostają zapisane w dokumentacji/tagu bez zmiany.

[Raport finalizacji](../../NEXT_VERSION_IMPLEMENTATION_PLAN.md#6-finalizacja-i-odbiór-funkcjonalny--18102026), [CURRENT_STATE](../../docs/CURRENT_STATE.md), [DECISIONS D-51–D-54](../../docs/DECISIONS.md), [README](../../README.md). Repozytorium nie zawiera nagrań, transkrypcji, logów, lokalnej konfiguracji ani modeli. Nie wykonano push ani publikacji zdalnej. Work przygotowuje kandydata do ostatecznego odbioru przez użytkownika i główną rozmowę; samodzielnie nie zatwierdza wydania.
