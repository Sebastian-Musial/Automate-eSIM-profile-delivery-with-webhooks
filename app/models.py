from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime

#ENUM
class EsimStatus(str, Enum):
    AVAILABLE  = "available"
    ASSIGNED = "assigned"


class EsimProfile(SQLModel, table=True):
    __tablename__ = "esim_profiles"

    id: int | None = Field(default=None, primary_key=True)
    qr_code_value: str 
    qr_image_url: str 
    status: EsimStatus = Field(default=EsimStatus.AVAILABLE)
    assigned_order_id: str | None = Field(default=None)
    assigned_at: datetime | None = Field(default=None)