from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session

from app.schemas import PayloadWebhook, WebhookResponse
from app.database import get_session
from app.config import settings
from app.services import assign_esim_profile

router = APIRouter()

@router.post("/api/webhooks/payment", response_model=WebhookResponse, status_code=status.HTTP_200_OK, tags=["Webhooks"])
def payment_webhook(payload: PayloadWebhook, x_webhook_token: str | None = Header(default=None), session: Session = Depends(get_session) ) -> WebhookResponse:
    if (x_webhook_token != settings.webhook_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong webhook token",
        )
    
    if (payload.status.strip().upper() != "COMPLETED"):
            return WebhookResponse(
                result="IGNORED",
                order_id=payload.order_id,
                message="Payment is not completed. Wrong payment status"
            )

    if (assign_esim_profile(session, payload.order_id, payload.customer_email)): #Template dla funkcji w service.py która będzie wykonywała logikę biznesową - chce aby funkcja zwracała wartość bool aby potwierdzić wykonanie
        return WebhookResponse(
            result="ASSIGNED",
            order_id=payload.order_id,
            message="Payment webhook processed and eSIM assigned"
        )
    else:         
        return WebhookResponse( # W przypadku braku wolnych profili oraz w przypadku zdublowania się zamówień prder_id
            result="IGNORED",
            order_id=payload.order_id,
            message="TEMPLATE WRONG"
        )