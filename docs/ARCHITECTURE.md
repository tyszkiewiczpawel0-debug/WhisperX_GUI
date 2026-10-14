# Architektura — stan i propozycja

## Istniejące rozwiązanie

Poza repozytorium GUI działa środowisko referencyjne rozpoznane w D0: Python, WhisperX i jego zależności, lokalne modele, FFmpeg/FFprobe. Skrypt `C:\AI\WhisperX\transcribe_trip_meeting.py` zawiera przepływ load_audio → ASR → zwolnienie modelu → alignment → własny eksport. Istnieją wyniki, lecz bieżący stos nie przeszedł nowego testu wykonawczego. Dowody: [raport D0](../DISCOVERY_REPORT.md) i [macierz](../REUSE_MATRIX.md).

## Rekomendacja do realizacji w D2

Tkinter → kontroler pojedynczego zadania → FFprobe/FFmpeg → adapter Python API WhisperX w osobnym procesie → istniejące writery TXT/SRT/JSON + run.json/process.log.

- GUI: wybór pliku, podstawowe parametry, start/anulowanie, status/log, otwarcie wyników. Długie operacje poza wątkiem UI.
- Kontroler: jeden proces z istniejącego venv, komunikacja przez kolejkę/statusy, anulowanie własnego drzewa procesów, jednoznaczny stan końcowy.
- Przygotowanie: rozpoznanie strumienia i długości, mono PCM 16 kHz w obszarze zadania, bez zmiany oryginału lub usuwania ciszy.
- Adapter: adaptacja sekwencji źródłowego skryptu z udokumentowanym pochodzeniem, bez jego importu. ASR i alignment kolejno, zwalnianie zasobów, kontrola dostępności modeli i Punkt; zakaz niejawnego pobierania.
- Eksport: biblioteczne writery zamiast wadliwego srt_ts; nowy katalog na każde zadanie, walidacja kompletu i metadane rzeczywiście użytych parametrów.

CLI pozostaje technicznie dostępną alternatywą; rekomendacja API pozwala kontrolować fazy i trzy wymagane formaty. Nie wymieniać silnika ani nie kopiować środowiska. Nie budować wielu profili lub usług. Szczegóły: [rekomendacja D0](../MVP_RECOMMENDATION.md).

## Konfiguracja przygotowana w D1

`config/local.example.toml` definiuje wzór prywatnego `config/local.toml`; aplikacja jeszcze go nie czyta. `schema_version=1`. Sekcja runtime wskazuje interpreter, dwa narzędzia i trzy katalogi zasobów; allow_downloads=false opisuje wymaganą politykę, sam plik nie egzekwuje jej technicznie. D2 musi sprawdzić ścieżki, odrzucić placeholdery i mapować katalogi do właściwych API/zmiennych procesu. HF hub cache nie jest katalogiem pojedynczego snapshotu. NLTK wymaga niezależnego preflight.

Sekcja paths określa katalog startowy wyboru pliku i bazę wyników. Profil JSON `WEBINAR_RUI_PL` zawiera wyłącznie startowe parametry kontraktu; typy bool/int są natywne. D2 ma walidować konfigurację i zapisywać parametry efektywne, bez cichego fallbacku. Domyślny VAD pyannote i polski alignment są rekomendowane na podstawie istniejącego API. Żaden z powyższych komponentów aplikacji nie został zaimplementowany w D1.
