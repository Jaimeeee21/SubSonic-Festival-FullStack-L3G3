from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any, Union


class EventoBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    fecha: str
    ubicacion: str
    imagen_url: Optional[str] = None
    capacidad: Optional[int] = None
    artistas: Optional[Union[Dict[str, Any], List[str]]] = None
    info: Optional[Union[List[str], str]] = None
    espacios_disponibles: Optional[List[Dict[str, Any]]] = None


class EventoCreate(EventoBase):
    id: str


class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[str] = None
    ubicacion: Optional[str] = None
    imagen_url: Optional[str] = None
    capacidad: Optional[int] = None
    artistas: Optional[Dict[str, Any]] = None
    info: Optional[List[str]] = None
    espacios_disponibles: Optional[List[Dict[str, Any]]] = None


class EventoResponse(EventoBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
