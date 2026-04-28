from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class EmpresaBase(BaseModel):
    """Base schema for Empresa"""
    nombre: str
    cif: str
    descripcion: Optional[str] = None
    telefono: str
    email_contacto: EmailStr
    website: Optional[str] = None
    logo_url: Optional[str] = None
    tipo_empresa: str  # food-truck, catering, merchandising, sponsor


class EmpresaCreate(EmpresaBase):
    """Schema for creating a new Empresa"""
    usuario_id: int


class EmpresaUpdate(BaseModel):
    """Schema for updating an Empresa"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    telefono: Optional[str] = None
    email_contacto: Optional[EmailStr] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    tipo_empresa: Optional[str] = None


class EmpresaResponse(EmpresaBase):
    """Schema for Empresa response"""
    id: int
    usuario_id: int
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmpresaPanelResponse(BaseModel):
    """Schema for Empresa panel with reservations"""
    id: int
    nombre: str
    cif: str
    descripcion: Optional[str]
    telefono: str
    email_contacto: str
    website: Optional[str]
    logo_url: Optional[str]
    tipo_empresa: str
    estado: str
    espacios_reservados: List[dict] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
