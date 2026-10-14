# Dane i pochodzenie

| Warstwa | Zawartość i lokalizacja | Ochrona |
|---|---|---|
| SOURCE / RAW | Oryginalne nagranie wybrane przez użytkownika, poza Git | Tylko odczyt; bez nadpisania i bez obowiązkowej kopii dużego pliku |
| DERIVED | Przygotowany WAV 16 kHz mono w przyszłym katalogu zadania | Powiązanie z oryginałem i poleceniem przygotowania w run.json |
| WORKING | Dane częściowe w podkatalogu work zadania | Nie oznaczają sukcesu; brak automatycznego usuwania istniejących danych użytkownika |
| OUTPUT | transcript.txt, transcript.srt, transcript.json, run.json, process.log | Osobny unikatowy katalog każdego uruchomienia, poza Git |

W D1 nie utworzono katalogów nagrań/wyników ani nowych danych wykonawczych. Istniejące INPUT/OUTPUT w `C:\AI\WhisperX` pozostają nietykalne. Nie kopiujemy audio, modeli ani .venv do projektu. Preferencję standardu dotyczącą snapshotów realizujemy proporcjonalnie: bez powielania nagrania w D1; przyszłe metadane wejścia i pochodzenia zabezpieczają identyfikację, a ewentualny hash wejścia jest decyzją implementacji.

Plan provenance: wynik → wersja aplikacji/pakietów i parametry efektywne → wejście (ścieżka, rozmiar, mtime, wybrany strumień, właściwości), wersje modeli, przygotowanie, różnica długości i ostrzeżenia. run.json ma też status, czasy, etap błędu/anulowania. Istniejące wyniki D0 nie mają takiego manifestu i nie dowodzą działania nowej aplikacji.

Decyzje otwarte: lokalizacja output na stanowisku, retencja pośrednich po sukcesie/błędzie, próg różnicy długości (D0 proponuje 0.1 s), obsługa nietypowych offsetów/wielu strumieni. Do ich rozstrzygnięcia nie uruchamiać automatycznego sprzątania. Model/cache/NLTK pozostają zasobami środowiska, nie danymi repozytorium.

W Git są dokumenty, wzór konfiguracji i profil bez sekretów. Prywatny TOML, .env, media, wyniki, wagi i logi są ignorowane. Reguły ignore nie potrafią rozpoznać dowolnego sekretu w dowolnym pliku: przed commitem przegląd zawartości i listy plików jest obowiązkowy. Nie używać `git add -f` dla danych lokalnych.
