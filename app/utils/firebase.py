"""
Configuración e inicialización de Firebase
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os

# Obtener ruta del archivo de credenciales
CREDS_PATH = Path(__file__).parent.parent.parent / "subsonic-festival-56216-firebase-adminsdk-fbsvc-fa73f8c742.json"

# Variable global para almacenar la instancia
_firebase_app = None
_db = None

def init_firebase():
    """Inicializar Firebase con credenciales"""
    global _firebase_app, _db
    
    if _firebase_app is not None:
        return  # Ya está inicializado
    
    if not CREDS_PATH.exists():
        raise FileNotFoundError(f"Archivo de credenciales no encontrado: {CREDS_PATH}")
    
    try:
        cred = credentials.Certificate(str(CREDS_PATH))
        _firebase_app = firebase_admin.initialize_app(cred)
        _db = firestore.client()
        print("[OK] Firebase initialized correctly")
    except Exception as e:
        print(f"[ERROR] Firebase initialization error: {str(e)}")
        raise

def get_firestore():
    """Obtener instancia de Firestore"""
    global _db
    if _db is None:
        init_firebase()
    return _db
