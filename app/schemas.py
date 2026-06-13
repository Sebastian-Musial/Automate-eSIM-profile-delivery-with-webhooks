from sqlmodel import SQLModel
from decimal import Decimal

class PayloadWebhook(SQLModel):
    event: str                                    #"payment.updated"
    order_id: str                                 #"ORD-2026-99431"
    customer_email: str                           #"student@example.com"
    status: str                                   #"COMPLETED"
    amount: Decimal                               #49.99
    currency: str                                 #"PLN"

class WebhookResponse(SQLModel):
    result: str
    order_id: str
    message: str