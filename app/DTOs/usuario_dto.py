from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict, Any


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    es_empresa: bool = False
    empresa_nombre: Optional[str] = None
    empresa_cif: Optional[str] = None
    foto_perfil: Optional[str] = None  # URL de la foto de perfil o base64
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    bio: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    empresa_nombre: Optional[str] = None
    empresa_cif: Optional[str] = None
    foto_perfil: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    bio: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioPerfil(BaseModel):
    """DTO para la respuesta del perfil del usuario"""
    id: str
    nombre: str
    email: str
    foto_perfil: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    bio: Optional[str] = None
    es_empresa: bool = False
    empresa_nombre: Optional[str] = None
    empresa_cif: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
