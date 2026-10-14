# Weryfikacja

D1: kontrole Git/ignore, parsowanie JSON/TOML standardową biblioteką, zgodność parametrów profilu, odwołań dokumentów, zachowania kontraktu i zakresu śledzonych plików. Polecenia do powtórzenia znajdują się w [README](../README.md). Nie ma jeszcze wykonywalnych testów aplikacji, więc nie deklarujemy przejścia pipeline.

Po autoryzacji D2 tworzyć testy rzeczywistych ryzyk: odrzucanie niepoprawnej konfiguracji, brak nadpisania wyników, stany błędu/anulowania, granice czasu SRT 59.9996/3599.9996, kompletność pięciu artefaktów, brak pobrań przy brakujących zasobach. Testy danych syntetycznych nie powinny wymagać nowych zależności ani zapisywać do źródłowego WhisperX.

Osobno zatwierdzone testy integracyjne: preflight modeli/VAD/Punkt offline, ASR+alignment na krótkiej próbce PL, VRAM batch 8, anulowanie FFmpeg/ASR/alignmentu i brak osieroconych procesów, responsywność GUI, pliki ze spacjami/polskimi znakami, różnice długości i strumienie audio/wideo. D3: pełny webinar RUI i odsłuch początku/środka/końca. Żadnego z tych testów silnika nie wykonano w D1.
