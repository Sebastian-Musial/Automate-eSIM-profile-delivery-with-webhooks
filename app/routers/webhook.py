from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session

from app.schemas import PayloadWebhook, WebhookResponse
from app.database import get_session
from app.config import Settings, get_settings
from app.services import assign_esim_profile, AssignEsimResult

router = APIRouter()

@router.post("/api/webhooks/payment", response_model=WebhookResponse, status_code=status.HTTP_200_OK, tags=["Webhooks"])
def payment_webhook(payload: PayloadWebhook, x_webhook_token: str | None = Header(default=None), settings: Settings = Depends(get_settings), session: Session = Depends(get_session) ) -> WebhookResponse:
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

    match assign_esim_profile(session, payload.order_id, payload.customer_email):
        case AssignEsimResult.ASSIGNED:
            return WebhookResponse(
                result="ASSIGNED",
                order_id=payload.order_id,
                message="Payment webhook processed and eSIM assigned"
            )
        case AssignEsimResult.DUPLICATED:      
            return WebhookResponse(
                result="DUPLICATED",
                order_id=payload.order_id,
                message="Duplicated order"
            )
        case AssignEsimResult.NOT_AVAILABLE:
            return WebhookResponse(
                result="NOT_AVAILABLE",
                order_id=payload.order_id,
                message="No available eSIM profile"
            )