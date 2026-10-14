# Zasady pracy AI — WHISPERX_GUI

Najpierw przeczytaj `docs/PROJECT_CONTRACT.md`, `docs/CURRENT_STATE.md` i `99_HANDOFF/CURRENT/HANDOFF.md`. Kontrakt v1.0 APPROVED jest nadrzędny; `PROJECT_STANDARD_v0.2.md` jest pomocniczym DRAFT / PILOT. Nie zmieniaj standardu i nie analizuj jego projektu pilotażowego.

- `C:\AI\WhisperX` jest READ ONLY: kod, konfiguracja, .venv, nagrania, wyniki i historia pozostają chronione. Nie importuj ani nie uruchamiaj transcribe_trip_meeting.py: ma efekty uboczne przy imporcie.
- REUSE BEFORE BUILD. Korzystaj z raportów D0 i istniejącego stosu. Nie instaluj/aktualizuj zależności, nie twórz drugiego venv ani nie pobieraj modeli bez odrębnej autoryzacji. Kontroluj niejawne pobieranie NLTK/HF i zapisy cache.
- Ścieżki stanowiska należą do ignorowanego `config/local.toml`; profil jest oddzielony od logiki. Nie dodawaj danych, modeli, tokenów ani logów do Git. `.gitignore` nie zastępuje przeglądu staged diff.
- Oryginały tylko do odczytu. Każde przyszłe zadanie ma oddzielny katalog wyników; żadnego niejawnego nadpisania poprzedniego uruchomienia. Nie usuwaj ani nie nadpisuj istniejących plików użytkownika jako automatycznej naprawy.
- Etapy D0–D4 są odrębne. D0 zatwierdzono 14.10.2026; D1 obejmuje inicjalizację, dokumentację i konfiguracje. D2 (GUI/pipeline) oraz D3 (pilotaż) wymagają autoryzacji. Nie uznawaj własnego checkpointu za odbiór użytkownika ani zgodę na kolejny etap.
- Bez rozszerzania MVP o streszczenia, analizę treści, diarizację, wiele profili i kolejkę nagrań. Zwykłe decyzje wykonawcze w zatwierdzonym zakresie podejmuj samodzielnie.
- Weryfikuj proporcjonalnie: D1 — Git, ignore, składnia konfiguracji, linki, zgodność dokumentów; D2 — zachowanie implementacji, błędy, anulowanie, ochrona danych. Nie uruchamiaj silnika jako kontroli dokumentacji. Używaj `-B` dla bezpiecznej diagnostyki Python bez bytecode.
- Po istotnej zmianie aktualizuj CURRENT_STATE, DECISIONS i jeden handoff. Oddzielaj fakty, rekomendacje i niezweryfikowane założenia. Przed lokalnym commitem sprawdź zakres i dane wrażliwe, po commicie status i branch. D1 upoważnia do lokalnych commitów; brak autoryzacji na remote/push.
- STOP odpowiedniej części: sprzeczne/brakujące dokumenty, ryzyko utraty danych, konieczność modyfikacji źródła/środowiska lub wyjścia poza etap. Zgłoś konkretną przeszkodę, kontynuując niezależne dozwolone prace.
