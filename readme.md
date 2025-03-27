<details>
  <summary>Spis treści</summary>
  <ol>
    <li>
      <a href="#o-projekcie">O projekcie</a>
      <ul>
        <li><a href="#cel-zadania-rekrutacyjnego">Cel zadania rekrutacyjnego</a></li>
        <li><a href="#informacje-dla-oceniającego">Informacje dla oceniającego</a></li>
        <li><a href="#przetwarzanie-tekstu">Przetwarzanie tekstu</a></li>
        <li><a href="#walidator-pesel">Walidator PESEL</a></li>
      </ul>
    </li>
    <li>
      <a href="#wymagania">Wymagania</a>
    </li>
    <li><a href="#instalacja">Instalacja</a></li>
  </ol>
</details>

## O projekcie

Projekt został stworzony jako zadanie rekrutacyjne.

### Cel zadania rekrutacyjnego
Stworzenie aplikacji internetowej za pomocą Django:
1. Aplikacja Django do przetwarzania tekstu
2. Walidator PESEL w aplikacji Django

### Informacje dla oceniającego
Postanowiłem utworzyć jeden główny projekt, w którym każde zadanie jest rozdzielone na osobne aplikacje:
- **Przetwarzanie tekstu** → `text_processing`
- **Walidator PESEL** → `pesel_validator`

### Przetwarzanie tekstu
Chciałbym dodać kilka słów na temat `TextProcessingForm`.
Zdaję sobie sprawę, że formularz powinien zawierać walidację rozmiaru przesłanego pliku, ale uznałem, że na razie nie jest to konieczne.

Jeśli chodzi o zapisywanie plików – zdaję sobie sprawę, że mogą one pozostawać na serwerze po przesłaniu. Można by jednak zaimplementować mechanizm czyszczenia, np. "workera", który uruchamia się raz na tydzień i usuwa stare pliki.

#### Walidator PESEL
Informacje o strukturze numeru PESEL znalazłem na stronie:
[https://dzidziusiowo.pl/niemowlak/pielegnacja-i-rozwoj/99-numer-pesel](https://dzidziusiowo.pl/niemowlak/pielegnacja-i-rozwoj/99-numer-pesel)

### Dodatkowe informacje
W projekcie wykorzystuję `pre-commit`, aby utrzymać jednolitą i spójną jakość kodu.

Napisałem również proste testy jednostkowe.

## Wymagania
- Python 3.12.9
- System operacyjny: Ubuntu

## Instalacja


1. Sklonuj repozytorium
```bash
git clone https://github.com/MatRos-sf/contelizer_task.git
```


2. Utwórz środowisko virtualne oraz zainstaluj niezbędne pakiety
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. (Opcjonalnie) Utwórz plik `.env` i podaj w nim `SECRET_KEY` oraz `DEBUG`.
Jeśli tego nie zrobisz, aplikacja sama wygeneruje klucz (zobacz `tasks/env.py`).

4. Wykonaj migracje i uruchom aplikacje
```bash
python manage.py migrate
python manage.py runserver
```
