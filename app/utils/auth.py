"""
app/utils/auth.py - Autenticación con Firebase y Google OAuth
"""
from firebase_admin import auth
from fastapi import HTTPException, status
from functools import wraps
from google.auth.transport import requests
from google.oauth2 import id_token

def verify_google_token(token: str):
    """
    Verifica un JWT token de Google Sign-In
    Retorna el email (identificador único del usuario)
    """
    try:
        # ID de cliente de Google
        CLIENT_ID = "173577391295-0g8g3015bilpdnt8575j7aoaca8scsb5.apps.googleusercontent.com"
        
        # Verificar el token con Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
        # Retornar el email como identificador único
        email = idinfo.get('email')
        if not email:
            raise ValueError("El token no contiene un email válido")
        
        return email
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token de Google inválido: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error al verificar token de Google: {str(e)}"
        )

def verify_firebase_token(token: str):
    """
    Verifica un JWT token de Google (mediante Google OAuth)
    Retorna el user_id si es válido
    """
    return verify_google_token(token)

def get_user_from_token(authorization_header: str):
    """
    Extrae y verifica el token del header Authorization
    Formato: "Bearer <token>"
    """
    if not authorization_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header Authorization no proporcionado"
        )
    
    parts = authorization_header.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de Authorization inválido. Usar: Bearer <token>"
        )
    
    token = parts[1]
    return verify_firebase_token(token)
