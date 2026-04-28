from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ReservaEspacioBase(BaseModel):
    tipo_espacio: str
    nombre_espacio: str
    tamaño: str
    descripcion: Optional[str] = None
    nombre_negocio: str
    precio: float
    ubicacion_ideales: Optional[List[str]] = None
    servicios_requiere: Optional[List[str]] = None


class ReservaEspacioCreate(ReservaEspacioBase):
    usuario_id: int


class ReservaEspacioUpdate(BaseModel):
    estado: Optional[str] = None
    nombre_negocio: Optional[str] = None
    precio: Optional[float] = None
    ubicacion_ideales: Optional[List[str]] = None
    servicios_requiere: Optional[List[str]] = None


class ReservaEspacioResponse(ReservaEspacioBase):
    id: int
    usuario_id: int
    estado: str
    fecha_reserva: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
