#!/usr/bin/env python3
"""
Script de diagnóstico para probar conexión a Firestore
"""
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from datetime import datetime

CREDS_PATH = Path(__file__).parent / "subsonic-festival-56216-firebase-adminsdk-fbsvc-fa73f8c742.json"

print("=" * 60)
print("🔍 DIAGNÓSTICO DE FIRESTORE")
print("=" * 60)

# 1. Verificar que el archivo existe
print("\n1️⃣ Verificando archivo de credenciales...")
if CREDS_PATH.exists():
    print(f"   ✅ Archivo encontrado: {CREDS_PATH}")
else:
    print(f"   ❌ Archivo NO encontrado: {CREDS_PATH}")
    exit(1)

# 2. Cargar credenciales
print("\n2️⃣ Cargando credenciales...")
try:
    cred = credentials.Certificate(str(CREDS_PATH))
    print(f"   ✅ Credenciales cargadas")
except Exception as e:
    print(f"   ❌ Error al cargar credenciales: {e}")
    exit(1)

# 3. Inicializar Firebase
print("\n3️⃣ Inicializando Firebase Admin SDK...")
try:
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(f"   ✅ Firebase inicializado correctamente")
except Exception as e:
    print(f"   ❌ Error al inicializar Firebase: {e}")
    exit(1)

# 4. Intentar escribir un documento de prueba
print("\n4️⃣ Intentando escribir documento de prueba...")
try:
    test_data = {
        'test': True,
        'timestamp': datetime.utcnow().isoformat(),
        'mensaje': 'Prueba de conexión'
    }
    db.collection('_test_diagnostico').document('test-doc').set(test_data)
    print(f"   ✅ Documento escrito exitosamente")
except Exception as e:
    print(f"   ❌ Error al escribir: {str(e)}")
    print(f"   Tipo de error: {type(e).__name__}")

# 5. Intentar leer el documento
print("\n5️⃣ Intentando leer documento de prueba...")
try:
    doc = db.collection('_test_diagnostico').document('test-doc').get()
    if doc.exists:
        print(f"   ✅ Documento leído: {doc.to_dict()}")
    else:
        print(f"   ❌ Documento no encontrado")
except Exception as e:
    print(f"   ❌ Error al leer: {str(e)}")

# 6. Intentar escribir en colección reservas_espacios
print("\n6️⃣ Intentando escribir en 'reservas_espacios'...")
try:
    reserva_data = {
        'id': 'test-123',
        'usuario_id': 999,
        'evento_id': 'madrid',
        'nombre_espacio': 'Test',
        'estado': 'confirmada',
        'fecha_reserva': datetime.utcnow().isoformat()
    }
    db.collection('reservas_espacios').document('test-reserva').set(reserva_data)
    print(f"   ✅ Reserva de prueba escrita")
except Exception as e:
    print(f"   ❌ Error al escribir reserva: {str(e)}")
    print(f"   Tipo de error: {type(e).__name__}")

print("\n" + "=" * 60)
print("✅ DIAGNÓSTICO COMPLETADO")
print("=" * 60)
