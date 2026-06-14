from enum import StrEnum
from sqlmodel import Session, select
from datetime import datetime

from app.models import EsimProfile, EsimStatus

class AssignEsimResult(StrEnum):
    NOT_AVAILABLE = "NOT_AVAILABLE"
    DUPLICATED = "DUPLICATED"
    ASSIGNED = "ASSIGNED"

def assign_esim_profile(session: Session, order_id: str, customer_email: str) -> AssignEsimResult:
    #Duplikacja
    profil_assigned = session.exec(
        select(EsimProfile).where(EsimProfile.assigned_order_id == order_id)   
    ).first()
    if profil_assigned is not None:
        return AssignEsimResult.DUPLICATED
    
    #Wolny profil
    profil_ava = session.exec(
        select(EsimProfile).where(EsimProfile.status == EsimStatus.AVAILABLE).order_by(EsimProfile.id).limit(1)
    ).first()
    if profil_ava is None:
        return AssignEsimResult.NOT_AVAILABLE
    
    profil_ava.status = EsimStatus.ASSIGNED
    profil_ava.assigned_order_id = order_id
    profil_ava.assigned_at = datetime.now()

    session.commit()

    print("Wyslane na adres: " + customer_email)
    print("\nWitam," \
    "\nPonizej kod QR dla zamowienia " + order_id + " twojego pakietu danych eSIM dla podroznych")
    print(profil_ava.qr_image_url)
    print("Dziekujemy za zakup\n")

    return AssignEsimResult.ASSIGNED