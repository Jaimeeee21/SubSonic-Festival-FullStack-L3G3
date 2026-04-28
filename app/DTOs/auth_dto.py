from pydantic import BaseModel
from typing import Optional


class LoginResponse(BaseModel):
    """Response schema for login"""
    user_id: str
    success: bool
    message: str
    es_empresa: Optional[bool] = False
    empresa_id: Optional[int] = None


class VerifyTokenResponse(BaseModel):
    """Response schema for token verification"""
    valid: bool
    user_id: Optional[str] = None
    es_empresa: Optional[bool] = False
    empresa_id: Optional[int] = None
