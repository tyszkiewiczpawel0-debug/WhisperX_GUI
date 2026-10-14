# KONTRAKT PROJEKTU — WHISPERX_GUI

**Wersja:** 1.0 — APPROVED  
**Data:** 14.10.2026  
**Status:** APPROVED — decyzja użytkownika z 14.10.2026  
**Projekt nadrzędny:** EKOSYSTEM  
**Repozytorium docelowe:** `C:\AI\WhisperX_GUI`  
**Repozytorium źródłowe:** `C:\AI\WhisperX`

## 1. Cel projektu

Celem projektu jest opracowanie lokalnej aplikacji GUI umożliwiającej przygotowywanie nagrań audio i wideo oraz ich transkrypcję przy wykorzystaniu WhisperX.

Aplikacja powinna uprościć proces do następującego przebiegu:

**Wybór nagrania → przygotowanie → wybór profilu i parametrów → przetwarzanie → zapis wyników.**

Projekt ma charakter narzędziowy i może w przyszłości obsługiwać różne zadania Ekosystemu, jednak pierwsza wersja pozostaje ograniczona do MVP.

Podstawowe zasady:

- Nie tworzymy ponownie funkcji, które zostały już poprawnie zaimplementowane.
- Zachowujemy niezależność repozytorium nowego projektu.
- Stosujemy istniejące standardy Ekosystemu.
- Nie ustanawiamy automatycznie nowych standardów dla pozostałych projektów.
- Rozwijamy aplikację iteracyjnie, na podstawie rzeczywistych potrzeb.

## 2. Rozdzielenie projektów

### 2.1. WHISPERX — istniejące rozwiązanie

Repozytorium `C:\AI\WhisperX` stanowi źródło wiedzy technicznej i potencjalnie wielokrotnego użytku kodu.

Dopuszcza się:

- Analizę kodu źródłowego i dokumentacji.
- Rozpoznanie istniejących skryptów transkrypcji.
- Identyfikację konfiguracji środowiska i zależności.
- Analizę istniejących metod przygotowywania nagrań.
- Wykorzystanie wybranych rozwiązań w nowym projekcie, po udokumentowaniu ich pochodzenia.

Nie dopuszcza się bez odrębnego zatwierdzenia:

- Modyfikacji kodu w repozytorium źródłowym.
- Aktualizacji WhisperX, PyTorch, CUDA lub innych zależności.
- Modyfikacji istniejącego `.venv`.
- Usuwania ani nadpisywania nagrań lub wyników.
- Wykonywania commitów lub innych zmian stanu repozytorium źródłowego.

### 2.2. WHISPERX_GUI — nowy projekt

Nowy projekt posiada własne repozytorium Git, dokumentację, kod aplikacji, konfigurację i historię zmian.

Może korzystać z istniejącego środowiska wykonawczego WhisperX, o ile discovery potwierdzi zasadność takiego rozwiązania.

Rozdzielenie repozytoriów nie oznacza obowiązku powielania środowisk Python, bibliotek ani modeli.

Sposób integracji z istniejącym WhisperX zostanie wybrany po discovery.

## 3. Etap D0 — discovery istniejącego repozytorium

**D0 jest pierwszym obowiązkowym etapem projektu.**

Celem nie jest budowa aplikacji, ale ustalenie, co już istnieje, jak działa i które rozwiązania można wykorzystać.

### Zakres rozpoznania

1. Struktura repozytorium, historia Git i aktualny stan plików.
2. Istniejące skrypty transkrypcji, w szczególności `transcribe_trip_meeting.py`, jeżeli znajduje się w repozytorium.
3. Sposób korzystania z Python API lub CLI WhisperX.
4. Przygotowywanie nagrań przez FFmpeg, w tym konwersja, próbkowanie i zachowanie osi czasu.
5. Obsługa modeli, GPU, języka, batch size i alignment.
6. Eksport wyników, formaty danych i znaczniki czasowe.
7. Obsługa błędów, logowanie i ewentualne mechanizmy wznawiania.
8. Istniejące testy, skrypty pomocnicze i udokumentowane ograniczenia.
9. Zależności środowiskowe oraz możliwości przeniesienia projektu na inny komputer.

### Zasady discovery

D0 może utworzyć katalog `C:\AI\WhisperX_GUI` oraz zapisać w nim wyłącznie dokumenty wynikowe discovery, mimo że formalna inicjalizacja Git i struktury aplikacji następuje w D1. Nie jest to zgoda na implementację GUI.

- Domyślnie wyłącznie odczyt.
- Bez instalowania i aktualizowania oprogramowania.
- Bez uruchamiania pełnych transkrypcji.
- Bez modyfikowania źródłowego repozytorium.
- Bez tworzenia nowego kodu aplikacji.
- Ustalenia muszą odróżniać fakty potwierdzone od hipotez i rekomendacji.

### Produkty D0

**DISCOVERY_REPORT.md**

Opis istniejącego rozwiązania, wykrytych komponentów, środowiska i ograniczeń.

**REUSE_MATRIX.md**

Macierz ponownego wykorzystania kodu:

| Komponent | Decyzja |
|---|---|
| Istnieje i nadaje się bez zmian | REUSE |
| Istnieje, wymaga adaptacji | ADAPT |
| Nie istnieje | BUILD |
| Istnieje, ale nie jest potrzebny w MVP | DEFER |

Dla każdego komponentu należy wskazać źródłowy plik lub mechanizm oraz uzasadnienie decyzji.

**MVP_RECOMMENDATION.md**

Rekomendacja architektury MVP, sposobu integracji z WhisperX i minimalnego zakresu nowych prac.

**Bramka D0:** użytkownik ocenia wyniki discovery i zatwierdza przejście do implementacji. Do tego momentu architektura pozostaje propozycją.

## 4. Zakres MVP

### 4.1. Interfejs graficzny

Preferowana technologia: Python + Tkinter, o ile discovery nie ujawni istotnych powodów do zmiany.

GUI obejmuje:

- Wybór pliku nagrania.
- Wyświetlenie podstawowych informacji o pliku.
- Przygotowanie materiału do transkrypcji.
- Wybór profilu przetwarzania.
- Ustawienie podstawowych parametrów.
- Rozpoczęcie i przerwanie zadania.
- Wyświetlanie statusu oraz logów.
- Dostęp do katalogu gotowych wyników.

Długotrwałe przetwarzanie nie może blokować interfejsu.

Nie wymagamy procentowego wskaźnika postępu, jeśli silnik nie udostępnia wiarygodnych danych.

### 4.2. Profile przetwarzania

Architektura musi obsługiwać profile, ale w MVP implementowany jest **jeden profil**.

**Identyfikator:** `WEBINAR_RUI_PL`  
**Nazwa:** Webinar — Rejestr Urbanistyczny PL

Proponowane parametry początkowe, do potwierdzenia podczas discovery:

| Parametr | Wartość |
|---|---|
| Model | large-v3 |
| Język | pl |
| Urządzenie | CUDA |
| Compute type | float16 |
| Batch size | 8 |
| Alignment | Włączony |
| Diarizacja | Wyłączona |

Profil przechowuje ustawienia w pliku konfiguracyjnym, niezależnym od logiki aplikacji.

Użytkownik może modyfikować udostępnione parametry pojedynczego uruchomienia. Zastosowane wartości są zapisywane z wynikami.

Zarządzanie wieloma profilami, ich importowanie i eksportowanie pozostają poza zakresem MVP.

### 4.3. Przygotowanie pliku

Aplikacja powinna:

- Rozpoznawać format i właściwości wejściowego nagrania.
- Sprawdzać dostępność wymaganych narzędzi.
- Przeprowadzać niezbędną konwersję za pomocą FFmpeg.
- Zapisywać materiał pośredni poza lokalizacją oryginału.
- Kontrolować długość nagrania i informować o istotnych rozbieżnościach.
- Zachowywać oryginalny plik bez modyfikacji.

Istniejące procedury przygotowania audio należy wykorzystać, jeżeli discovery potwierdzi ich poprawność i przydatność.

### 4.4. Przetwarzanie i wyniki

MVP obsługuje pojedyncze nagranie w jednym zadaniu.

Wymagane wyniki:

- `transcript.txt` — tekst transkrypcji.
- `transcript.srt` — napisy ze znacznikami czasu.
- `transcript.json` — strukturalne dane transkrypcji.
- `run.json` — parametry, wersje narzędzi i metadane wykonania.
- `process.log` — dziennik przetwarzania.

Każde zadanie otrzymuje odrębny katalog wynikowy.

Ponowne uruchomienie nie może niejawnie nadpisywać wcześniejszych wyników.

## 5. Pilotaż — webinar RUI z 14.10.2026

Pierwszym rzeczywistym materiałem testowym jest nagranie webinaru dotyczącego Rejestru Urbanistycznego, przeprowadzonego 14 października 2026 r.

Pilotaż obejmuje:

1. Sprawdzenie nagrania źródłowego.
2. Przygotowanie materiału do WhisperX.
3. Transkrypcję z profilem `WEBINAR_RUI_PL`.
4. Weryfikację kompletności wyników.
5. Kontrolę zgodności znaczników czasowych z nagraniem.
6. Ocenę wybranych fragmentów pod względem rozpoznawania polskiej mowy i terminologii specjalistycznej.
7. Udokumentowanie ewentualnych problemów.

Celem nie jest uzyskanie idealnej transkrypcji, ale potwierdzenie poprawnego działania całego procesu i określenie ograniczeń.

Automatyczne streszczanie webinaru, analiza prawna jego treści i przekazywanie wyników do innych projektów nie należą do MVP.

## 6. Architektura i środowisko

Projekt powinien zachować logiczny podział:

**GUI → kontroler zadania → przygotowanie audio → silnik WhisperX → eksport wyników.**

Interfejs nie powinien bezpośrednio zawierać logiki transkrypcji.

Sposób wywołania WhisperX (CLI, Python API, istniejący skrypt lub adapter) zostanie rozstrzygnięty po D0.

Zasady techniczne:

- Nie instalujemy drugiego stosu zależności bez uzasadnienia.
- Nie kopiujemy środowisk `.venv` do repozytorium.
- Ścieżki właściwe dla komputera użytkownika pozostają w lokalnej konfiguracji.
- Projekt dostarcza `.env.example` lub równoważny wzór konfiguracji.
- `README.md` opisuje uruchomienie na nowym stanowisku i lokalizację danych.
- Nagrania, wyniki, modele, cache, hasła i tokeny nie trafiają do Git.
- Dostęp do internetu, w tym pobieranie modeli, wymaga jawnego uzasadnienia i zgody, gdy jest potrzebny.
- Nie wykonujemy automatycznych zmian globalnego środowiska Windows.

## 7. Etapy realizacji

| Etap | Cel | Warunek zakończenia |
|---|---|---|
| D0 | Discovery WhisperX | Raport, macierz reuse, rekomendacja |
| D1 | Inicjalizacja repozytorium GUI | Git, minimalna struktura, dokumentacja środowiska |
| D2 | Implementacja MVP | Działające GUI i zintegrowana transkrypcja |
| D3 | Pilotaż webinaru RUI | Wyniki, testy i raport usterek |
| D4 | Ocena MVP | Decyzja o zamknięciu MVP lub dalszym rozwoju |

Każdy etap kończy się zwięzłym checkpointem i określeniem następnego kroku.

Nie mnożymy dodatkowych podetapów ani dokumentów, jeśli nie służą one kontroli ryzyka lub odtwarzalności pracy.

## 8. Kryteria akceptacji MVP

MVP można uznać za zakończone, gdy:

- Użytkownik potrafi przeprowadzić pełną transkrypcję z GUI, bez ręcznego wpisywania komend.
- Profil `WEBINAR_RUI_PL` działa i zapisuje rzeczywiście zastosowane parametry.
- Oryginalne nagranie pozostaje nienaruszone.
- Wyniki są kompletne i zapisane w przewidywalnej strukturze.
- Interfejs pozostaje responsywny podczas pracy silnika.
- Błędy są prezentowane użytkownikowi i rejestrowane.
- Można ustalić, jakimi wersjami narzędzi wykonano transkrypcję.
- Wyniki pilotażu zostały zweryfikowane, a stwierdzone ograniczenia udokumentowane.
- Repozytorium pozwala odtworzyć konfigurację i uruchomić aplikację na innym stanowisku według instrukcji.

## 9. Zasady pracy z Work

Work pełni funkcję wykonawczą i analityczną.

W ramach zatwierdzonego zadania Work może samodzielnie diagnozować zwykłe błędy techniczne, wykonywać niezbędne poprawki i ponawiać testy bez każdorazowego uzyskiwania nowego zlecenia, o ile nie przekracza zakresu, warunków STOP ani uprawnień. Nie może samodzielnie zatwierdzić własnych rezultatów ani rozpocząć kolejnego etapu D0–D4.

Może samodzielnie rozpoznawać istniejący kod, opracowywać rekomendacje, a po zatwierdzeniu zakresu wykonywać prace implementacyjne w nowym repozytorium.

Obowiązują następujące ograniczenia:

- D0 nie upoważnia do rozpoczęcia implementacji.
- Repozytorium źródłowe pozostaje chronione przed zmianami.
- Zmiany środowiska i instalacje wymagają odrębnej decyzji.
- Działania destrukcyjne, operacje na produkcyjnych danych i publikowanie repozytorium wymagają jawnej zgody.
- Commitowanie zmian w nowym repozytorium odbywa się zgodnie z przyjętym modelem pracy projektu; publikacja zdalna nie następuje automatycznie.
- Work nie ustanawia samodzielnie nowych zasad obowiązujących cały Ekosystem.
- W raportach oddziela wyniki obserwacji, problemy, rekomendacje i decyzje wymagające zatwierdzenia.

## 10. Relacja z Ekosystemem

`WHISPERX_GUI` jest niezależnym projektem podrzędnym wobec Ekosystemu.

Stosuje już przyjęte zasady prowadzenia repozytoriów, dokumentowania środowiska, checkpointów i handoffów.

`PROJECT_STANDARD_v0.2` ma status `DRAFT / PILOT` i jest materiałem referencyjnym dla organizacji repozytorium oraz sposobu pracy. Wskazanie w nim `Progman_Kadry` jako projektu pilotażowego pozostaje bez zmian i nie stanowi zadania do analizy, korekty ani dostosowania tego standardu przez `WHISPERX_GUI`. W razie rozbieżności ze szczegółowymi postanowieniami niniejszego zatwierdzonego kontraktu należy zgłosić ją użytkownikowi, bez samodzielnej zmiany standardu.

Wiedza zdobyta podczas discovery i implementacji powinna pozostać dostępna dla przyszłych projektów, szczególnie w zakresie lokalnego przetwarzania audio i integracji narzędzi AI.

Wnioski o potencjalnym zastosowaniu przekrojowym mogą zostać przekazane do projektu Ekosystem.

**Przekazanie wniosku nie oznacza automatycznego przyjęcia nowego standardu.**

---

**Decyzja otwierająca:** Pierwszym zadaniem Work jest D0 — discovery istniejącego `C:\AI\WhisperX`, bez implementacji GUI i bez modyfikacji środowiska źródłowego.