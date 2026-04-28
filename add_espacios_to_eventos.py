#!/usr/bin/env python3
"""
Script para agregar espacios disponibles a los eventos en eventos-data.json
"""
import json
from pathlib import Path

# Espacios disponibles para cada evento
ESPACIOS_DISPONIBLES = {
    "food-trucks": [
        {
            "id": "food-truck-1",
            "tipo": "food-truck",
            "nombre": "Food Truck Premium",
            "tamaño": "5m × 10m",
            "capacidad": "15+ personas",
            "servicios": ["electricidad", "agua", "drenaje"],
            "precio_base": 1500.00,
            "disponibles": 5,
            "ubicaciones": ["entrada-principal", "escenario-1", "zona-vip"]
        },
        {
            "id": "food-truck-2",
            "tipo": "food-truck",
            "nombre": "Food Truck Estándar",
            "tamaño": "4m × 8m",
            "capacidad": "10+ personas",
            "servicios": ["electricidad", "agua"],
            "precio_base": 1000.00,
            "disponibles": 8,
            "ubicaciones": ["zona-central", "escenario-2", "escenario-3"]
        }
    ],
    "stalls": [
        {
            "id": "stall-1",
            "tipo": "stall",
            "nombre": "Puesto Estándar",
            "tamaño": "3m × 3m",
            "capacidad": "2-4 personas",
            "servicios": ["electricidad"],
            "precio_base": 800.00,
            "disponibles": 15,
            "ubicaciones": ["zona-comercial", "zona-central"]
        },
        {
            "id": "stall-2",
            "tipo": "stall",
            "nombre": "Puesto Premium",
            "tamaño": "4m × 4m",
            "capacidad": "4-6 personas",
            "servicios": ["electricidad", "agua", "drenaje"],
            "precio_base": 1200.00,
            "disponibles": 10,
            "ubicaciones": ["entrada-principal", "escenario-principal"]
        }
    ],
    "booths": [
        {
            "id": "booth-1",
            "tipo": "booth",
            "nombre": "Booth de Merchandising",
            "tamaño": "4m × 6m",
            "capacidad": "5-8 personas",
            "servicios": ["electricidad", "iluminación"],
            "precio_base": 2000.00,
            "disponibles": 8,
            "ubicaciones": ["escenario-principal", "entrada-vip"]
        },
        {
            "id": "booth-2",
            "tipo": "booth",
            "nombre": "Booth Experiencial",
            "tamaño": "6m × 6m",
            "capacidad": "10+ personas",
            "servicios": ["electricidad", "iluminación", "wifi"],
            "precio_base": 2500.00,
            "disponibles": 5,
            "ubicaciones": ["escenario-principal", "zona-vip"]
        }
    ],
    "popup-stores": [
        {
            "id": "popup-1",
            "tipo": "popup-store",
            "nombre": "Pop-up Store",
            "tamaño": "3m × 5m",
            "capacidad": "3-5 personas",
            "servicios": ["electricidad"],
            "precio_base": 900.00,
            "disponibles": 12,
            "ubicaciones": ["zona-comercial", "entrada-secundaria"]
        }
    ]
}

# Crear lista completa de espacios
TODOS_LOS_ESPACIOS = []
for categoria, espacios in ESPACIOS_DISPONIBLES.items():
    TODOS_LOS_ESPACIOS.extend(espacios)

# Leer eventos-data.json
json_path = Path(__file__).parent / "public" / "eventos-data.json"

print(f"📂 Leyendo: {json_path}")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✓ Cargados {len(data['principales'])} eventos\n")

# Agregar espacios_disponibles a cada evento
print("📝 Agregando espacios disponibles a eventos...\n")

for evento in data['principales']:
    evento['espacios_disponibles'] = TODOS_LOS_ESPACIOS
    print(f"✓ Evento: {evento['location']} - {len(TODOS_LOS_ESPACIOS)} espacios agregados")

# Guardar cambios
print(f"\n💾 Guardando cambios en: {json_path}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ ¡Espacios disponibles agregados a {len(data['principales'])} eventos!")
print(f"   Total de tipos de espacios: {len(TODOS_LOS_ESPACIOS)}")
print("\n📊 Espacios disponibles:")
for espacio in TODOS_LOS_ESPACIOS:
    print(f"   • {espacio['nombre']} ({espacio['tipo']}) - {espacio['disponibles']} disponibles - ${espacio['precio_base']}")
