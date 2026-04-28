#!/usr/bin/env python3
"""
Script para sincronizar datos de empresas a Firebase
Inserta empresas de demostración y sus espacios reservados
"""
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from pathlib import Path

# Inicializar Firebase
cred_path = Path(__file__).parent / "subsonic-festival-56216-3767f772323c.json"
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

# Datos de empresas de demostración
empresas = [
    {
        "id": "tuempresa-001",
        "nombre": "TuEmpresa S.L.",
        "cif": "B12345678",
        "descripcion": "Empresa de comida rápida y catering para eventos",
        "telefono": "+34-666-123-456",
        "email_contacto": "contacto@tuempresa.es",
        "website": "www.tuempresa.es",
        "logo_url": "https://via.placeholder.com/200?text=TuEmpresa",
        "tipo_empresa": "Catering",
        "estado": "activa",
        "espacios_reservados": [
            {
                "id": "espacio-001",
                "tipo_espacio": "food-truck",
                "nombre_espacio": "Food Truck Premium",
                "tamaño": "5m × 10m",
                "descripcion": "Espacio para food truck con suministro eléctrico y agua",
                "nombre_negocio": "TuEmpresa Catering",
                "precio": 1500.00,
                "estado": "confirmada",
                "ubicacion_ideales": ["entrada-principal", "escenario-1"],
                "servicios_requiere": ["electricidad", "agua", "drenaje"]
            },
            {
                "id": "espacio-002",
                "tipo_espacio": "stall",
                "nombre_espacio": "Puesto de Venta",
                "tamaño": "3m × 3m",
                "descripcion": "Puesto estándar para venta de productos",
                "nombre_negocio": "TuEmpresa Tienda",
                "precio": 800.00,
                "estado": "confirmada",
                "ubicacion_ideales": ["zona-comercial"],
                "servicios_requiere": ["electricidad"]
            }
        ]
    },
    {
        "id": "merch-store-001",
        "nombre": "Merch Store S.A.",
        "cif": "A87654321",
        "descripcion": "Tienda especializada en merchandising de festivales",
        "telefono": "+34-666-789-012",
        "email_contacto": "info@merchstore.es",
        "website": "www.merchstore.es",
        "logo_url": "https://via.placeholder.com/200?text=MerchStore",
        "tipo_empresa": "Merchandising",
        "estado": "activa",
        "espacios_reservados": [
            {
                "id": "espacio-003",
                "tipo_espacio": "booth",
                "nombre_espacio": "Booth de Merchandising",
                "tamaño": "4m × 6m",
                "descripcion": "Booth con mostrador y vitrina para merchandising",
                "nombre_negocio": "Merch Store Oficial",
                "precio": 2000.00,
                "estado": "confirmada",
                "ubicacion_ideales": ["escenario-principal", "entrada-vip"],
                "servicios_requiere": ["electricidad", "iluminación"]
            }
        ]
    },
    {
        "id": "sponsor-beverage-001",
        "nombre": "Bebidas Refrescantes S.L.",
        "cif": "B56789012",
        "descripcion": "Empresa de bebidas refrescantes y servicios de bar",
        "telefono": "+34-666-345-678",
        "email_contacto": "eventos@bebidasref.es",
        "website": "www.bebidasrefrescantes.es",
        "logo_url": "https://via.placeholder.com/200?text=Bebidas",
        "tipo_empresa": "Bebidas",
        "estado": "activa",
        "espacios_reservados": [
            {
                "id": "espacio-004",
                "tipo_espacio": "stall",
                "nombre_espacio": "Barra de Bebidas",
                "tamaño": "6m × 4m",
                "descripcion": "Barra de servicio con máquinas de bebidas",
                "nombre_negocio": "Bebidas Refrescantes",
                "precio": 1200.00,
                "estado": "confirmada",
                "ubicacion_ideales": ["escenario-2", "escenario-3"],
                "servicios_requiere": ["agua", "electricidad", "drenaje"]
            }
        ]
    }
]

print("📝 Insertando empresas en Firebase...\n")

for empresa in empresas:
    # Guardar empresa
    empresa_doc = {
        "nombre": empresa["nombre"],
        "cif": empresa["cif"],
        "descripcion": empresa["descripcion"],
        "telefono": empresa["telefono"],
        "email_contacto": empresa["email_contacto"],
        "website": empresa["website"],
        "logo_url": empresa["logo_url"],
        "tipo_empresa": empresa["tipo_empresa"],
        "estado": empresa["estado"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    db.collection("empresas").document(empresa["id"]).set(empresa_doc)
    print(f"✓ Empresa: {empresa['nombre']} ({empresa['tipo_empresa']})")
    
    # Guardar espacios reservados
    for espacio in empresa.get("espacios_reservados", []):
        espacio_doc = {
            "empresa_id": empresa["id"],
            "tipo_espacio": espacio["tipo_espacio"],
            "nombre_espacio": espacio["nombre_espacio"],
            "tamaño": espacio["tamaño"],
            "descripcion": espacio["descripcion"],
            "nombre_negocio": espacio["nombre_negocio"],
            "precio": espacio["precio"],
            "estado": espacio["estado"],
            "ubicacion_ideales": espacio["ubicacion_ideales"],
            "servicios_requiere": espacio["servicios_requiere"],
            "fecha_reserva": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        db.collection("empresas").document(empresa["id"]).collection("espacios").document(espacio["id"]).set(espacio_doc)
        print(f"  ├─ Espacio: {espacio['nombre_espacio']} ({espacio['tipo_espacio']})")

print(f"\n✅ {len(empresas)} empresas insertadas")
total_espacios = sum(len(e.get("espacios_reservados", [])) for e in empresas)
print(f"✅ {total_espacios} espacios reservados insertados")

print("\n" + "=" * 60)
print("🎉 ¡SINCRONIZACIÓN DE EMPRESAS COMPLETADA!")
print("=" * 60)
