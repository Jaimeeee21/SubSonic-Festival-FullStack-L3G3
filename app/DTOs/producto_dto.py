from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: str
    imagen_default: Optional[str] = None
    colores: Optional[List[Dict[str, Any]]] = None
    stock: int = 0


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    imagen_default: Optional[str] = None
    colores: Optional[List[Dict[str, Any]]] = None
    stock: Optional[int] = None


class ProductoResponse(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
