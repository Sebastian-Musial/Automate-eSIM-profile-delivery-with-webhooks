# Automatyzacja dostawy profili eSIM przez Webhooks

Aplikacja serwerowa automatyzyjąca wydawanie profili eSIM w postaci kodów QR na podstawie powiadomień od zewnętrznego operatora z informacją o udanej transakcji. 

# Jak uruchomić

# 

# 

# Dane wejściowe od zewnętrznego operato o udanej transakcji (Payload)

Poniżej przykład powiadomienia:

{
  "event": "payment.updated",
  "order_id": "ORD-2026-99431",
  "customer_email": "student@example.com",
  "status": "COMPLETED",
  "amount": 49.99,
  "currency": "PLN"
}
