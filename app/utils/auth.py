"""
app/utils/auth.py - Autenticación con Firebase y Google OAuth
"""
from firebase_admin import auth
from fastapi import HTTPException, status
from functools import wraps
from google.auth.transport import requests
from google.oauth2 import id_token
import base64
import json

def decode_google_token(token: str):
    """
    Decodifica un JWT de Google sin verificar la firma
    Se usa para obtener información después de que ya fue verificado
    """
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Token inválido: formato incorrecto")
        
        # Decodificar el payload (parte 2)
        payload = parts[1]
        # Agregar padding si es necesario
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        raise ValueError(f"Error decodificando token: {str(e)}")

def verify_google_token(token: str):
    """
    Verifica un JWT token de Google Sign-In
    Retorna el email (identificador único del usuario)
    Acepta AMBOS CLIENT_IDs (nuevo y antiguo) mientras se migra
    """
    try:
        # IDs de cliente de Google (nuevo y antiguo para compatibilidad)
        CLIENT_IDS = [
            "173577391295-bvsq2o87tinllnbavnolunmor3fcsg2u.apps.googleusercontent.com",  # Nuevo
            "173577391295-0g8g3015bilpdnt8575j7aoaca8scsb5.apps.googleusercontent.com"   # Antiguo (transitorio)
        ]
        
        # Intentar verificar con ambos IDs
        idinfo = None
        for client_id in CLIENT_IDS:
            try:
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
                break
            except:
                continue
        
        if idinfo is None:
            raise ValueError("Token no válido con ninguno de los CLIENT_IDs configurados")
        
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
