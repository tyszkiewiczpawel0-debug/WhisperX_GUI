# WHISPERX_GUI

Lokalny interfejs przygotowania audio/wideo i transkrypcji przez istniejący WhisperX. MVP obejmuje jedno nagranie, profil WEBINAR_RUI_PL oraz TXT, SRT, JSON, metadane uruchomienia i log. Nie obejmuje streszczania ani analizy treści.

**D0 zatwierdzony przez użytkownika 14.10.2026. D1 przygotowany do odbioru. GUI i pipeline nie są zaimplementowane; nie istnieje jeszcze polecenie uruchamiające aplikację. D2 nie rozpoczęto.**

## Mapa i źródła prawdy

- [Kontrakt v1.0 APPROVED](docs/PROJECT_CONTRACT.md) — jedyna obowiązująca kopia, przeniesiona bez zmiany treści.
- [Standard v0.2](PROJECT_STANDARD_v0.2.md) — pomocniczy DRAFT / PILOT, bez zmian.
- [Stan](docs/CURRENT_STATE.md), [architektura](docs/ARCHITECTURE.md), [dane](docs/DATA.md), [decyzje](docs/DECISIONS.md).
- [Raport D0](DISCOVERY_REPORT.md), [reuse](REUSE_MATRIX.md), [rekomendacja](MVP_RECOMMENDATION.md) — historyczne raporty, aktualny status zatwierdzenia w CURRENT_STATE. Stare ścieżki kontraktu w D0 opisują stan sprzed przeniesienia.
- [AGENTS.md](AGENTS.md) — zasady bezpiecznej pracy AI.
- [config/local.example.toml](config/local.example.toml) — wzór stanowiska; [profil](config/WEBINAR_RUI_PL.json).
- [src/](src/README.md) — miejsce przyszłego kodu; [tests/](tests/README.md) — plan weryfikacji.
- [Checkpoint](99_HANDOFF/CURRENT/HANDOFF.md) — punkt wejścia do dalszej pracy.
- [Snapshot pakietów](docs/ENVIRONMENT_PACKAGES.txt) — odczyt metadanych, nie przetestowany lockfile.

## Obecne stanowisko

D0 wykazało Python 3.11.9, WhisperX 3.8.6, PyTorch 2.8.0+cu128, FFmpeg/FFprobe 8.1.2 i RTX 5070 Ti. Interpreter: `C:\AI\WhisperX\.venv\Scripts\python.exe`. Tkinter importuje się. Pełny pipeline GPU/offline i batch 8 nie zostały zweryfikowane.

W D2 planowane jest użycie istniejącego interpretera i modeli przez adapter API w osobnym procesie. Nie kopiować .venv ani nie uruchamiać starego skryptu. Źródłowy katalog WhisperX pozostaje READ ONLY.

Przed przyszłym uruchomieniem skopiuj wzór do `config/local.toml` tylko jeśli taki plik jeszcze nie istnieje, po czym uzupełnij ścieżki. D1 nie tworzy prywatnej konfiguracji i nie ma jeszcze jej czytnika. TOML jest równoważnikiem `.env.example`; Python 3.11 ma `tomllib`, więc nie potrzeba nowego pakietu dotenv. Nie stosujemy automatycznej interpolacji zmiennych ani `~`; podawaj pełne ścieżki.

Znane lokalizacje z D0: narzędzia FFmpeg/FFprobe w `C:\Users\tyszk\AppData\Local\Microsoft\WinGet\Links`, HF hub w `C:\Users\tyszk\.cache\huggingface\hub`, torch home w `C:\Users\tyszk\.cache\torch`, NLTK w `C:\Users\tyszk\AppData\Roaming\nltk_data`. To dane dokumentacyjne stanowiska, nie stałe przyszłej aplikacji. Input może wskazywać katalog nagrań do odczytu. Output wybierz poza źródłem WhisperX i oryginałami, np. `C:\AI\WhisperX_GUI_results` (przykład; D1 go nie tworzy).

## Uruchomienie na nowym stanowisku

1. Pobierz lokalną kopię repozytorium, np. `git clone <ścieżka-do-lokalnego-repo> <katalog-docelowy>`. D1 nie konfiguruje hostingu ani remote. Sprawdź branch `main` i checkpoint.
2. Sprawdź dostępny Windows, Python 3.11 z Tkinter, FFmpeg/FFprobe oraz sprzęt i sterownik NVIDIA dla wybranego stosu CUDA. Wersje z D0 są punktem odniesienia, nie gwarancją kompatybilności innego komputera.
3. Jeśli istnieje odpowiednie środowisko WhisperX, wskaż je. Jeżeli go brak, odtworzenie wymaga osobno zatwierdzonej instalacji: Python/venv, właściwe wydania torch/torchaudio/torchvision cu128 oraz pozostałe pakiety według snapshotu. Snapshot nie ustala źródeł wheel, hashy ani dostępności wydań; nie uruchamiaj go ślepo przez pip. Plan instalacji i źródła dystrybucji należy sprawdzić przed wykonaniem. D1 nie instaluje ani nie obiecuje zakończonego testu odtworzenia.
4. Zapewnij lokalne zasoby ASR Systran/faster-whisper-large-v3, alignment jonatasgrosman/wav2vec2-large-xlsr-53-polish, VAD pyannote z pakietu oraz NLTK Punkt PL. Rewizje i zawartość opisuje raport D0. Modele pozyskaj z autoryzowanego lokalnego zasobu lub przez osobno zatwierdzone pobranie; nie są w Git. Nie kopiuj .venv z innego stanowiska.
5. Przygotuj `config/local.toml` z wzoru; wskaż nagrania i odrębny katalog wyników. Nagranie pilotażowe RUI dostarcza użytkownik; w D0 nie znaleziono go w INPUT.
6. W D1 nie uruchomisz GUI. Po implementacji D2 instrukcja zostanie uzupełniona o rzeczywisty entry point. Nie zastępuj go uruchomieniem skryptu źródłowego.
7. Teraz wykonaj kontrole poniżej. Po zatwierdzeniu testów D2/D3 sprawdź dodatkowo ładowanie offline, krótką próbkę PL, eksporty, anulowanie i synchronizację. Do tego czasu pełne uruchomienie nowego stanowiska pozostaje nieweryfikowane.

## Weryfikacja bieżącego stanu

W katalogu repozytorium:

```powershell
git status --short
git branch --show-current
git log -2 --oneline
git remote -v
git diff --check
git check-ignore .venv/pyvenv.cfg .env config/local.toml INPUT/test.wav runs/test/run.json
```

Status powinien być pusty, branch `main`, remote pusty. `check-ignore` powinien wypisać chronione ścieżki. Sprawdź także, że wzór konfiguracji, profil i dokumentacja pozostają wersjonowane (`git ls-files`). Składnia konfiguracji, bez silnika i bez zapisów:

```powershell
& 'C:\AI\WhisperX\.venv\Scripts\python.exe' -I -B -c "import json,tomllib,pathlib; print(json.loads(pathlib.Path('config/WEBINAR_RUI_PL.json').read_text(encoding='utf-8'))['id']); tomllib.loads(pathlib.Path('config/local.example.toml').read_text(encoding='utf-8')); print('TOML OK')"
```

Na innym stanowisku zastąp ścieżkę interpretera. Te kontrole potwierdzają przygotowanie repozytorium, nie działanie transkrypcji. Zakres późniejszych testów opisuje [tests/README.md](tests/README.md).
