# BrainVenture: Kurs Neuroprzywództwa

## O Projekcie

BrainVenture to interaktywna platforma edukacyjna poświęcona neuroprzywództwu - podejściu do zarządzania opartemu na neurobiologii. Aplikacja umożliwia użytkownikom odkrycie własnego stylu przywództwa poprzez testy osobowości, dostęp do ustrukturyzowanego kursu oraz monitorowanie postępów w nauce.

## Funkcje

- **Dashboard**: Przegląd postępów, szybki dostęp do najważniejszych funkcji, ostatnia aktywność
- **Typy Neurolidera**: Test osobowości identyfikujący jeden z czterech typów neuroprzywódcy z opisami i rekomendacjami
- **Struktura Kursu**: Hierarchiczna struktura kursu z blokami, modułami i lekcjami
- **Profil Użytkownika**: Indywidualne statystyki, osiągnięcia, personalizacja
- **Zasoby**: Blog, artykuły, książki, badania i narzędzia wspierające naukę

## Technologia

Aplikacja została zbudowana przy użyciu następujących technologii:

- **Frontend**: Streamlit
- **Backend**: Python
- **Dane**: Struktury JSON, pliki Markdown
- **UI**: Material 3 Design (zaimplementowany w CSS)
- **Bezpieczeństwo**: Content Security Policy (CSP)

## Instalacja i uruchomienie

1. Sklonuj repozytorium:
   ```
   git clone https://github.com/your-username/brainventure.git
   cd brainventure
   ```

2. Metoda szybka (Windows):
   ```
   start_brainventure.bat
   ```
   
   lub uruchom skrypt pythonowy:
   ```
   python run_app.py
   ```

3. Metoda ręczna:
   ```
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Struktura Projektu

```
app.py                  # Główny plik aplikacji
app/                    # Moduły głównego interfejsu aplikacji
components/             # Komponenty UI wielokrotnego użytku
config/                 # Konfiguracja aplikacji, bezpieczeństwa, treści
core/                   # Główne funkcje biznesowe
data/                   # Dane aplikacji (treści kursu, testy, profile użytkowników)
docs/                   # Dokumentacja
modules/                # Funkcjonalne moduły aplikacji
pages/                  # Strony aplikacji
static/                 # Zasoby statyczne (obrazy, CSS, JS)
utils/                  # Funkcje pomocnicze
```

## Typy Neuroleaderów

1. **Neuroempata** - Lider zorientowany na ludzi i emocje
2. **Neuroinnowator** - Lider zorientowany na innowacje i twórcze rozwiązania
3. **Neuroinspirator** - Lider zorientowany na motywację i inspirację
4. **Neuroreaktor** - Lider zorientowany na działanie i efektywność

## Struktura Kursu

Kurs składa się z:
- 5 Bloków tematycznych
- 15 Modułów
- 150 Lekcji

## Licencja

Ten projekt jest udostępniany na licencji MIT.

## Autorzy

BrainVenture Team - kontakt@brainventure.com
