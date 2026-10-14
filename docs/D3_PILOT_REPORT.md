# D3 — pilotaż webinaru RUI, 14.10.2026

**Status D3: PARTIAL, do oceny użytkownika.** Jeden pełny przebieg zakończył się `succeeded`; kontrola akustyczna jest **NOT VERIFIED**. D0–D2.1 zatwierdzone i D3 autoryzowane w zleceniu użytkownika. D4 nie rozpoczęto.

## Źródło i preflight

Jedyny plik INPUT: `C:\AI\WhisperX_GUI\INPUT\Webinar_RUI_2026-10-14.mp4`, 321 387 385 B. Identyfikacja na podstawie jednoznacznej nazwy, daty i lokalizacji wskazanej przez użytkownika, metadanych OBS oraz zgodnej tematyki tekstu; nie niezależne poświadczenie pochodzenia nagrania.

SHA-256 przed i po: `fd7bc2854a3a01a889972f9c2252e89e3a2c2c9320d78dc68398e53327cb6660`.

MP4, H.264 1920×1080, jedna ścieżka audio AAC LC, 48 kHz stereo. Audio 7123,029 s (1:58:43,029), kontener 7123,066667 s. Offset audio i kontenera 0. FFprobe rozpoznał materiał bez ostrzeżeń. FFmpeg/FFprobe 8.1.2 dostępne. Wolne miejsce przed startem: 1 609 365 757 952 B.

Preflight aplikacji potwierdził lokalne modele ASR large-v3, polski alignment, VAD i NLTK oraz CUDA/float16. GPU NVIDIA GeForce RTX 5070 Ti. WhisperX 3.8.6, Python 3.11.9, torch/torchaudio 2.8.0+cu128, faster-whisper 1.2.1, CTranslate2 4.8.2. Pełne wersje, rewizje modeli i hashe kodu w run.json. Użyto istniejącego środowiska i mechanizmów offline.

## Parametry i wykonanie

Profil `WEBINAR_RUI_PL`: large-v3, pl, cuda, float16, batch_size=8, alignment=true, diarization=false. Bez fallbacku ani zmian profilu. Prompt pojedynczego uruchomienia:

> Rejestr Urbanistyczny, plan ogólny gminy, miejscowy plan zagospodarowania przestrzennego, decyzja o warunkach zabudowy, akt planowania przestrzennego, GML, APP, dane przestrzenne, zbiór danych przestrzennych, geoportal.

Dokładny tekst jest zgodny w request.json, parameters.initial_prompt i głównym initial_prompt w run.json; `initial_prompt_state=accepted_by_engine`. To potwierdza przyjęcie opcji przez load_model, nie poprawę jakości względem przebiegu bez promptu. Nie wykonano porównawczego ASR.

Uruchomiono aktualny Controller → worker → FFmpeg → WhisperX → alignment → eksport. Lokalny jednorazowy skrypt w ignorowanym runs/ wywołał kontroler i odebrał zdarzenia; nie zmieniono kodu aplikacji. W D3 nie sterowano widocznym GUI ani nie powtarzano testu jego responsywności. Wynik potwierdza pipeline aplikacji; interakcja użytkownika z GUI w trakcie pełnego webinaru pozostaje NOT VERIFIED.

WAV `work/audio.wav`: PCM s16le, 16 kHz, mono, 227 937 016 B, 7123,029312 s. Różnica względem audio +0,000312 s. Bez skracania, usuwania ciszy czy korekty osi czasu. Polecenie FFmpeg z `-n` i jawnym wyborem ścieżki zapisane w manifeście.

Przebieg 19:00:42–19:03:59 czasu Europe/Warsaw. Czas kontrolera **196,781 s (3 min 16,8 s)**, około 36,2× szybciej od czasu nagrania; pojedyncza obserwacja, nie benchmark. Czasy zaobserwowanych zdarzeń: preflight 19:00:42, prepare 19:00:46, asr_loading 19:00:52, asr 19:01:01, alignment_loading 19:02:36, alignment 19:02:37, export 19:03:57. Odbiór zdarzeń ma rozdzielczość około 0,2 s. ASR z VAD około 95 s, alignment około 80,5 s. Worker zakończył się kodem 0, kontroler nieaktywny, uchwyt procesu zwolniony.

## Wyniki i kontrola techniczna

Katalog wyników: `C:\AI\WhisperX_GUI\runs\jobs\20261014_190042_d74c919aa76a4dfe9e6582273f727323`.

| Artefakt | Rozmiar B | Kontrola |
|---|---:|---|
| transcript.txt | 89660 | 748 linii zgodnych z tekstem segmentów JSON |
| transcript.srt | 117976 | 748 kolejnych wpisów, poprawny format czasu, zgodność granic z JSON do 1 ms |
| transcript.json | 1872072 | 748 segmentów, 11903 słowa; wszystkie słowa mają start/end |
| run.json | 14881 | succeeded, exit_code=0, parametry, prompt, wersje, źródło i przygotowanie |
| process.log | 2894 | etapy i ostrzeżenia, końcowy sukces, bez traceback błędu pipeline |

Zakres segmentów: 8,819–7123,053 s. Brak ujemnych/odwróconych czasów, nieuporządkowanych lub nakładających się segmentów. **Ostatni segment i jego ostatnie słowo kończą się 23,688 ms poza WAV** (24 ms poza deklarowanym audio MP4), nadal przed końcem kontenera wideo. Walidator aplikacji dopuszcza 100 ms, dlatego succeeded jest zgodne z implementacją. Ścisła kontrola granicy WAV z tolerancją 1 ms wykazała dwa przekroczenia dotyczące tego samego końca. Nie oznaczamy jej jako PASS, nie przycięto wyników.

Najdłuższe przerwy między segmentami: 219,305–381,547 s (162,242 s), 5775,027–5838,038 s (63,011 s), 162,723–213,864 s (51,141 s), 7056,110–7102,884 s (46,774 s). Przerwy i brak tekstu przed 8,819 s nie dowodzą utraty mowy ani ciszy — wymagają odsłuchu.

## Jakość: analiza tekstu i niewykonany odsłuch

Przejrzano wszystkie segmenty przecinające okna 0–180 s, 3471,515–3651,515 s i 6943,029–7123,029 s (segmenty na granicach mogą wychodzić poza okno). Prywatne wycinki tekstu zapisano w lokalnym text_samples.json, poza Git.

- Początek: tekst prób dźwięku i rozmów otoczenia. Formuły pożegnalne w 95,443–123,472 oraz 133,016–153,560 s są podejrzane, szczególnie ze względu na długość przypisanego czasu; możliwa halucynacja ASR, **niepotwierdzona odsłuchem**.
- Środek: tekst jest zasadniczo czytelny, zawiera terminologię rejestru urbanistycznego, planowania przestrzennego i logowania. Widoczne niezgrabne formy językowe oraz zapisy nazw wymagają sprawdzenia. Nie rozstrzygamy, czy pochodzą z wypowiedzi, czy ASR.
- Koniec: tekst obejmuje zamknięcie prezentacji i późniejszą rozmowę; występują urwane lub niezgrabne sformułowania. Zachowano całość wejścia, w tym fragmenty otoczenia.

Kompletność mowy, zgodność nazw/specjalistycznych pojęć z audio, synchronizacja napisów oraz rzeczywisty wpływ promptu: **NOT VERIFIED**. Nie odtworzono materiału akustycznie, nie wyliczano WER ani nie zadeklarowano oceny prawnej/treściowej webinaru. Obecność terminów w tekście nie dowodzi skuteczności promptu.

## Zasoby, ostrzeżenia i ochrona

Punktowe odczyty nvidia-smi, cała karta (nie pamięć przypisana wyłącznie workerowi): 19:01:05 — 6575/16303 MiB, GPU 88%; 19:01:36 — 9309/16303 MiB, GPU 100%; 19:03:02 — 5133/16303 MiB, GPU 31%. Maksimum z próbek 9309 MiB **nie jest szczytem całego przebiegu**. RAM: NOT VERIFIED — Get-Process nie zwrócił procesów Python w dostępnej sesji. Nie instalowano monitoringu. Nie zaobserwowano OOM ani błędu zasobów.

Znane ostrzeżenia TorchCodec o DLL dekodera i pyannote o wyłączeniu TF32; Lightning informuje o adaptacji checkpointu w pamięci. Nie wykonywano sugerowanej migracji pliku ani zmian środowiska. Używana ścieżka FFmpeg z audio w pamięci zakończyła się sukcesem.

SHA-256 oryginału identyczne przed/po; nazwa i plik zachowane. Porównanie 46565 plików C:\AI\WhisperX: identyczne ścieżki, rozmiary i mtime_ns. Nie jest to pełne hashowanie instalacji. Hashe profilu i local.toml również identyczne. Bez instalacji, pobrań, drugiego venv, zapisów w źródle, nadpisywania wyników i push. Każdy wynik w nowym katalogu. Mechanizmy offline/audit hook aktywne; nie jest to systemowy audyt sieci bibliotek natywnych.

Lokalny TOML nadal wskazuje historyczny input_dir źródła; jest to domyślna lokalizacja, nie ograniczenie wyboru. Jawnie przekazany plik GUI/INPUT jest potwierdzony w run.json; output pozostaje oddzielny. Nie zmieniano lokalnej konfiguracji użytkownika.

Dowody: `C:\AI\WhisperX_GUI\runs\d3_20261014_190033` — precheck.json, source_before.json, integrity.json, run_location.json, resources.jsonl, validation.json, text_samples.json. Hashe pięciu wyników w validation.json. Diagnostyka i dane nie trafiły do Git.

## Rekomendacje i bramka etapu

Przed oceną MVP zalecany odsłuch wskazanych trzech okien, podejrzanych pożegnań, najdłuższych przerw i ostatnich sekund. Użytkownik powinien ocenić dopuszczalność końca napisów przesuniętego o 24 ms oraz interakcję GUI podczas długiego zadania. Nie ma podstaw do kolejnej pełnej transkrypcji ani zmiany modelu/parametrów bez ustalenia błędu jakościowego. Brak konieczności naprawy aplikacji ujawnionej przez ten przebieg; tolerancja 100 ms pozostaje jawnym ograniczeniem.

Definition of Done: identyfikacja, ochrona, WAV, pełny ASR/alignment, prompt, pięć artefaktów, struktura, czas i dokumentacja wykonane; jakość akustyczna i pełna ocena synchronizacji niewykonane. D3 PARTIAL, bez samodzielnego odbioru i bez rozpoczęcia D4.

Git: branch main, kod uruchomiony z f45474170fc8da67537cdd59d9eab337fd9e3c9a. Commit dokumentacyjny D3: `Document RUI pilot results and verification limits`; SHA podawane po commicie w odpowiedzi końcowej. Zmiany wyłącznie dokumentacyjne, sprawdzane przed lokalnym commitem.
