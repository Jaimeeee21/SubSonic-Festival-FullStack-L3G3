from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReservaBase(BaseModel):
    evento_id: str
    cantidad_entradas: int
    precio_total: float


class ReservaCreate(ReservaBase):
    usuario_id: int


class ReservaUpdate(BaseModel):
    estado: Optional[str] = None
    cantidad_entradas: Optional[int] = None
    precio_total: Optional[float] = None


class ReservaResponse(ReservaBase):
    id: int
    usuario_id: int
    estado: str
    fecha_reserva: datetime
    fecha_evento: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
