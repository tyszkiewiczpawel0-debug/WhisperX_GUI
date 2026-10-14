# Bieżący stan — 14.10.2026, po D2

**D2: COMPLETE w zakresie wykonawczym, do formalnego odbioru użytkownika. D0 i D1 zatwierdzone w zleceniu D2. D3 nie rozpoczęto.**

Poprawka pierwszego uruchomienia (14.10.2026): odtworzono ParserError wynikający z UTF-8 bez BOM czytanego przez Windows PowerShell 5.1/CP1250. Launcher jest teraz ASCII, konfiguracja jawnie UTF-8, błędy startu pozostają w konsoli z kodem 1. Rzeczywista ścieżka Start.cmd → Start.ps1 → GUI przeszła test z wizualnym sprawdzeniem okna i zamknięciem (kod 0), podobnie ścieżka z polskimi znakami/spacjami. Brak/błędy konfiguracji i brak interpretera — PASS. Poprawka gotowa do ponownego odbioru D2; nie rozpoczęto D2.1 ani D3. Silnika i środowiska nie zmieniano, testów GPU nie powtarzano. Szczegóły w początkowej sekcji raportu testów.

Istnieje działające GUI Tkinter z wyborem nagrania, metadanymi, profilem, parametrami, przygotowaniem WAV, transkrypcją, alignmentem, etapami/logiem, anulowaniem i otwieraniem wyników. Silnik działa w osobnym procesie istniejącego środowiska. Każda operacja ma unikatowy katalog, manifest i log. Transkrypcja używa bibliotecznych eksporterów TXT/SRT/JSON.

Potwierdzono: 11 testów logiki/integracji, rzeczywiste eksportery i przeniesienie znaczników minut/godzin, blokadę sieci i zapisów poza zadaniem, anulowanie potomnego FFmpeg oraz rzeczywistego ASR/alignmentu, responsywność Tkinter. Dwa pełne przebiegi 20 s PL na RTX 5070 Ti, large-v3/float16/batch 8, alignment PL: succeeded, 2 segmenty/58 słów. Ostatni 23,766 s; to pomiar próbki, nie benchmark.

Ostrzeżenie TorchCodec pozostaje w logu/manifeście, lecz nie blokuje używanego dekodowania FFmpeg. Brak testu CPU/innych compute, długich nagrań, jakości i synchronizacji RUI oraz drugiego stanowiska. Ochrona offline obejmuje mechanizmy bibliotek i audit hook Python, nie systemowy firewall kodu natywnego.

Źródło bez zmian: porównanie ścieżka/rozmiar/mtime_ns wszystkich 46565 plików przed/po D2 identyczne. Kontrakt i standard mają pierwotne SHA256. Brak instalacji, pobierania, zmian źródła i push. Dane i lokalna konfiguracja są ignorowane. Wyniki szczegółowe: [raport](D2_TEST_REPORT.md), [handoff](../99_HANDOFF/CURRENT/HANDOFF.md).

Start: dwuklik Start.cmd; lokalny TOML gotowy. Następny krok: użytkownik odbiera D2 i oddzielnie autoryzuje D3. Nie rozpoczęto pilotażu RUI ani nie uznano checkpointu za odbiór.
