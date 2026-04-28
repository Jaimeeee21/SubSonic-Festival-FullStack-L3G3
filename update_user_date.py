"""
Script para actualizar el usuario antiguo con created_at
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from datetime import datetime

# Inicializar Firebase
creds_path = Path(__file__).parent / "subsonic-festival-56216-3767f772323c.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(str(creds_path))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Usuario antiguo a actualizar
usuario_id = "suarezpitel_gmail_com"

print(f"[INFO] Actualizando usuario: {usuario_id}")

try:
    # Obtener el usuario
    doc = db.collection('usuarios').document(usuario_id).get()
    
    if not doc.exists:
        print(f"[ERROR] Usuario no encontrado")
    else:
        usuario = doc.to_dict()
        print(f"[INFO] Usuario actual: {usuario}")
        
        # Verificar si tiene created_at
        if 'created_at' not in usuario:
            # Asignar una fecha (puedes cambiar esto a la fecha real)
            usuario['created_at'] = datetime.now()
            
            # Actualizar en Firestore
            db.collection('usuarios').document(usuario_id).update({
                'created_at': usuario['created_at']
            })
            
            print(f"[OK] Agregado created_at al usuario")
        else:
            print(f"[INFO] El usuario ya tiene created_at: {usuario['created_at']}")
        
        # Mostrar el usuario actualizado
        doc = db.collection('usuarios').document(usuario_id).get()
        print(f"\n[INFO] Usuario actualizado:")
        print(f"  Email: {doc.to_dict().get('email')}")
        print(f"  Nombre: {doc.to_dict().get('nombre')}")
        print(f"  Creado en: {doc.to_dict().get('created_at')}")

except Exception as e:
    print(f"[ERROR] {str(e)}")

print("[OK] Proceso completado!")
