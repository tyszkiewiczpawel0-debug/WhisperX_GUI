# Bieżący stan — 14.10.2026, po pilotażu D3

**D3: PARTIAL, do oceny użytkownika. D0–D2.1 zatwierdzone zleceniem D3. D4 nie rozpoczęto.**

Jeden pełny przebieg Webinar_RUI_2026-10-14.mp4 (1:58:43) zakończył się succeeded w 196,781 s. Profil WEBINAR_RUI_PL: large-v3/pl/cuda/float16/batch 8, alignment włączony, diarizacja wyłączona. Dokładny prompt terminologiczny zlecenia przyjęty przez silnik i zapisany w run.json; profil niezmieniony.

Wyniki: `C:\AI\WhisperX_GUI\runs\jobs\20261014_190042_d74c919aa76a4dfe9e6582273f727323`. Komplet TXT/SRT/JSON/run.json/process.log; 748 segmentów, 11903 słowa z czasami. TXT/SRT zgodne z JSON. WAV 16 kHz mono ma różnicę długości +0,312 ms. Ostatni znacznik 23,688 ms poza WAV, w tolerancji aplikacji 100 ms; ścisła kontrola granicy nie przeszła dla ostatniego segmentu/słowa. Brak nakładania segmentów.

Przejrzano tekst początku/środka/końca; podejrzane pożegnania na początku i długie przerwy wymagają odsłuchu. Kontrola akustyczna, kompletność mowy, synchronizacja oraz wpływ promptu na jakość: NOT VERIFIED. Pełny przebieg wywołano przez istniejący kontroler, bez sterowania widocznym GUI w D3. RAM niedostępny w diagnostyce; największa punktowa obserwacja całej karty GPU 9309/16303 MiB, nie pomiar szczytu.

Oryginał: SHA-256 przed/po identyczne. Chronione źródło: identyczne ścieżki/rozmiary/mtime_ns 46565 plików, nie pełny hash instalacji. Profil/local.toml bez zmian. Bez instalacji, pobierania, zmian środowiska, nadpisania wcześniejszych wyników i push. Kod aplikacji nie wymagał zmian; znane ostrzeżenia TorchCodec/TF32 nie zablokowały pracy. Worker zakończony kodem 0, kontroler zwolnił proces.

Kolejny krok: użytkownik ocenia raport i wykonuje odsłuch wskazanych fragmentów; dalszy etap wymaga decyzji. Start aplikacji: dwuklik Start.cmd.

[Raport D3](D3_PILOT_REPORT.md), [decyzje](DECISIONS.md), [checkpoint](../99_HANDOFF/CURRENT/HANDOFF.md). Historyczne testy: [D2.1](D2_1_TEST_REPORT.md), [D2](D2_TEST_REPORT.md).
