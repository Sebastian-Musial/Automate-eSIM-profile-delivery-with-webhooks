# Automatyzacja dostawy profili eSIM przez Webhooks - opis programu

Aplikacja serwerowa automatyzująca wydawanie profili eSIM w postaci kodów QR na podstawie powiadomień od zewnętrznego operatora z informacją o udanej transakcji. 
Głównym celem aplikacji jest zautomatyzowanie procesu biznesowego opierającego się na weryfikacji powiadomień które są otrzymywane od zewnętrznego systemu płatności w formie powiadomienia o zrealizowanej płatności, przydzieleniu wolnego profilu eSIM do zamówienia i wysłania powiadomienia e-mail.

Weryfikacja płatności jest realizowana według wyznaczonych wytycznych:
- Weryfikacja tokena w nagłówku X-Webhook-Token - zabezpieczenie endpointu przed fałszywimi żądaniami 
- Weryfikacja statusu płatności - status musi mieć wartość COMPLETED. Walidacja uwzględnia korzystanie z małych i dużych liter
- Zamówienie może być przypisane tylko do jednego jednocześnie profilu eSim
- Przed realizacją zamówienia weryfikowana jest dostępność profili eSIM - W przypadku braku wolnego zamówienie nie jest realizowane i wysyłany jest stosowny komunikat do systemu płatności.
- W przypadku realizacji zamówienia wysyłane jest powiadomienie e-mail wraz z kodem QR. Ze względu na aspekt symulacyjny powiadomienie jest wyświetlane w konsoli wraz z lokalizacją pliku graficznego z wygenerowanym kodem QR

W ramach aplikacji został przygotowany też skrypt tworzący 5 nowych rekordów z wolnymi profilami eSim oraz na podstawie danych z nowoutworzonych profili eSim generowane są jednocześnie pliki graficzne z zakodowaną informacją o profilu w formie kodu QR. Pliki graficzne z generowanymi kodami QR są zapisywane w folderze static/qrcodes. Każdy plik graficzny jest przypisany do swojego indywidualnego rekordu w bazie danych.



## Logika biznesowa

Aplikacja dostarcza profil eSIM tylko gdy otrzyma status COMPLETED od zewnętrznego operatora transakcji przy czym:
- Walidowane są poprawnie też znaki o innej wielkości liter. Aplikacja sama podczas sprawdzenia zamienia wszystkie znaki na duże w celu sprawdzenia czy uzyskamy słowo COMPLETED
- Pole ze statusem zamówienia jest odbierane jako string jako założenie że nie otrzymaliśmy listy dostępnych statusów od operatora. W przypadku gdyby taka lista była pole powinno być odbierane jako enum z wcześniej utworzoną listą wyliczeniową z wszystkimi możliwymi statusami



## Schemat działania 

1. Przyjmij powiadomienie od zewnętrznego systemu.
2. Sprawdź, czy żądanie jest autentyczne - Sprawdź nagłówek X-Webhook-Token.
3. Jeżeli token niepoprawny -> odrzuć żądanie i wyślij odpowiedź do systemu płatności.
4. Sprawdź status płatności.
5. Jeżeli status != COMPLETED -> nic nie przydzielaj, ignoruj żądanie i wyślij odpowiedź do systemu płatności.
6. Sprawdź, czy istnieje już profil eSIM przypisany do danego `order_id` -> nic nie przydzielaj, ignoruj żądanie i wyślij odpowiedź do systemu płatności.
7. Pobierz jeden wolny profil eSIM.
8. Oznacz go jako ASSIGNED.
9. W konsoli wypisz symulacyjny e-mail z kodem QR:
10. Wyślij odpowiedź do systemu płatności o poprawnej realizacji zamówienia



## Jak uruchomić

1. Utwórz .env na podstawie .env.example
2. Uruchom Postgresa: docker compose up -d
3. Utwórz i aktywuj venv
    - python -m venv .venv
    - .venv\Scripts\activate.bat - dla windows aktywacja środowiska w CMD
    - source .venv/bin/activate - dla Linux to samo
4. Zainstaluj zależności: pip install -r requirements.txt
5. Uruchom API: python -m uvicorn app.main:app --reload
6. W celu dodania 5 przykładowych rekordów do bazy oraz wygenerowania dla nich kodów QR: python -m app.seed



## Skrypt seed ładujący bazę danych przykładowymi 5 rekordami i generujący kody QR

Skrypt ten tworzy 5 rekordów i generuje 5 plików graficznych .png które są zapisywane w katalogu static/qrcodes.
Każde wywołanie tworzy nowe dane. W przypadku potrzeby wykasowania bazy danych i postawienia jej na nowo w dockerze wymagane jest ręcznie wykasowanie plików graficznych z kodem QR w folderze static/qrcodes.



## Podgląd bazy danych poprzez wejście do bazy danych przez dockera

1. Weryfikacja nazwy kontenera w dockerze: docker ps

2. Polecenie w celu wejścia do kontenera (NAZWA_KONTENERA - sprawdzamy przez docker ps, example_user i example_db - sprawdzamy w .env) docker exec -it NAZWA_KONTENERA psql -U example_user -d example_db 

3. Polecenie SQL w celu wypisania tabeli
  SELECT id, qr_code_value, qr_image_url, status, assigned_order_id, assigned_at
  FROM esim_profiles
  ORDER BY id;

## TEST webhook za pomocą curl

curl -X POST "http://127.0.0.1:8000/api/webhooks/payment" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Token: SecretToken123" \
  -d '{
    "event": "payment.updated",
    "order_id": "ORD-2026-99431",
    "customer_email": "student@example.com",
    "status": "COMPLETED",
    "amount": 49.99,
    "currency": "PLN"
  }'



## Przydatne komendy podczas pracy z projektem oraz adres dokumentacji 

  python -m venv .venv

  .venv\Scripts\activate.bat - dla windows aktywacja środowiska w CMD
  source .venv/bin/activate - dla Linux to samo

  docker compose up -d
  docker compose down -v

  uvicorn app.main:app --reload

  http://127.0.0.1:8000/docs
  http://127.0.0.1:8000/health

  docker ps

  docker exec -it NAZWA_KONTENERA psql -U example_user -d example_db

  SELECT id, qr_code_value, qr_image_url, status, assigned_order_id, assigned_at
  FROM esim_profiles
  ORDER BY id;



## Dane wejściowe od zewnętrznego operatora o udanej transakcji (Payload)

Poniżej przykład powiadomienia:

{
  "event": "payment.updated",
  "order_id": "ORD-2026-99431",
  "customer_email": "student@example.com",
  "status": "COMPLETED",
  "amount": 49.99,
  "currency": "PLN"
}
