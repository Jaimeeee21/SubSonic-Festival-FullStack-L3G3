#!/usr/bin/env python3
"""
Script para sincronizar reservas de espacios a Firebase
Toma las reservas de demostración de empresas y las sincroniza
"""
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from pathlib import Path
import json

# Inicializar Firebase
cred_path = Path(__file__).parent / "subsonic-festival-56216-firebase-adminsdk-fbsvc-fa73f8c742.json"
print(f"🔍 Buscando credenciales en: {cred_path}")

if not cred_path.exists():
    print(f"❌ NO ENCONTRADO: {cred_path}")
    exit(1)

try:
    cred = credentials.Certificate(str(cred_path))
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase inicializado\n")
except Exception as e:
    print(f"❌ Error inicializando Firebase: {e}")
    exit(1)

# Datos de reservas de espacios (correspondientes a las empresas registradas)
reservas = [
    {
        "id": "reserva-001",
        "empresa_id": "tuempresa-001",
        "evento_id": "madrid",
        "espacio_id": "food-truck-1",
        "tipo_espacio": "food-truck",
        "nombre_espacio": "Food Truck Premium",
        "tamaño": "5m × 10m",
        "nombre_negocio": "TuEmpresa Catering",
        "precio": 1500.00,
        "estado": "confirmada",
        "ubicacion_ideales": ["entrada-principal", "escenario-1"],
        "servicios_requiere": ["electricidad", "agua", "drenaje"],
        "fecha_reserva": datetime.now()
    },
    {
        "id": "reserva-002",
        "empresa_id": "tuempresa-001",
        "evento_id": "barcelona",
        "espacio_id": "stall-1",
        "tipo_espacio": "stall",
        "nombre_espacio": "Puesto Estándar",
        "tamaño": "3m × 3m",
        "nombre_negocio": "TuEmpresa Tienda",
        "precio": 800.00,
        "estado": "confirmada",
        "ubicacion_ideales": ["zona-comercial"],
        "servicios_requiere": ["electricidad"],
        "fecha_reserva": datetime.now()
    },
    {
        "id": "reserva-003",
        "empresa_id": "merch-store-001",
        "evento_id": "madrid",
        "espacio_id": "booth-1",
        "tipo_espacio": "booth",
        "nombre_espacio": "Booth de Merchandising",
        "tamaño": "4m × 6m",
        "nombre_negocio": "Merch Store Oficial",
        "precio": 2000.00,
        "estado": "confirmada",
        "ubicacion_ideales": ["escenario-principal"],
        "servicios_requiere": ["electricidad", "iluminación"],
        "fecha_reserva": datetime.now()
    },
    {
        "id": "reserva-004",
        "empresa_id": "sponsor-beverage-001",
        "evento_id": "valencia",
        "espacio_id": "stall-2",
        "tipo_espacio": "stall",
        "nombre_espacio": "Barra de Bebidas",
        "tamaño": "4m × 4m",
        "nombre_negocio": "Bebidas Refrescantes",
        "precio": 1200.00,
        "estado": "confirmada",
        "ubicacion_ideales": ["escenario-2"],
        "servicios_requiere": ["agua", "electricidad", "drenaje"],
        "fecha_reserva": datetime.now()
    }
]

print("📝 Sincronizando reservas de espacios a Firebase...\n")

# Limpiar reservas antiguas (opcional)
reservas_ref = db.collection("reservas_espacios")
# docs = reservas_ref.stream()
# count = 0
# for doc in docs:
#     doc.reference.delete()
#     count += 1
# print(f"   ✓ Eliminadas {count} reservas antiguas\n")

# Insertar nuevas reservas
for reserva in reservas:
    reserva_doc = {
        "empresa_id": reserva["empresa_id"],
        "evento_id": reserva["evento_id"],
        "espacio_id": reserva["espacio_id"],
        "tipo_espacio": reserva["tipo_espacio"],
        "nombre_espacio": reserva["nombre_espacio"],
        "tamaño": reserva["tamaño"],
        "nombre_negocio": reserva["nombre_negocio"],
        "precio": reserva["precio"],
        "estado": reserva["estado"],
        "ubicacion_ideales": reserva["ubicacion_ideales"],
        "servicios_requiere": reserva["servicios_requiere"],
        "fecha_reserva": reserva["fecha_reserva"],
        "created_at": datetime.now()
    }
    
    db.collection("reservas_espacios").document(reserva["id"]).set(reserva_doc)
    print(f"✓ Reserva #{reserva['id']}: {reserva['nombre_espacio']} en {reserva['evento_id']}")

print(f"\n✅ {len(reservas)} reservas de espacios sincronizadas a Firebase")

print("\n" + "=" * 60)
print("🎉 ¡SINCRONIZACIÓN DE RESERVAS COMPLETADA!")
print("=" * 60)
