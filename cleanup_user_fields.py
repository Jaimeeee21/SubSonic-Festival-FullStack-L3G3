"""
Script para limpiar el usuario: eliminar creado_en, dejar solo created_at
y asegurar que existe entradas_compradas
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Inicializar Firebase
creds_path = Path(__file__).parent / "subsonic-festival-56216-3767f772323c.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(str(creds_path))
    firebase_admin.initialize_app(cred)

db = firestore.client()

usuario_id = "suarezpitel_gmail_com"

print(f"[INFO] Limpiando usuario: {usuario_id}")

try:
    # Obtener el usuario
    doc = db.collection('usuarios').document(usuario_id).get()
    
    if not doc.exists:
        print(f"[ERROR] Usuario no encontrado")
    else:
        usuario = doc.to_dict()
        print(f"[INFO] Usuario actual:")
        for key, value in usuario.items():
            print(f"  {key}: {value}")
        
        # Eliminar creado_en si existe
        if 'creado_en' in usuario:
            db.collection('usuarios').document(usuario_id).update({
                'creado_en': firestore.DELETE_FIELD
            })
            print(f"[OK] Eliminado campo 'creado_en'")
        
        # Asegurar que existe entradas_compradas
        if 'entradas_compradas' not in usuario:
            db.collection('usuarios').document(usuario_id).update({
                'entradas_compradas': []
            })
            print(f"[OK] Agregado campo 'entradas_compradas: []'")
        else:
            print(f"[INFO] El usuario ya tiene 'entradas_compradas'")
        
        # Mostrar usuario actualizado
        doc = db.collection('usuarios').document(usuario_id).get()
        print(f"\n[INFO] Usuario actualizado:")
        usuario_actualizado = doc.to_dict()
        for key, value in usuario_actualizado.items():
            print(f"  {key}: {value}")

except Exception as e:
    print(f"[ERROR] {str(e)}")

print("[OK] Proceso completado!")
