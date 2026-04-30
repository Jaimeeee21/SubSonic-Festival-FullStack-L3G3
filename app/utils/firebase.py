"""
Configuración e inicialización de Firebase
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import os


def get_firebase_credentials_path():
    """
    Busca automáticamente el archivo de credenciales de Firebase (.json)
    en la carpeta raíz del proyecto. Soporta cualquier nombre de archivo.
    """
    root_dir = Path(__file__).parent.parent.parent

    # Buscar cualquier archivo .json que contenga 'subsonic' en el nombre
    json_files = list(root_dir.glob("*subsonic*.json"))

    if json_files:
        return json_files[0]  # Devolver el primer .json encontrado

    # Si no hay archivo con 'subsonic', buscar cualquier .json
    # (en caso de que el usuario haya renombrado el archivo)
    json_files = list(root_dir.glob("*.json"))

    if json_files:
        return json_files[0]

    # Si no encuentra nada, devolver la ruta esperada para el error
    return root_dir / "subsonic-festival-56216-3767f772323c.json"


# Obtener ruta del archivo de credenciales
CREDS_PATH = get_firebase_credentials_path()

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
    """Obtener instancia de Firestore (puede ser None si Firebase no está disponible)"""
    global _db
    if _db is None:
        init_firebase()
    return _db
