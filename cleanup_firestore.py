"""
Script para limpiar usuarios de prueba de Firestore
Elimina todos los usuarios excepto los que son emails válidos
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Función para encontrar credenciales de Firebase automáticamente
def get_firebase_credentials():
    root_dir = Path(__file__).parent
    json_files = list(root_dir.glob("*subsonic*.json"))
    if not json_files:
        json_files = list(root_dir.glob("*.json"))
    if json_files:
        return json_files[0]
    raise FileNotFoundError("No se encontró archivo de credenciales JSON en la carpeta raíz")

# Inicializar Firebase
creds_path = get_firebase_credentials()

if not firebase_admin._apps:
    cred = credentials.Certificate(str(creds_path))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Usuarios de prueba a eliminar (IDs que no son emails)
test_users_to_delete = [
    "108831282504798598678",  # SUB anterior
    "118168110488984175795",   # SUB anterior
    "test2_test_com",
    "testuser_example_com",
    "user_admin",
    "user_juan"
]

print("[INFO] Iniciando limpieza de Firestore...")
print(f"[INFO] Usuarios a eliminar: {test_users_to_delete}")

# Eliminar usuarios de prueba
usuarios_ref = db.collection('usuarios')

for user_id in test_users_to_delete:
    try:
        usuarios_ref.document(user_id).delete()
        print(f"[OK] Eliminado usuario: {user_id}")
    except Exception as e:
        print(f"[ERROR] No se pudo eliminar {user_id}: {str(e)}")

# Mostrar usuarios restantes
print("\n[INFO] Usuarios restantes en Firestore:")
docs = usuarios_ref.stream()

for doc in docs:
    user_data = doc.to_dict()
    email = user_data.get('email', 'N/A')
    nombre = user_data.get('nombre', 'N/A')
    print(f"  - ID: {doc.id}")
    print(f"    Email: {email}")
    print(f"    Nombre: {nombre}\n")

print("[OK] Limpieza completada!")
