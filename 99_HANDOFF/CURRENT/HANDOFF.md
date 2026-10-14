# WHISPERX_GUI — checkpoint D3

Data: 14.10.2026. Odbiorca: główna rozmowa ChatGPT WHISPERX_GUI, za pośrednictwem użytkownika.

**D3: PARTIAL.** D0–D2.1 zatwierdzone w zleceniu D3. Jeden pełny przebieg succeeded, ale odsłuch i jakość akustyczna NOT VERIFIED. D4 nie rozpoczęto.

## Nagranie i parametry

`C:\AI\WhisperX_GUI\INPUT\Webinar_RUI_2026-10-14.mp4`, 321387385 B, audio 7123,029 s. SHA-256 przed/po: `fd7bc2854a3a01a889972f9c2252e89e3a2c2c9320d78dc68398e53327cb6660`. Jedna ścieżka AAC 48 kHz stereo, offset 0. WAV PCM s16le/16 kHz/mono, delta +0,312 ms, bez cięć.

WEBINAR_RUI_PL: large-v3/pl/cuda/float16/batch 8/alignment=true/diarization=false. Prompt uruchomienia przyjęty (`accepted_by_engine`), identyczny w konfiguracji i potwierdzeniu run.json:

> Rejestr Urbanistyczny, plan ogólny gminy, miejscowy plan zagospodarowania przestrzennego, decyzja o warunkach zabudowy, akt planowania przestrzennego, GML, APP, dane przestrzenne, zbiór danych przestrzennych, geoportal.

## Pięć artefaktów

Wspólny katalog: `C:\AI\WhisperX_GUI\runs\jobs\20261014_190042_d74c919aa76a4dfe9e6582273f727323`:

- `transcript.txt` — tekst;
- `transcript.srt` — napisy;
- `transcript.json` — segmenty i słowa;
- `run.json` — źródło, rzeczywiste parametry, wersje i status;
- `process.log` — etapy i ostrzeżenia.

Pełna transkrypcja z alignmentem: 196,781 s, exit_code=0, proces zwolniony. 748 segmentów, 11903 słowa z czasami. TXT/SRT zgodne z JSON, brak nakładania segmentów. Zakres 8,819–7123,053 s; ostatni koniec 23,688 ms poza WAV, w tolerancji aplikacji 100 ms. Nie korygowano wyników. Najdłuższa przerwa 162,242 s wymaga odsłuchu.

## Jakość, ograniczenia i ochrona

Przegląd tekstu trzech okien początku/środka/końca wykonany. Podejrzane pożegnania w 95–154 s, przerwy i końcówka do odsłuchu. Kompletność mowy, synchronizacja, poprawność specjalistycznych pojęć względem audio i wpływ promptu: NOT VERIFIED. Nie wykonano oceny prawnej ani streszczenia. D3 wywołany przez kontroler aplikacji; interakcja z widocznym GUI podczas tego przebiegu nieweryfikowana.

Największa próbka VRAM całej karty: 9309/16303 MiB; nie szczyt procesu. RAM niedostępny w tej diagnostyce. Znane ostrzeżenia TorchCodec i TF32; adaptacja checkpointu Lightning tylko w pamięci. Bez błędu zasobów i bez powtórzenia pełnej transkrypcji.

Oryginał niezmieniony (SHA-256); 46565 plików chronionego C:\AI\WhisperX bez zmian ścieżek/rozmiarów/mtime_ns, nie pełne hashowanie instalacji. Profil i local.toml bez zmian. Bez instalacji, pobrań, zmiany venv, nadpisania wcześniejszych wyników i push. Dowody w `runs/d3_20261014_190033`, poza Git. Brak zmian implementacji.

[Pełny raport D3](../../docs/D3_PILOT_REPORT.md) opisuje kontrole, przerwy, próbki tekstu, czas i ograniczenia. [Stan](../../docs/CURRENT_STATE.md), [decyzje](../../docs/DECISIONS.md).

## Git i następna decyzja

Branch main. Kod pilotażu: `f45474170fc8da67537cdd59d9eab337fd9e3c9a`. Lokalny commit dokumentacji: `Document RUI pilot results and verification limits`; jego SHA i status po commicie w odpowiedzi końcowej. Zakres commita: raport, stan, decyzje, README i ten jeden handoff, bez danych.

Rekomendowany następny krok: odsłuch wskazanych fragmentów i ocena D3 przez użytkownika. Nie uruchamiać automatycznie kolejnej transkrypcji. Nie rozpoczynać D4 ani rozwoju bez decyzji użytkownika.
