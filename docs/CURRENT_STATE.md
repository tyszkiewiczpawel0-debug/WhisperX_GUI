# Bieżący stan — 14.10.2026, po D2.1

**D2.1: COMPLETE wykonawczo, do odbioru użytkownika. D2 formalnie zatwierdzony w zleceniu D2.1. D3 nie rozpoczęto i wymaga odrębnej autoryzacji.**

MVP obsługuje opcjonalny initial_prompt z profilu JSON, edytowalny w wielowierszowym polu GUI dla uruchomienia. Profil pozostaje niezmieniony; dostarczona wartość jest pusta. Brak/null/pusty tekst/białe znaki oznaczają brak promptu. Pozostały tekst przechodzi bez zmian przez kontroler i adapter do load_model/asr_options lokalnego WhisperX 3.8.6.

run.json odróżnia konfigurację (parameters.initial_prompt) od wartości potwierdzonej po load_model (initial_prompt + initial_prompt_state). Błąd/anulowanie przed ASR nie deklaruje użycia promptu; przerwanie ładowania pozostawia submission_unconfirmed. Nie dopisujemy pełnego promptu do process.log. Pozostałe parametry i architektura D2 zachowane.

Weryfikacja: 16/16 testów PASS (11 D2 + 5 ukierunkowanych z podprzypadkami), rzeczywisty widget Tkinter i niezmienność profilu, błędy/anulowanie, dokładne przekazanie i JSON. Jeden pełny przebieg lokalnej próbki D2 20 s z promptem: succeeded, 6 segmentów, 25,047 s, komplet wyników. Składnia Python i granice układu widocznego GUI 940x810/760x680 — PASS. Launchery niezmienione; wcześniejsze testy uruchomienia opisano w raporcie D2.

Ochrona źródła: przed/po identyczne ścieżki, rozmiary i mtime_ns wszystkich 46565 plików C:\AI\WhisperX. SHA256 próbki również identyczne. Nie jest to pełne hashowanie instalacji. Bez zmian środowiska, instalacji, pobierania, nadpisywania wcześniejszych wyników i push. Dane testowe oraz lokalny TOML poza Git.

Ograniczenia: nie oceniano jakości terminologii RUI, pełnego webinaru, CPU/innych compute ani długiego materiału. Nie powtarzano macierzy kosztownych testów GPU. Ostrzeżenie TorchCodec nadal nie blokuje używanego dekodowania. Ręczny odbiór wyglądu należy do użytkownika.

Start: dwuklik Start.cmd. Kolejny krok: odbiór D2.1 i osobna autoryzacja D3 ze wskazaniem webinaru oraz ewentualnego promptu terminologicznego. Gotowość techniczna do takiego pilotażu, bez samodzielnego jego rozpoczęcia.

[Raport D2.1](D2_1_TEST_REPORT.md), [raport D2](D2_TEST_REPORT.md), [decyzje](DECISIONS.md), [checkpoint](../99_HANDOFF/CURRENT/HANDOFF.md).
