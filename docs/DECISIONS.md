# Decyzje — 14.10.2026

| ID | Status | Decyzja / uzasadnienie |
|---|---|---|
| D-01 | Zatwierdzone przez użytkownika | Kontrakt v1.0 APPROVED nadrzędny; D0 formalnie odebrany 14.10.2026, D1 autoryzowany w załączonym zleceniu. Brak zgody na D2 w tym zleceniu |
| D-02 | Wykonawcza D1 | Git lokalny, main, bez remote/push; obowiązujący kontrakt przeniesiony bez zmiany bajtów do docs/PROJECT_CONTRACT.md |
| D-03 | Wykonawcza D1 | Raporty D0 i standard pozostają w root jako materiały historyczne/referencyjne. Aktualny status jest w CURRENT_STATE i handoffie |
| D-04 | Wykonawcza D1 | TOML zamiast .env jako równoważny wzór; tomllib w Python 3.11 eliminuje potrzebę nowej zależności. Lokalny plik ignorowany |
| D-05 | Zlecenie D1 | Jeden profil WEBINAR_RUI_PL: large-v3/pl/cuda/float16/batch 8/alignment=true/diarization=false. Wartości startowe do testów, nie certyfikacja pipeline |
| D-06 | Rekomendacja D0 | Tkinter, osobny proces, adapter Python API, reuse venv/modeli/writerów. Dokumentacja nie traktuje tego jako zaimplementowanego rozwiązania |
| D-07 | Wykonawcza D1 | src i tests zawierają opis odpowiedzialności i plan kontroli; brak pustych modułów, klas i atrap. Manifest pakietów jest snapshotem, nie lockfile ani autoryzacją instalacji |

Przed D2: użytkownik odbiera D1 i autoryzuje implementację, rozstrzyga proponowany wariant integracji, politykę pośrednich/próg długości oraz zakres dozwolonych testów wykonawczych. Nie wymagają ponownego rozstrzygania drobne decyzje organizacyjne już objęte D1. Brak modeli/zależności w późniejszej weryfikacji wymaga osobnej decyzji o instalacji/pobraniu, a nie automatycznej naprawy. D3 wymaga dostarczenia nagrania RUI i autoryzacji pilotażu.
