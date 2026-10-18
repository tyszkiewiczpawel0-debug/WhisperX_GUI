# Bieżący stan — 18.10.2026, finalizacja v1.1.0

**RELEASE CANDIDATE READY — PENDING FINAL ACCEPTANCE**

Użytkownik autoryzował finalizację po pozytywnym odbiorze funkcjonalnym GUI: uruchomienie, oba profile, reset nadpisań i responsywność podczas rzeczywistego WhisperX. Potwierdził pełną transkrypcję AUDIO-01 succeeded i komplet wyników. Ten przebieg używał legacy i zgłosił −405 ms; manifest lokalnego zadania 20261018_110836_9aeb60370a554010b1df99798e1486a8 potwierdza tryb, status i obecność plików. Nie jest to pełny test preserve.

**Domyślne tryby wydania:** sesja_rady_gminy=preserve (jawne pole JSON), WEBINAR_RUI_PL=legacy (bajtowo niezmieniony JSON). Brak pola zawsze oznacza legacy. Bez zmian src, przełącznika GUI, globalnej metody przygotowania lub kontraktu wyników. Do wczytania nowego defaultu uruchom aplikację ponownie; profile są ładowane przy starcie.

Finalizacja używa 23 testów automatycznych: wszystkie PASS na gałęzi roboczej (6,585 s), w tym walidacja defaultów, brak pola=legacy, A → B → A, snapshoty request/run z rzeczywistym workerem i regresja obu trybów. Eksporty TXT/SRT/JSON oraz blokady offline/zapisu PASS. Przed lokalnym tagiem ponownie weryfikowany jest main. Logi i końcowy protokół refs: runs/finalization_2e0513d7a00f425cb68da196ff457360 (ignorowane).

Lokalny kandydat wydania: main i tag v1.1.0 mają wskazywać ten sam końcowy commit po integracji codex/multiple-profiles; dokładny SHA odczytuje git rev-parse HEAD oraz git rev-parse 'v1.1.0^{commit}', zgodność jest sprawdzana w końcowej kontroli. Wejście: d446143 na gałęzi roboczej, main=a677fc6. Punkt mvp-v1.0 pozostaje a677fc6f62620752156fd2565edac6e3585090e0. Stan końcowy Git i pełne identyfikatory przekazuje odpowiedź finalizacyjna. Bez publikacji zdalnej.

Zachowane dowody: pięć zdarzeń AUDIO-01 zachowuje synchronizację w preserve (sekcja 5 planu), wcześniejszy 20-sekundowy rzeczywisty ASR sesji/preserve succeeded. Nie powtarzano pomiaru pełnego audio ani ASR w finalizacji. Użytkownik potwierdził funkcjonalny GUI i pełny ASR legacy; **NOT TESTED** nadal: pełny 98-minutowy ASR preserve, całościowy odsłuch/lip-sync i ocena wszystkich słów, drugie stanowisko, CPU/inne compute oraz ponowne rzeczywiste anulowanie ASR/alignmentu. Nie przenosimy starego NOT TESTED funkcjonalnego GUI na stan po jego odbiorze. Historycznych trzech PARTIAL MVP w tagu nie przepisano.

[Raport finalizacji](../NEXT_VERSION_IMPLEMENTATION_PLAN.md#6-finalizacja-i-odbiór-funkcjonalny--18102026), [decyzje D-51–D-54](DECISIONS.md), [handoff](../99_HANDOFF/CURRENT/HANDOFF.md), [instrukcja](../README.md). Uruchomienie Start.cmd → profil sesji (preserve) lub webinar (legacy). Odbiorcy: użytkownik i główna rozmowa ChatGPT projektu. Work przygotowuje lokalnego kandydata, nie zatwierdza samodzielnie wydania i nie rozpoczyna dalszego rozwoju.
